---
name: friday-status
description: Run the recurring Friday status update for the Streakly Comeback work with a single trigger phrase and no additional input - gathers what shipped, what's in progress, and what's blocked directly from the workspace (git history, change_log.md, stakeholder profiles' open items) instead of requiring the user to dictate notes each time. Use whenever the user says something like "run my Friday status update," "do my weekly status for Streakly," or pastes the trigger phrase below. Hands the gathered material to the weekly-status skill for calibration and formatting rather than reinventing it.
---

# Friday Status Update (self-gathering)

**Trigger prompt** — paste this to run it:
> Run my Friday status update for Streakly.

## Why this is a separate skill from `weekly-status`

`weekly-status` turns notes someone already wrote into a clean, audience-calibrated update — but it still needs those notes handed to it. This skill exists so a Friday update can run from one paste with nothing dictated: it gathers the material itself from the actual state of the workspace, then hands off to `weekly-status`'s calibration and formatting rules rather than duplicating them. If `weekly-status` ever changes its rules, this skill inherits the change automatically.

## Steps to run, in order

1. **Establish the window.** Default to the last 7 days. If `status-updates.md` (see Output below) already has a prior entry, use its date as the start of the window instead — this keeps runs contiguous so nothing gets double-reported or silently skipped between weeks.
2. **Gather Shipped.** Run `git log --oneline --since="<window start>"` from the project root. Each commit message is already a real, human-written description of what changed — read them rather than re-deriving what happened from the diffs.
3. **Gather In Progress.** Check `change_log.md` for anything logged in the window that describes ongoing, not-yet-shipped work.
4. **Gather Blockers.** Re-read each stakeholder profile's "Open items" section fresh (`04-team/stakeholders/*.md`) — these change between runs, so don't rely on what a prior run found. Anything still listed there is a live blocker worth reporting.
5. **Calibrate and format.** Hand everything gathered above to the `weekly-status` skill: it defines the per-audience calibration (team vs. leadership) and the rule that a claim only gets reported if the workspace actually backs it up. Don't include anything in Shipped that the git log doesn't actually show.

## Output format

Two calibrated updates in the exact structure `weekly-status` defines — one for the team (Raj + Lena), one for leadership (Marcus).

## Where it's saved

Append as a new dated section to `status-updates.md` at the project root (create it if it doesn't exist). Newest entry goes at the top. Head each entry with the date and the exact commit range it covers, so the next run's "establish the window" step has something concrete to pick up from.
