# Streakly Comeback Screen — Prototype

Open `index.html` in any browser. No build step, no dependencies.

## PM Brief

**Persona:** 24-year-old user who hit a 12-day streak, missed two days, and has not opened the app since.

**Job to be done:** Get back in without feeling they lost everything.

**Feature:** A personalized Comeback screen with a best-streak stat, one 60-second comeback lesson, and a one-tap streak-freeze offer.

**Constraint:** Use data Streakly already has. No new integrations.

This brief is grounded in three converging research sources — interview synthesis (Priya, Tom, Amara), NPS feedback analysis, and the competitive matrix — plus the decision brief Marcus approved. All three point to the same gap: every competitor protects users *before* a streak breaks (freezes, charges, skip allowances), but almost nobody helps once it's already broken. That's the moment this screen is designed for.

## Key decisions made during the interview

| Decision | What we chose | Why |
|---|---|---|
| **Streak-freeze mechanic** | Prospective only — banks a freeze that protects the *next* missed day. It does **not** retroactively restore the broken 12-day streak. | No competitor offers retroactive restoration; keeping it prospective closes the *post*-lapse gap (the actual white space) without overpromising on the *pre*-lapse mechanic everyone already ships. |
| **Best-streak stat** | A permanent record shown separately from the current streak, which restarts at 1 after the lesson. | Research: users want a "coach," not a "scorekeeper." Preserving the 12-day record as a visible, permanent badge — rather than erasing it — is what turns "you lost everything" into "your progress is still here." |
| **Comeback lesson content** | Continues the user's existing track (French · Basics) exactly where they left off. | Constraint is to use data Streakly already has — no special one-off content to build or maintain. |
| **Screen structure** | One screen. Best-streak stat, the lesson entry point, and the freeze toggle are all visible together. | Interviewee and NPS feedback both flagged that the app doesn't visibly adapt to a lapsed user's state — a single screen that surfaces everything at once (vs. a multi-step wizard) makes that adaptation immediate and legible. |
| **Lesson fidelity** | Simulated: 2 mock multiple-choice cards with feedback, then a completion state — not a straight jump to "done." | Demonstrates the actual 60-second lesson experience rather than just asserting it happened. |
| **Track for the demo** | Language learning (French). | Not specified in the original brief; simplest track to mock as multiple-choice. |
| **Visual design system** | IDEXX's brand palette (Clarity Blue `#0B76F0`, neutrals, Arial) as a stand-in. | IDEXX's internal **Spot** design system (the actual product component library) wasn't accessible in this environment — no local reference and no public documentation. This approximates the brand rather than reproducing Spot's actual components/tokens. If Spot assets become available, restyle against those directly rather than treating this palette as final. |

## Flow

1. **Comeback screen** — best-streak stat (12 days), "Start your comeback lesson" card, and a freeze toggle.
2. **Lesson** — 2 mock French vocabulary questions with immediate feedback (correct answers highlighted in Clarity Blue, incorrect answers shown neutrally rather than with a punitive red X, per the "coach not scorekeeper" research finding).
3. **Completion** — new streak starts at Day 1, best-streak badge (12 days) still visible, and confirmation that a freeze was banked if the user turned it on.

A "Restart demo" link on the completion screen resets state for repeat walkthroughs — it's a demo control, not part of the product UI.
