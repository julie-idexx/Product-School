# Agent Registry — Comeback Coach

*The three agents built across this course, registered as one connected system. Every field below is real — pulled from the actual scripts and specs in `agents/`, not aspirational.*

## 1. Registry

### Metric Pulse Agent

| Field | Value |
|---|---|
| **Name** | `metric_pulse.py` |
| **Trigger** | Runs unconditionally on its schedule (not event-driven) |
| **Data sources** | `data/users.csv` (`acquisition_channel`), `data/retention.csv` (`day_7`, `broke_streak_week1`, `cohort_week`) |
| **Output format** | Slack digest: headline metric + per-channel breakdown + `⚠️ ALERT` flags at ±2pts WoW + "Top signal" line + a "Next: run anomaly diagnosis?" CTA |
| **Delivery channel** | Slack (via `--post` + `SLACK_WEBHOOK_URL`); always prints/saves regardless |
| **Trigger schedule** | Nightly (cron); the digest itself is framed as landing Monday 8am |
| **Owner** | PM (Julie) — prototype stage; see `metric-pulse.md` §4 for the Python+cron / n8n / dev-ticket handoff plan |

### Anomaly-to-Hypothesis Agent

| Field | Value |
|---|---|
| **Name** | `anomaly_diagnosis.py` |
| **Trigger** | **Event-driven, not scheduled** — chained off Metric Pulse via `--chain-anomaly`, fires only when Day-7 retention or streak-break rate has already crossed the 2pt alert threshold |
| **Data sources** | The decomposition Metric Pulse just computed (streak-break rate + per-channel Day-7 rates in real runs; `sessions_week1` / `push_optin_rate` in the simulated test scenarios) |
| **Output format** | One of three Slack diagnostic variants (full diagnostic + SQL, low-confidence, inconclusive) — see `anomaly-diagnosis.md` §3 |
| **Delivery channel** | Slack + an entry appended to `outcome-log.md` (project root) |
| **Trigger schedule** | None of its own — purely reactive to Metric Pulse's alert |
| **Owner** | PM (Julie) — Step 3 (hypothesis generation) is an explicit heuristic stand-in; owning a real LLM call there before this runs unattended is the next real handoff, not a "nice to have" |

### Weekly Insight Report

| Field | Value |
|---|---|
| **Name** | `weekly_insight.py` |
| **Trigger** | Runs unconditionally on its schedule |
| **Data sources** | `data/users.csv` + `data/retention.csv` (via Metric Pulse's own functions, not reimplemented), `change_log.md` + `git log` (sprint completions), `02-research/weekly-synthesis-log.md` or `02-research/nps-analysis.md` (feedback signal), `data/nudges.csv` (push-notification fallback signal), `04-team/stakeholders/*.md` (fallback watch item), **and `outcome-log.md`** (the Anomaly agent's output — see §2) |
| **Output format** | 3-2-1 report: Done (3) / Changed (2) / Watch (1) |
| **Delivery channel** | Saved to `reports/YYYY-MM-DD.md` (the "versioned file" — one dated file per run) + a condensed Slack summary |
| **Trigger schedule** | Friday 4pm |
| **Owner** | PM (Julie) |

## 2. Connection plan

**Metric Pulse → Anomaly Agent: wired and tested.** `metric_pulse.py --chain-anomaly` checks its own two alert flags (`day7_alert`, `break_alert`) after computing the digest. If neither fired, it's a no-op — printed and confirmed in testing (`agents/metric-pulse.md`, `agents/anomaly-diagnosis.md`). If either fired, it builds a real decomposition (streak-break rate + each channel's Day-7 rate) and calls `anomaly_diagnosis.run_diagnosis()` **in-process** — not a separate scheduled job that might drift out of sync, a direct function call with the exact numbers Metric Pulse just computed.

**Anomaly Agent → Weekly Insight: wired and tested this session.** This connection didn't exist before now — `weekly_insight.py` previously only pulled "Watch next week" from stakeholder open items and had no idea `outcome-log.md` existed. Added `read_outcome_log_entries()` and `anomaly_connection_bullets()`, which look at `outcome-log.md` for anything logged in the report's 7-day window:

- **An unresolved diagnosis** (still `_TBD_`) becomes the **Watch next week** item, displacing the standing stakeholder-open-item fallback — a scored, dated hypothesis waiting on confirmation is more concretely actionable than a stakeholder note that may not have moved in weeks.
- **A confirmed diagnosis** (someone filled in "what actually happened") becomes the **lead item in Changed this week** — a root cause getting confirmed is real news, and it displaces the routine retention-channel bullet down to second place rather than competing on equal footing.

Both directions were verified against constructed `outcome-log.md` files before being called done — an unresolved entry correctly took over the Watch slot, a resolved entry correctly led Changed, and the report still degrades gracefully to the old behavior when `outcome-log.md` doesn't exist yet (the real current state — no diagnosis has been triggered and confirmed yet).

**What's still a manual step, on purpose:** filling in `outcome-log.md`'s "what actually happened" column. No agent should auto-close that loop — confirming a root cause is a human judgment call, the same reason `anomaly_diagnosis.py`'s Step 3 stays a flagged heuristic rather than a rubber-stamped auto-diagnosis.

## 3. Learning loop

See [`agents/learning-loop.md`](learning-loop.md) — a weekly self-review prompt, not a script (scoring a hypothesis against reality is a reasoning task, same reason Step 3 above isn't scriptable either). Reads `outcome-log.md`, scores each resolved diagnosis hit / miss / partial, and proposes exactly one heuristic update to `CLAUDE.md` — proposes, never auto-applies.

## 4. Six-month roadmap — one agent per month

Grounded in the actual open threads this project already has on record, not generic agent ideas:

| Month | Agent | Closes |
|---|---|---|
| 1 | **Experiment Guardrail Agent** | Tracks sample-size accrual toward the ~1,565/arm the pilot's own power analysis called for (`data/experiment-design.md`), and flags the go/no-go date from `docs/recommendation-memo.md` automatically instead of relying on someone remembering it. |
| 2 | **Cohort Quality Agent** | Runs the acquisition-channel/intent-mismatch hypothesis (`data/metric-diagnosis.md`'s H1, confidence 7/10, flagged as "cheapest to test, highest confidence") at scale, continuously — the single most important open diagnostic question, currently answered from one small sample. |
| 3 | **Day-30 Durability Tracker** | Re-runs the significance check on Day-30 retention as the extended pilot cohort accrues data, and alerts the moment it crosses (or definitively fails to cross) significance — the one claim that's stayed unproven since `hypothesis.md`. |
| 4 | **Notification Fatigue Monitor** | Watches whether the pilot's surprising finding (engagement climbing across sends, not fatiguing) holds as volume scales past n=50/arm, or whether real fatigue finally shows up — the "key tension, still live" line in `CLAUDE.md`. |
| 5 | **Design-Review Closer Agent** | Resolves the still-open loop from Lena's interrupted design review (three unanswered questions, no file ever saved) by scheduling and tracking a real follow-up instead of letting it stay an invisible gap, the same class of issue `workspace-audit.md` flagged once already. |
| 6 | **Comeback Coach Brain** | Reads every agent above plus this stack's own outputs and produces one monthly synthesis for Marcus — automating what `recommendation-memo.md` and `presentation.pptx` currently take a PM to hand-build, closing the loop from raw signal to a leadership-ready ask. |
