# Learning Loop — Comeback Coach Self-Review

*A weekly self-review prompt, not a script. Scoring a hypothesis against what actually happened is a judgment call — the same reason `anomaly_diagnosis.py`'s Step 3 stays a flagged heuristic rather than something a cron job does unattended.*

**Trigger prompt** — paste this to run it:
> Run the weekly learning loop on outcome-log.md.

## Steps

1. **Read `outcome-log.md` in full.** Skip any entry where every "What actually happened" cell is still `_TBD_` — there's nothing to score yet, and scoring an unresolved entry would just be guessing at the guess.
2. **For each resolved entry, score the top-ranked hypothesis** (not all three — the loop that matters is "was the thing we'd have acted on first actually right"):
   - **Hit** — the confirmed cause matches the top hypothesis.
   - **Miss** — the confirmed cause is something the hypothesis set didn't even name.
   - **Partial** — the confirmed cause overlaps with the top hypothesis but isn't the whole story.
3. **Look for a pattern across entries, not just a tally.** One miss is noise. The same *kind* of miss twice is a real gap in `generate_hypotheses()`'s candidate set or confidence weighting.
4. **Propose exactly one heuristic update to `CLAUDE.md`.** Not three, not "several things to consider" — the discipline is picking the single change most likely to prevent the next miss. State it as a concrete edit, not a vague direction.
5. **Do not apply the edit.** Propose it and wait — the same human-approval pattern this whole project uses for anything that changes how the agent stack behaves, not just what it reports.

## Output format

```
## Learning Loop Review — {date}

Reviewed: {N} resolved entries, {M} still open (skipped)

| Date | Top hypothesis | Confidence | What happened | Score |
|---|---|---|---|---|
| ... | ... | ... | ... | Hit / Miss / Partial |

Pattern: {one or two sentences on what the scores have in common, if anything}

Proposed CLAUDE.md update: {one concrete, single edit}
```

## Worked example (simulated — no real outcome-log.md exists yet)

*`outcome-log.md` doesn't have any resolved entries yet — no diagnosis has been triggered and confirmed in production. This demonstrates the loop actually produces a sensible review, not just a template, using three constructed entries.*

**Simulated input:**

| Date | Top hypothesis | Confidence | What actually happened |
|---|---|---|---|
| 2026-09-15 | Push notification delivery issue | 8/10 | Confirmed — APNs delivery delay from a config change, ~40% of pushes delayed 6+ hours |
| 2026-08-28 | New user cohort quality shift (channel mix) | 6/10 | Ruled out internally — traced instead to a competitor (Duolingo) running a aggressive win-back promo the same week, pulling marginal users away before Day-7 |
| 2026-08-14 | Push notification delivery issue | 7/10 | Partially confirmed — delivery was delayed, but a concurrent streak-reset copy change (shipped the same day) also contributed; both mattered |

**Review:**

```
## Learning Loop Review — 2026-09-17

Reviewed: 3 resolved entries, 0 still open (skipped)

| Date | Top hypothesis | Confidence | What happened | Score |
|---|---|---|---|---|
| 2026-09-15 | Push notification delivery issue | 8/10 | Confirmed - APNs delay, 40% of pushes delayed 6+ hrs | Hit |
| 2026-08-28 | Cohort quality shift (channel mix) | 6/10 | Actually a competitor promo pulling users away | Miss |
| 2026-08-14 | Push notification delivery issue | 7/10 | Push delay confirmed, but a concurrent copy regression also contributed | Partial |

Pattern: the one clean miss wasn't a bad call given the evidence available - it was a cause the
hypothesis set never had a slot for at all. generate_hypotheses() only scores internal signals
(push delivery, cohort/channel mix, deploy timing); nothing in it checks whether a competitor
made a move the same week, even though agents/competitive-pulse.md already tracks exactly that.

Proposed CLAUDE.md update: add a line to the Agent Stack section noting that before trusting
an Anomaly Agent diagnosis, cross-check 02-research/competitive-pulse-log.md for the same week -
one of three diagnoses so far missed a competitor promo entirely because nothing in the loop
looks outside Streakly's own data.
```

This is exactly the shape the real review will take once `outcome-log.md` has real resolved entries — re-run this prompt for real the first time an Anomaly Agent diagnosis actually gets confirmed, rather than treating this simulated pass as a substitute for it.
