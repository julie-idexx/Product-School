---
name: competitive-pulse
description: Run the recurring weekly competitive pulse check for Streakly with a single trigger phrase and no additional input - searches the web for anything new from Duolingo, Babbel, Elevate, Brilliant, and Streaks this week, cites every claim to a source, and flags whether it changes the white-space analysis in competitive-matrix.md. Use whenever the user says something like "run my competitive pulse check," "any competitor news this week," or pastes the trigger phrase below.
---

# Competitive Pulse Check

**Trigger prompt** — paste this to run it:
> Run my competitive pulse check for Streakly.

## Why this one needs live search, unlike the other two

`friday-status` and `research-synthesis` both gather from material already inside the workspace. This one can't — "what did competitors do this week" only exists out on the web, so this skill's first real step is search, not reading local files. That also means it's the one workflow here that can come back empty-handed through no fault of its own (a search that finds nothing, or a site that blocks the fetch) — see step 4.

## Steps to run, in order

1. **Read `02-research/competitive-matrix.md` first.** It has the current competitor set (Duolingo, Babbel, Elevate, Brilliant, Streaks) and what's already known about each — the pulse check should be targeted at what's *changed*, not a cold restart of the whole competitive study.
2. **Search each competitor for the last 7-14 days** — feature launches, pricing changes, app-store changelog highlights, notable press. One search per competitor is usually enough; widen only if the first pass is ambiguous.
3. **Filter for material changes.** A changelog line like "bug fixes and performance improvements" isn't a finding. A new streak mechanic, a pricing change, a new AI feature, a acquisition/funding move — those are.
4. **Cite every claim to its actual source URL.** No source, no claim — this matches how every other competitive claim in this workspace is already sourced. If a competitor's official channels can't be reached or a search comes back empty, say so plainly ("no notable changes found this week" or "couldn't verify — [reason]") rather than filling the gap with a guess. `competitive-matrix.md` and `docs/decision-brief.md` already disclose one such gap (Reddit access was blocked) — this skill should disclose its own the same way, not paper over it.
5. **Check against the white-space analysis.** `competitive-matrix.md`'s "White Space for Streakly" names two specific gaps (real post-lapse recovery, and a home screen that adapts to lapse state). If anything found this week closes either gap for a competitor, flag it explicitly — that's the one finding worth surfacing loudly, since it directly affects whether Streakly's differentiation still holds.

## Output format

A dated entry, one line per competitor: what changed (with a source link) or "nothing notable found," plus a closing line on whether anything found this week affects the white-space analysis.

## Where it's saved

Append as a new dated section to `02-research/competitive-pulse-log.md` (create it if it doesn't exist), newest entry at the top. If something closes a white-space gap, say so in the log entry and flag it — don't silently let `competitive-matrix.md` go stale against a finding that actually changes the analysis.
