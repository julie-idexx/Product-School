# Metric Pulse Agent — Streakly

*Module 6 Agent Stack, first of three. Monitors Day-7 retention and streak-break rate, week over week, by acquisition channel. Runs nightly; delivers Monday 8am.*

## 1. The agent script

[`agents/metric_pulse.py`](metric_pulse.py) — a self-contained Python script, no dependencies beyond the standard library.

What it does:

- Loads `users.csv` (for `acquisition_channel`) and `retention.csv` (for `day_7`, `broke_streak_week1`), and joins them on `user_id`.
- **"This week" vs. "last week"** is defined as the two most recent `cohort_week` values in the data. *(This project's sample data is organized by weekly signup cohort rather than a rolling timestamp — in a live system with real event timestamps, swap this for an actual rolling 7-day window. See the docstring at the top of the script.)*
- Computes the overall Day-7 retention rate and streak-break rate for each week, plus the same two metrics split by `organic` / `paid` / `referral`.
- Flags an alert when either headline metric moves **2 or more percentage points** week over week, and flags a channel with "← watch this" under the same threshold.
- **Detects an active A/B test automatically** (any user in that cohort with a non-blank `variant`) and prepends a warning to the digest rather than silently reporting a treatment effect as if it were organic movement. This isn't a hypothetical edge case — it's exactly what the real data does, see the test run below.
- Formats the Slack digest text and, with `--post`, sends it to a Slack incoming webhook.

## 2. Slack message template

```
📊 Streakly Retention Pulse, {day} {month} {date}
[⚠️ {experiment_note} — only present if an A/B test is live in either week]

Day-7 retention: {pct}% ({arrow} {n}pts vs last week) [⚠️ ALERT — if |Δ| ≥ 2pts]
(baseline: 39%)

By channel:
  Organic: {pct}% ({arrow} {n}pts) [← watch this — if |Δ| ≥ 2pts]
  Paid: {pct}% ({arrow} {n}pts) [← watch this]
  Referral: {pct}% ({arrow} {n}pts) [← watch this]

Streak-break rate: {pct}% ({arrow} {n}pts vs last week) [⚠️ ALERT]
By channel:
  Organic: {pct}% ({arrow} {n}pts) [← watch this]
  Paid: {pct}% ({arrow} {n}pts) [← watch this]
  Referral: {pct}% ({arrow} {n}pts) [← watch this]

Top signal: {channel} channel {drop accelerating | notable improvement}. [Check campaign changes from last week. — only on a drop]

Next: run anomaly diagnosis? Reply YES to trigger.
```

`{arrow}` is `↓` / `↑` / `→ flat`. The "Next: run anomaly diagnosis?" line is a static prompt for now — see the wiring note below for what it would take to make it a real interactive trigger rather than text.

## 3. Running it manually to verify output

```bash
cd agents
python3 metric_pulse.py --users /path/to/data/users.csv --retention /path/to/data/retention.csv
```

- Default paths are `../data/users.csv` and `../data/retention.csv` — that only resolves once `data/` lives inside this project (see `workspace-audit.md`'s reorg suggestion #2); until then, pass `--users`/`--retention` explicitly, as in the test run below.
- Add `--json` to also print the raw computed numbers (`day7_now`, `day7_delta_pts`, `channel_deltas_pts`, etc.) — useful for checking the digest text against the actual math, not just eyeballing it.
- Add `--week N` to force a specific `cohort_week` as "this week" instead of the latest one — this is how the second test run below produces a clean, non-experiment comparison for demo purposes.
- **Nothing gets posted to Slack unless you pass `--post`.** Without it, the script only prints — safe to run repeatedly while checking the output.
- To actually post: `export SLACK_WEBHOOK_URL=https://hooks.slack.com/services/...` then run with `--post`.

## 4. How this would be wired in the real world

| Option | What it's good for | What it costs |
|---|---|---|
| **Python + cron** | Fastest path to something actually running unattended today. The script already works — `crontab -e` and a nightly line is the entire setup. | Needs a machine that's always on (not a PM's laptop). No retry, no failure alerting — if the script errors at 2am, nobody knows until Monday's digest doesn't show up. Credentials live in a shell env on whatever box runs it. |
| **n8n** | A real scheduler with built-in retry, run history, and a native Slack node (handles auth/formatting for you) — a PM can change the schedule or the destination channel without touching Python. | The metric computation itself still has to live somewhere — either as a Code node running this same script, or rewritten to query a warehouse table once CSVs are replaced by real data. n8n orchestrates; it doesn't replace the logic in `metric_pulse.py`. |
| **Developer ticket** | The real destination: reads from the production database instead of a CSV snapshot, runs on whatever the data-eng team already uses (Airflow, dbt, etc.), gets proper on-call ownership and monitoring. | Takes real engineering time and has to get prioritized. Slowest to ship. |

**Recommendation for right now:** this is exactly the "validate it works before asking anyone to build it" stage — Python + cron (or n8n if it needs to survive a laptop reboot) is the right next step, not a ticket yet. The script itself, including the A/B-test-detection logic the test run below actually needed, is the spec to hand to engineering once this earns a permanent home — the same build-then-hand-off pattern already used for the Comeback screen itself (`04-team/spec-readiness.md`).

## 5. Test run against the real Streakly snapshot

**Run 1 — the actual latest data (`cohort_week 5` vs. `4`).** This is the honest result, including the thing the script exists partly to catch: week 5 is the live A/B test cohort, so the jump below is not a clean organic signal.

```
$ python3 metric_pulse.py --users .../data/users.csv --retention .../data/retention.csv

📊 Streakly Retention Pulse, Thu Sep 17
⚠️ Note: cohort_week 5 includes an active A/B test. Movement below blends the treatment effect with organic change - see 05-decide/metric-findings.md before treating this as a pure organic signal.

Day-7 retention: 61% (↑ 34pts vs last week) ⚠️ ALERT
(baseline: 39%)

By channel:
  Organic: 82% (↑ 53pts)  ← watch this
  Paid: 58% (↑ 43pts)  ← watch this
  Referral: 42% (↑ 5pts)  ← watch this

Streak-break rate: 45% (↑ 10pts vs last week) ⚠️ ALERT
By channel:
  Organic: 38% (↓ 3pts)  ← watch this
  Paid: 58% (↑ 22pts)  ← watch this
  Referral: 39% (↑ 11pts)  ← watch this

Top signal: Organic channel notable improvement.

Next: run anomaly diagnosis? Reply YES to trigger.
```

**Run 2 — `--week 4`, a clean pre-experiment comparison (`cohort_week 4` vs. `3`).** No experiment note fires, since neither week has a `variant` set. This is what a normal week looks like, and it matches the shape of the spec's sample output closely — a real drop, a real per-channel culprit, a real actionable "top signal."

```
$ python3 metric_pulse.py --week 4 --users .../data/users.csv --retention .../data/retention.csv

📊 Streakly Retention Pulse, Thu Sep 17

Day-7 retention: 27% (↓ 4pts vs last week) ⚠️ ALERT
(baseline: 39%)

By channel:
  Organic: 29% (→ flat)
  Paid: 15% (↓ 26pts)  ← watch this
  Referral: 38% (↑ 16pts)  ← watch this

Streak-break rate: 35% (↓ 10pts vs last week) ⚠️ ALERT
By channel:
  Organic: 41% (↓ 9pts)  ← watch this
  Paid: 35% (↓ 12pts)  ← watch this
  Referral: 28% (↓ 9pts)  ← watch this

Top signal: Paid channel drop accelerating. Check campaign changes from last week.

Next: run anomaly diagnosis? Reply YES to trigger.
```

**What this confirms before scheduling anything:** the math, the threshold logic, and the channel breakdown all work correctly against real data — and, just as importantly, the agent caught its own biggest failure mode (conflating an A/B test with organic movement) on the very first run against real data, rather than needing that bug reported later.
