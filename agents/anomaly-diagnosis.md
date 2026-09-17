# Anomaly Diagnosis Agent — Streakly

*Module 6 Agent Stack, third of three. Chained off `metric_pulse.py` — only runs when metric_pulse's Day-7 retention or streak-break-rate alert has already fired.*

## 1. The updated agent

[`agents/anomaly_diagnosis.py`](anomaly_diagnosis.py) — the 5-step loop, standard library only.

[`agents/metric_pulse.py`](metric_pulse.py) — extended with a `--chain-anomaly` flag. When either alert fires, it builds a real decomposition (streak-break rate + each acquisition channel's Day-7 rate — the actual metric tree this data supports) and calls `anomaly_diagnosis.run_diagnosis()` directly. If neither alert fired, it's a no-op — the chain only triggers on alert, never unconditionally.

**Honesty note, upfront, because it matters for how to read everything below:** Steps 1 and 2 are pure data computation — fully deterministic, fully testable, no judgment involved. Step 3 (generating ranked hypotheses with confidence scores) is a *reasoning* task, not a data computation, and a cron job can't actually reason. `generate_hypotheses()` is a deterministic heuristic — good enough to test the loop's mechanics and stop-conditions end to end, which is exactly what the simulated test below verifies, but it is **not** a substitute for real hypothesis generation. In production, that function is where a real LLM call belongs — the same kind of reasoning a PM/Claude already did by hand in `05-decide/metric-findings.md` and `data/metric-diagnosis.md` for the actual week-5 pilot.

## 2. Conditions at each step

| Step | What it checks | Passes → continue | Fails → |
|---|---|---|---|
| 1. Threshold check | \|Δ\| on the triggering metric ≥ 2pts | Yes → Step 2 | No → log only, stop (this shouldn't normally happen — metric_pulse only chains when its own alert already fired at this threshold) |
| 2. Metric tree decomposition | How many component drivers moved meaningfully (each driver has its own threshold — 2pts for point-based drivers, 10% relative for `sessions_week1`) | ≥ 2 drivers moved → Step 3 | Exactly 0–1 drivers moved → **Inconclusive**, stop. Not enough decomposed signal to build a real hypothesis on top of. |
| 3. Hypothesis generation | Top-ranked hypothesis's confidence score | **Strictly above** 6/10 → Step 4 | ≤ 6/10 → **Low confidence**, stop. Posting a guess with a number attached to it is worse than saying "not confident enough yet." |
| 4. SQL + Slack | — | Always runs once Step 3 passes | — |
| 5. Log the call | — | Always runs, regardless of which step stopped the loop (except Step 1) | — |

## 3. Slack diagnostic format

**Full diagnostic** (Steps 1–4 all passed):

```
🔍 Streakly Anomaly Detected, {day}, {time}

Trigger: {Metric name} {dropped|rose} {N}pts ({before}% → {after}%) overnight

Metric tree decomposition:
  {driver 1}: {before} → {after} ({Δ}) [MOVED]
  {driver 2}: {before} → {after} ({Δ}) [MOVED]
  {driver 3}: {before} → {after} ({Δ})

Top 3 hypotheses:
1. {hypothesis} ({likelihood label}, {rationale}) — confidence {N}/10
2. {hypothesis} ({likelihood label}, {rationale}) — confidence {N}/10
3. {hypothesis} ({likelihood label}, {rationale}) — confidence {N}/10

SQL to confirm hypothesis 1:
```
{SQL for the top hypothesis}
```

Logged to outcome-log.md. Run this query and reply with the output. I'll interpret.
```

**Low confidence** (Step 3 failed):

```
⚠️ Streakly Anomaly — Low Confidence, {day}, {time}

Trigger: {Metric name} {dropped|rose} {N}pts overnight

Metric tree decomposition:
  {each driver, same format as above}

Top hypothesis: {hypothesis} — confidence {N}/10 (below the 6/10 threshold)

Stopping here rather than posting a guess. Logged to outcome-log.md — needs a human look before this becomes a diagnosis.
```

**Inconclusive** (Step 2 failed — not explicitly requested but a real, necessary third state, since Step 2's own stop condition needs somewhere to go):

```
❓ Streakly Anomaly — Inconclusive, {day}, {time}

Trigger: {Metric name} {dropped|rose} {N}pts overnight

Metric tree decomposition:
  {each driver, same format as above}

Only one driver moved meaningfully — not enough to decompose the cause. Flagged inconclusive rather than guessing at a 1-driver story.
```

## 4. Simulated test — verifying the loop runs correctly end to end

Four scenarios in [`agents/scenarios/`](scenarios/), one per stop point, plus two runs against real project data via `metric_pulse.py --chain-anomaly`.

**What running these actually caught, before any of this went near a schedule:**

1. Step 1 and Step 2 used two different conventions for "is this value a fraction (0.22) or a whole percentage point (22)?" — Step 1 auto-detected which one it got; Step 2 didn't, so a driver value passed as a fraction would silently produce a delta 100x too small and never trip its own threshold. Fixed by giving Step 2 the same auto-detect Step 1 already had.
2. Two of the three Slack formatters (`low_confidence`, `inconclusive`) were still calling the old ad-hoc date-formatting and metric-name-formatting code directly instead of the shared `display_name()`/`format_time()` helpers — caught by actually reading the printed output ("Day7 Retention", lowercased dates) rather than trusting that a helper function existed meant every caller used it.

**Scenario 1 — the requested test, a 4-point retention drop (`scenarios/day7_drop_4pt.json`), matching the sample's exact shape:**

```bash
python3 anomaly_diagnosis.py --simulate scenarios/day7_drop_4pt.json --outcome-log /tmp/outcome-log-test.md
```

```
🔍 Streakly Anomaly Detected, Thu Sep 17, 11:14am

Trigger: Day-7 retention dropped 4pts (39% → 35%) overnight

Metric tree decomposition:
  streak_break_rate: 22 -> 29 (+7.0pts) [MOVED]
  sessions_week1: 4.1 -> 3.2 (-22%) [MOVED]
  push_optin_rate: 54 -> 51 (-3.0pts) [MOVED]

Top 3 hypotheses:
1. Push notification delivery issue (high likelihood, correlates with session drop) — confidence 8/10
2. New user cohort quality shift (channel mix) (medium, streak-break rate moved sharply) — confidence 6/10
3. Streak-reset copy or notification-copy regression after the last deploy (low, no direct signal for this in the decomposition - needs confirmation, not ruled out) — confidence 3/10

SQL to confirm hypothesis 1:
```
SELECT date, COUNT(*) AS push_sent, SUM(delivered) AS push_delivered,
       AVG(opened) AS open_rate
FROM streakly_notifications
WHERE sent_date >= CURRENT_DATE - 7
GROUP BY date
ORDER BY date;
```

Logged to outcome-log.md. Run this query and reply with the output. I'll interpret.

[status: posted]
```

**Scenario 2 — below the alert threshold (`scenarios/below_threshold.json`, a 1pt move):**

```
Step 1 (threshold check): day7_retention moved -1pts -> STOP - log only, no diagnosis needed
[status: stopped_below_threshold]
```

**Scenario 3 — only one driver moved (`scenarios/inconclusive_1driver.json`):**

```
❓ Streakly Anomaly — Inconclusive, Thu Sep 17, 11:14am
Trigger: Day-7 retention dropped 4pts overnight
Metric tree decomposition:
  streak_break_rate: 22 -> 29 (+7.0pts) [MOVED]
  sessions_week1: 4.1 -> 4.0 (-2%)
  push_optin_rate: 54 -> 53 (-1.0pts)
Only one driver moved meaningfully — not enough to decompose the cause. Flagged inconclusive rather than guessing at a 1-driver story.
[status: inconclusive]
```

**Scenario 4 — two drivers moved, but the top hypothesis doesn't clear the confidence bar (`scenarios/low_confidence.json`):**

```
⚠️ Streakly Anomaly — Low Confidence, Thu Sep 17, 11:14am
Trigger: Day-7 retention dropped 3pts overnight
Metric tree decomposition:
  streak_break_rate: 22 -> 24 (+2.0pts) [MOVED]
  sessions_week1: 4.1 -> 3.6 (-12%) [MOVED]
  push_optin_rate: 54 -> 54 (+0.0pts)
Top hypothesis: Push notification delivery issue — confidence 5/10 (below the 6/10 threshold)
Stopping here rather than posting a guess. Logged to outcome-log.md — needs a human look before this becomes a diagnosis.
[status: low_confidence]
```

**Chained against real data — `metric_pulse.py --week 4 --chain-anomaly`** (real week-4-vs-3 comparison, which alerts on both metrics):

```
[--chain-anomaly: alert fired, running anomaly_diagnosis]

⚠️ Streakly Anomaly — Low Confidence, Thu Sep 17, 11:21am

Trigger: Day-7 retention dropped 4pts overnight

Metric tree decomposition:
  streak_break_rate: 45.0 -> 35.0 (-10.0pts) [MOVED]
  channel_organic: 29.4 -> 29.4 (+0.0pts)
  channel_paid: 41.2 -> 14.7 (-26.5pts) [MOVED]
  channel_referral: 21.9 -> 37.5 (+15.6pts) [MOVED]

Top hypothesis: New user cohort quality shift (channel mix) — confidence 6/10 (below the 6/10 threshold)

Stopping here rather than posting a guess. Logged to outcome-log.md — needs a human look before this becomes a diagnosis.

[anomaly_diagnosis status: low_confidence]
```

This is the honest, expected outcome for a *real* chained run: real data only supports a channel + streak-break-rate decomposition (no push-opt-in or sessions fields exist in this dataset), so the heuristic has less to work with than the simulated scenario and correctly lands right at the confidence boundary rather than forcing a guess — exactly the case Step 3's gate exists to catch. It also confirms the chain fires on **either** alert, not just Day-7: a separate check (`--week 2`, `metric_pulse.py --json`) showed `day7_alert: false` but `break_alert: true`, and the chain still triggered correctly off the streak-break-rate alert alone.

**Every stop point in the spec fired in at least one of the six runs above** — below-threshold, inconclusive, low-confidence, and full-diagnostic all verified before this goes anywhere near a schedule.
