# project.md

*Skeleton draft from the Sept team Slack thread (Marcus, Raj, Lena) — starting point, not final. To be aligned on before Thursday's meeting.*

## What Streakly Is

Streakly is a consumer habit + micro-learning app. Users pick a track (languages, guitar, coding, chess), do a short daily lesson (5 minutes), and build a streak — the streak is the product's heartbeat, what turns "I downloaded an app" into "I show up every day."

Launched 4 years ago. Series B funded ($42M). 2.1 million registered users, 340,000 monthly active users, growing 28% YoY on MAU.

## My Squad

PM, Engagement squad — owns everything related to keeping users active in their first weeks: the home screen, the daily lesson loop, streak mechanics, and push notifications.

Triad: Raj (Senior Engineer), Lena (Product Designer), me (PM).

## Current Phase

Discovery — the Comeback experience. No designs, no committed scope. 8 weeks from sprint kickoff.

Acquisition is working (install → pick a track → finish first lesson), but a large share of new users break their streak in week 1, and once it's gone, most never come back.

## Key Stakeholders

- **Marcus** — Head of Product, I report to him. Wants to understand why Day-7 retention dropped and what to do about it.
- **Raj** — Senior Engineer, my triad. Owns technical feasibility (e.g., confirmed a Comeback screen concept is doable with existing data, flagged new logic needed for targeting/freeze rules).
- **Lena** — Product Designer, my triad. Owns the design direction and user research (sketched the initial Comeback screen concept, surfaced the "streak reset feels like punishment" insight).

## Problem Statement

Day-7 retention has dropped from 48% to 39% since the streak redesign shipped (Marcus).

The drop is sharpest among users who break their streak in week 1 — once someone misses two days in a row, churn is almost double (Raj).

User research shows why: people build a good streak, miss a day because life happens, and come back to a counter reset to zero. It feels like punishment, with no way back in (Lena). The "you lost your streak" push notification has a harsh tone, and after a user taps through, the app offers nothing — it just drops them back at day zero (Lena).

Open question raised by Marcus, not yet resolved: is the core problem the streak reset itself, or the notification nagging users right when they're most likely to quit — or both (Raj thinks likely both).

Working hypothesis: users go passive because breaking a streak feels like failure, and there's no graceful comeback. They need to be pulled back with a reason specific to their own progress, not a generic "keep going!"

## Goals

- Align the team on the problem itself before designing solutions (Marcus's ask, ahead of Thursday's meeting).
- Give users a graceful path back in after a broken streak, rather than a cold reset to zero.

## Non-Goals

- Not yet defining the solution in detail. Lena has sketched an early direction (a "Comeback screen" with a best-streak stat, a 60-second comeback lesson, and a one-tap streak freeze), and Raj confirmed it's technically doable with existing data sources — but Marcus wants problem alignment first, before designing solutions.
- Not yet decided: whether the fix targets the streak-reset mechanic, the notification tone/timing, or both.

## Success Metrics

- Day-7 retention: current baseline 39%, prior to redesign 48%. No specific recovery target has been set in the thread yet.
- Churn rate for users who miss two consecutive days in week 1 (currently ~2x baseline, per Raj) — a candidate metric to watch as this is defined further.

---
*Not yet filled in from this thread: Goal this quarter, Bet, Not doing (see orientation.md template) — to be completed after Thursday's alignment discussion.*
