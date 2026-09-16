# PM Brief — Streakly Comeback Screen

## Source

Grounded in [`research/interview-synthesis.md`](../research/interview-synthesis.md), [`research/nps-analysis.md`](../research/nps-analysis.md), [`research/competitive-matrix.md`](../research/competitive-matrix.md), and [`docs/decision-brief.md`](../docs/decision-brief.md) (approved by Marcus).

## Persona

24-year-old user who hit a 12-day streak, missed two days, and has not opened the app since.

## Job to be done

Get back in without feeling they lost everything.

## Feature

Personalized Comeback screen:
- Best-streak stat
- One 60-second comeback lesson
- One-tap streak-freeze offer

## Constraint

Use data Streakly already has. No new integrations.

## Interview decisions

| Question | Decision |
|---|---|
| What does the streak-freeze offer do? | **Prospective only.** Banks a freeze that auto-protects the *next* single missed day. Does not retroactively restore the broken 12-day streak — no competitor offers retroactive restoration either, so this stays consistent with the category while closing the post-lapse gap nobody else covers. |
| What is the "best-streak stat"? | A **permanent record**, shown separately from the current streak counter. The current streak restarts at 1 after today's lesson; the best-streak badge (12 days) stays visible as proof of what they built — this is the "coach, not scorekeeper" reframe the research calls for. |
| What is the comeback lesson's content? | **Continues their existing track** from where they left off. No special "welcome back" content — uses progress data Streakly already has, per the no-new-integrations constraint. |
| Is this one screen or a multi-step flow? | **One screen.** Best-streak stat, "Start your comeback lesson" button, and a freeze toggle are all visible together — not a wizard. |
| How much of the lesson should the prototype simulate? | **Simulated.** 1–2 mock multiple-choice cards with feedback, then a completion/celebration state — not just a straight jump to "done." |
| Which track for the demo? | **Language learning** (not specified in the original brief; easiest to mock as a simple multiple-choice card). |
| Visual design system? | **IDEXX brand palette** (Clarity Blue, Arial, neutrals) as a stand-in — IDEXX's actual internal "Spot" design system/component library wasn't available in this environment, so this approximates the brand rather than reproducing Spot exactly. |
