# Weekly Insight Agent — Streakly

*Module 6 Agent Stack, second of three. Pulls retention metrics, sprint completions, and the top user-feedback signal into a fixed 3-2-1 report: Done this week / Changed this week / Watch next week.*

## 1. The agent script

[`agents/weekly_insight.py`](weekly_insight.py) — standard library only, imports `metric_pulse.py` directly rather than re-implementing its retention math, so the two agents can never quietly disagree about the same numbers.

**Sources, and exactly how each one is used:**

1. **Retention metrics** (`data/users.csv` + `data/retention.csv`) — same "this week vs. last week by `cohort_week`" comparison as `metric_pulse.py`, and it inherits the same active-experiment detection. The single largest channel movement becomes the first "Changed" bullet.
2. **Sprint completions** (`change_log.md`) — every row dated in the last 7 days becomes a "Done" candidate. `change_log.md` is often too sparse to reach 3 real entries on its own (it logs decisions, not every commit), so the script fills any remaining slots from `git log` in the same window, skipping anything that already duplicates a change_log entry.
3. **Top user-feedback signal** (`02-research/weekly-synthesis-log.md` if a fresh entry exists there this week, otherwise the standing `02-research/nps-analysis.md`) — this becomes the second "Changed" bullet **only when there's something genuinely new to report.** If nothing new came through `research-synthesis`'s inbox this week, reporting the same static NPS theme as "changed" would be dishonest, so the script falls back to a real, freshly computed signal instead: the push-notification (`data/nudges.csv`) open-rate move.

**"Watch next week"** scans `04-team/stakeholders/*.md` in priority order (Raj, then Marcus, then Lena) and surfaces the first bolded "Open items" line it finds — Raj's engineering blocker wins by default since it's the most concretely actionable for a PM to track week to week.

## 2. Slack message template

```
📋 Streakly Weekly Insight, {day} {month} {date}

Done this week:
• {change_log or git-log item 1}
• {change_log or git-log item 2}
• {change_log or git-log item 3}

Changed this week:
• {largest retention channel movement} [+ A/B-test caveat if the week is affected]
• {fresh feedback theme this week} OR {push-notification open-rate move} OR {a plain note that nothing moved / nothing new came in}

Watch next week:
• {top-priority stakeholder open item}
```

The actual Slack post (`--post`) sends a condensed 3-2-1 one-liner-per-section version of the same content — the full version above is what gets saved to disk.

## 3. Running it manually to verify output

```bash
cd agents
python3 weekly_insight.py --users /path/to/data/users.csv --retention /path/to/data/retention.csv --nudges /path/to/data/nudges.csv
```

- Defaults assume `data/`, `change_log.md`, `02-research/`, and `04-team/stakeholders/` all live at the project root, one level up from `agents/` — true once `data/` is brought inside the project (see `workspace-audit.md`), pass the three `--users`/`--retention`/`--nudges` flags explicitly until then.
- `--week N` forces a specific `cohort_week` as "this week," for backtesting or demoing a week that isn't the live one — same flag as `metric_pulse.py`, and it now drives *both* the retention comparison and the push-notification comparison consistently (it didn't at first; see the test run below).
- `--json` prints the raw picked bullets and metadata alongside the formatted report.
- Every run saves to `reports/YYYY-MM-DD.md` regardless of `--post` — nothing needs to touch Slack to verify the file output.
- `--post` requires `SLACK_WEBHOOK_URL` in the environment; without it, the script only prints and saves.

## 4. How this would be wired in the real world

Same three options as `metric_pulse.py` (`agents/metric-pulse.md` §4), with the same recommendation: **Python + cron for now.** The one addition specific to this agent — it shells out to `git log`, so whatever runs it needs the repo checked out locally with history available, not just the CSV snapshot. That's a non-issue for cron on a machine with the repo cloned, but worth calling out explicitly if this ever moves to n8n or a hosted runner that only has data-file access.

## 5. Test run against the real Streakly snapshot

**What "run it manually first" actually caught, before this got anywhere near a schedule:**

1. **First run, true latest data (`cohort_week 5` vs. `4`):** the retention side correctly flagged the active A/B test (inherited from `metric_pulse.py`), but the push-notification side didn't — it silently reported "dropped 9pts to 12%." That number was wrong: in `cohort_week 5`, the comeback-arm's nudges get logged under a *different* `nudge_type` (`comeback_screen`) than the control arm (`streak_lost`), so comparing `streak_lost` open rate week over week was quietly comparing "everyone" (week 4) against "just the control arm" (week 5) — a population change caused by the experiment, not a real drop. Fixed by giving the push-notification check the same active-experiment guard the retention check already had.
2. **Second bug, caught while verifying the fix with `--week 4`:** the push-notification comparison ignored `--week` entirely and always looked at its own latest two send-dates, so it stayed inconsistent with whatever week the rest of the report was demonstrating. Fixed by making both signals share the same week-number context.

**Run 1 — clean pre-experiment comparison (`--week 4`, i.e. `cohort_week 4` vs. `3`):**

```
📋 Streakly Weekly Insight, Thu Sep 17

Done this week:
• Ran an agentic interview round (P3L2a) against the Comeback screen prototype — Claude in character as Priya, Tom, and Amara.
• Day 1 of discovery phase for the Comeback experience
• Add metric pulse agent - Module 6 agent stack, first of three

Changed this week:
• Paid channel retention dropped 26pts, now 15%, accelerating decline
• Push notification open rate recovered 6pts to 21%

Watch next week:
• Raj's open item: Still waiting on data-model clarification for the streak-freeze field.
```

**Run 2 — true latest data (`cohort_week 5` vs. `4`), the honest result including the A/B test:**

```
📋 Streakly Weekly Insight, Thu Sep 17

Done this week:
• Ran an agentic interview round (P3L2a) against the Comeback screen prototype — Claude in character as Priya, Tom, and Amara.
• Day 1 of discovery phase for the Comeback experience
• Add metric pulse agent - Module 6 agent stack, first of three

Changed this week:
• Organic channel retention rose 53pts, now 82%, recovering (week includes an active A/B test - see metric-pulse.md)
• Push notification open rate comparison skipped this week - the nudge_type split changed because of the active A/B test; comparing it as-is would compare different populations, not a real week-over-week move

Watch next week:
• Raj's open item: Still waiting on data-model clarification for the streak-freeze field.
```

*(Run 2's output is what's actually saved at [`reports/2026-09-17.md`](../reports/2026-09-17.md) — the true current state, not the cleaner demo.)*

**What this confirms before scheduling anything:** the 3-2-1 structure holds, `change_log.md` + `git log` reliably fills three real "Done" bullets even when the log itself is sparse, and — same lesson as `metric_pulse.py` — the agent's first real run against real data surfaced a genuine correctness bug (twice) rather than a clean-looking but wrong number making it into a Monday report unnoticed.
