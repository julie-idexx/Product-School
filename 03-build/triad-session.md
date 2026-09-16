# Triad Working Session — Streakly Comeback Screen

Prep: [`pm-brief.md`](pm-brief.md), [`prototype/index.html`](prototype/index.html), [`hypothesis.md`](hypothesis.md), [`change_log.md`](../change_log.md). 30 minutes, Raj (eng) + Lena (design).

## 1. Agenda

**Goal for this session:** not "get feedback" — that's already happened across three rounds (build-interview decisions, the P3L2a agentic interview, the codebase-tour exercise). The goal is to leave with a **build-scope decision**, not another round of opinions.

| Time | Segment | What happens |
|---|---|---|
| 0–5 min | **Why we're here** | One-slide recap: Day-7 retention 48%→39%, ~80% of lapsed users never return, three research methods converged on "post-lapse recovery is the unclaimed white space." State the hypothesis out loud. |
| 5–13 min | **Live walkthrough** | Click through all three states in the browser: Comeback screen → freeze toggle → 2-card lesson → completion screen (with the 3-stat row). Narrate the decisions already made and why (prospective-only freeze, one screen not a wizard, lifetime-lessons stat added after Tom/Amara's "still feels like starting over" feedback). Don't re-open decisions that are already made — flag them as *closed* so the room knows what's still actually open. |
| 13–25 min | **Targeted discussion** | Raj and Lena each get dedicated time on the specific open questions below — not a general "thoughts?" |
| 25–29 min | **Decide** | Walk through the "Decisions to leave with" list. For each: decided now, or assigned an owner + date to decide. Nothing leaves this meeting unresolved *and* unowned. |
| 29–30 min | **Next steps** | Who writes the spec/ticket, who's on point for the experiment design, when's the next checkpoint. |

## 2. What to show

- The prototype itself, live in a browser — not screenshots. Click through the real interaction, including the freeze toggle and both lesson-answer states (correct green, incorrect neutral gray).
- The one-sentence hypothesis: *"We believe the Comeback screen will deliver a measurable recovery in the ~80% of lapsed users who currently never come back, as measured by Day-7 retention rate."*
- The single most-cited research finding: **content was never the complaint** — every piece of negative feedback (interviews, NPS, competitive gap) is about the mechanics and tone around a lapse, not the lessons.

## 3. Questions to ask

**For Raj (engineering feasibility):**
1. Do we already store a per-user "best streak ever" and a lifetime lesson-completion count, or is either a new field/instrumentation we need to request?
2. How do we currently detect "this user just came back after N missed days" — a batch job, or a lazy check on next login? Does it respect each user's own day-boundary/timezone setting?
3. What's the blast radius of hooking a Comeback trigger into whatever already resets streaks? Is that reset logic isolated, or does it share a pass with other state (XP, notifications, etc.) the way it easily could?
4. Is "bank a freeze for next time" a new persisted concept, or is there something adjacent (a flag, a notification-preference-style field) we could extend instead of building from scratch?
5. Rough sizing: what would a flagged, A/B-testable v1 take — and is there a cheaper slice (e.g., stat + lesson only, freeze later) that gets us a testable version faster?

**For Lena (design):**
1. Does the 3-stat completion screen (Day 1 / Best streak / Lifetime lessons) hold up visually with real data — longer numbers, other languages, other tracks (guitar/coding/chess, not just language vocab cards)?
2. Copy check: does "Today restarts your streak — but it doesn't restart you" and the rest of the coach-not-scorekeeper tone match Streakly's actual brand voice, or is this PM's placeholder copy that needs a real pass?
3. Any concern with the visual approach (styled against IDEXX's Spot Mantine tokens for this exercise) versus whatever Streakly's actual design system is — is this close enough to prototype from, or does it need to be redone before dev even starts?
4. How should this screen visually signal "this is a different moment" versus the normal home screen, so it doesn't read as a bug or a glitch to a returning user?

## 4. Decisions we need to walk out with

1. **Build scope for v1** — ship stat + lesson + freeze together, or phase the freeze separately if it's the more expensive piece?
2. **Lapse-detection approach** — reuse existing reset/cron-style logic, or build an isolated check? (This was flagged as *the* engineering fork-in-the-road in the codebase-tour exercise — it needs an answer before a ticket can be sized.)
3. **Data readiness** — is "lifetime lessons completed" available now, or is it a blocking dependency that needs its own ticket first?
4. **Design sign-off status** — is the current direction (copy + visual approach) approved to build against, or does it need a revision pass before engineering starts?
5. **Next owner** — who writes the PRD/engineering ticket and the experiment design (guardrail metrics, sample size), and by when?

---

## Post-session alignment doc (template)

*Copy this section into a new doc/message immediately after the session, while it's fresh. Fill in every row — an empty row means something didn't actually get decided.*

**Session:** Streakly Comeback Screen — Triad Working Session
**Date:**
**Attendees:**

### Decisions made

| # | Decision | Owner | Notes |
|---|---|---|---|
| 1 | Build scope for v1 | | |
| 2 | Lapse-detection approach | | |
| 3 | Data readiness / dependency | | |
| 4 | Design sign-off status | | |
| 5 | Next owner for spec + experiment design | | |

### Open questions (decided later, not now)

| # | Question | Owner | Due |
|---|---|---|---|
| | | | |

### Risks / concerns raised

| # | Risk | Raised by | Severity |
|---|---|---|---|
| | | | |

### Action items

| # | Action | Owner | Due date |
|---|---|---|---|
| | | | |

### Next checkpoint

**Date/format:**
**What needs to be true by then:**

---

## Invite message

> **Streakly Comeback screen — 30 min working session**
>
> Hi Raj, hi Lena — I'd like 30 minutes with both of you to walk through the Comeback screen prototype and leave with a build-scope decision, not another round of feedback.
>
> Quick context: Day-7 retention dropped 48% → 39% after the v2 redesign, and it's concentrated in users who break their streak in week 1 — roughly 80% of them never come back. Three research methods (interviews, NPS, competitive analysis) converged on the same fix, and I've now run it through a build interview and two rounds of usability testing.
>
> In the session I'll do a live walkthrough of the prototype, then I have specific questions for each of you — Raj, on feasibility and where this hooks into our existing streak-reset logic; Lena, on whether the current copy and visual direction are far enough along to build against. Full agenda and prep docs are here: `03-build/triad-session.md`.
>
> No prep needed beyond glancing at the prototype (`03-build/prototype/index.html`) if you have five minutes before we meet — otherwise I'll walk through it live.
>
> Proposing [DATE/TIME] — let me know if that doesn't work.
