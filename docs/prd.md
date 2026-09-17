# PRD — Streakly Comeback Screen

*Audience: Raj (engineering), Lena (design). v1 scope reflects the cut already agreed with Raj in `spec-readiness.md`.*

## Problem Statement

Day-7 retention dropped from 48% to 39% after the v2 streak/notification redesign, concentrated in users who break their streak in week 1; once a user misses two consecutive days, ~80% never return (`decision-brief.md`). Three independent research methods converge on the same failure point: the streak reset itself and its surrounding notification, not the lesson content — no source flags the lessons as a problem (`decision-brief.md`; `interview-synthesis.md`; `nps-analysis.md`). No competitor studied offers a real recovery path after a streak has already broken; every competitor's mechanic (freeze, charge, skip allowance) only prevents a break before it happens, never addresses one after the fact (`competitive-matrix.md`, "White Space for Streakly").

## User

A user who broke a multi-day streak in their first week and has not returned since — matches Tom's account (12-day streak, lost after a 2-day trip) and Amara's stated fear of the same outcome at 4 days in (`interview-synthesis.md`).

**Job to be done:** come back in after a break without the app treating it as starting from nothing. Tom: *"There was no way to recover it, nothing. So I gave up."* Amara: *"I don't want to lose everything I've built after four days."* (`interview-synthesis.md`)

## Goals and Non-Goals

**Goals**
- Show a lapsed user a permanent record of their best streak, separate from the reset counter (`interview-synthesis.md`, Theme 2; `nps-analysis.md`, "coach not scorekeeper").
- Give the user an immediate, low-friction way to resume the habit loop the same day they return (`decision-brief.md`, recommended action).
- Offer a streak-freeze that protects the user's *next* miss, closing the pre-lapse-protection gap every competitor studied already has and Streakly does not (`competitive-matrix.md`).

**Non-Goals**
- **v1 scope is best-streak stat + comeback lesson only. The streak-freeze is v2** — agreed with engineering (`spec-readiness.md`).
- Retroactively restoring the lost streak. No competitor studied does this (`competitive-matrix.md`).
- Serving users who lapse a second time within the same week. Explicitly out of scope for v1 (`spec-readiness.md`).
- Redesigning the re-engagement notification itself. Flagged as a related but separate problem — the notification's harsh tone is its own contributing cause, distinct from the reset mechanic this screen addresses (`interview-synthesis.md`, Theme 3; `nps-analysis.md`).

## Success Metrics

- Day-7 retention among users who broke a streak in week 1 — the specific population behind the 48%→39% drop (`decision-brief.md`).
- Hypothesis this feature is built to test: *"We believe that the Comeback screen ... will deliver a measurable recovery in the ~80% of lapsed users who currently never come back ... as measured by Day-7 retention rate."* (`hypothesis.md`)

## User Stories

1. As a user who broke my streak, I want to see my best streak preserved so that I don't feel like I'm starting from nothing. (`interview-synthesis.md`, Amara; `nps-analysis.md`)
2. As a returning user, I want a short lesson I can complete immediately so that I can restart my habit the same day I come back. (`decision-brief.md`)
3. As a returning user, I want the app to recognize I'm coming back after a lapse instead of showing the same generic home screen so that I feel the app knows where I am. (`nps-analysis.md`: "nothing acknowledges where I am"; `competitive-matrix.md`)
4. As a user reading the recovery screen, I want language that doesn't blame me for missing days so that coming back doesn't feel like being punished. (`nps-analysis.md`: "a coach ... not a scorekeeper that punishes me"; `interview-synthesis.md`, Tom: "that just made me feel bad")
5. *(v2)* As a user who just recovered, I want to bank a streak freeze for my next miss so that a single bad day doesn't cost me everything again. (`competitive-matrix.md`)

## Open Questions

- **`research/competitive-reddit.md` was listed as a source for this PRD but does not exist in the workspace.** `decision-brief.md` itself discloses this: Reddit cross-validation of the competitive research was planned but never obtained (tool access limitation). Every competitive claim above rests on structured research only (`competitive-matrix.md`), not independently checked against public sentiment.
- Whether the notification's tone/timing gets redesigned alongside this screen or is separate follow-on work — both `interview-synthesis.md` and `nps-analysis.md` name it as its own contributing problem, not resolved by this screen alone.
- Behavior for a user with no prior streak, or no lessons remaining in their track, is undefined in every research file reviewed for this PRD. Needs a design decision (Lena) and a data contract (Raj) before build.
