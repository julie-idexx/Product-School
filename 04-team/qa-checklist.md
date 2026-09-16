# QA Checklist — Streakly Comeback Screen

*Reviewed against [`04-team/spec-readiness.md`](spec-readiness.md), [`03-build/prototype/README.md`](../03-build/prototype/README.md), and [`03-build/prototype/index.html`](../03-build/prototype/index.html).*

## 1. Edge case list

### Empty states
- User has never held a streak — no value exists for the best-streak card at all (not zero, absent).
- New user with zero lifetime lessons completed — does "47 lessons" become "0," and does the reassurance copy still make sense at zero?
- No lessons remaining in the user's track (track completed, or content exhausted) — what does "Start your comeback lesson" do with nothing to continue?
- User switched tracks (or their original track was removed/changed) since they last opened the app — which track's lesson does the Comeback screen continue?

### Edge data conditions
- Best streak of exactly 1 day — does "your progress is still here" read oddly attached to a 1-day record?
- User lapses twice within the same week. **Per `spec-readiness.md`, this is explicitly out of v1 scope — the Comeback screen should not trigger a second time.** The edge case to test isn't "what does it show," it's "does it correctly *not* show."
- Streak-freeze already banked from a prior visit (v2 concern, but worth pre-empting): does the toggle need an "already active" state instead of always defaulting to off?
- Underlying task/lesson data for "continue where you left off" is missing or was deleted.

### Timing scenarios
- Missed exactly one day — should sit below the trigger threshold; confirm the boundary is enforced at "2+ days," not "1+."
- Missed many days, weeks, or months — does "restart your streak" / best-streak framing still make sense for a long-dormant user, or does it need different copy at that distance?
- Time zone / day-boundary edge cases — "missed a day" needs to be relative to the user's own day-start setting, not a global UTC midnight, or users near the boundary get misclassified.
- Comeback screen shown "too late" — user already did today's lesson through the normal flow before the Comeback screen loads. Does it still show and create a duplicate/confusing lesson state?
- User backgrounds and reopens the app multiple times in one lapsed session — does the screen show once and stay dismissed, or reappear every time?

### Permission states
- Push notifications off — the re-engagement loop assumes a notification brings the user back; confirm the Comeback screen still triggers correctly on the next *organic* open with no dependency on a notification having fired.
- Background app refresh off (iOS) — if any lapse calculation depends on background processing, the app could show stale streak state on open.
- Push permission revoked mid-lapse — is there an in-app fallback (badge, banner) so a user without notifications still discovers this screen?

## 2. PM QA pass — `index.html`, screen by screen

| # | Check | Verdict | Blocking? |
|---|---|---|---|
| 1 | UI matches the agreed v1 scope (stat + lesson only, freeze deferred to v2 per `spec-readiness.md`) | **Fail** — the file still renders a fully functional freeze toggle (`#freeze-card`, `#freeze-toggle`) | **Blocks sign-off against the current spec** — scope mismatch, not a code defect. See PR comment below. |
| 2 | Best-streak stat handles a user with no prior streak | **Fail** — `best-streak-value` is hardcoded to "12 days" with no empty-state branch anywhere in the markup | **Blocks launch** — there's no empty-state design here to hand to engineering yet |
| 3 | Lesson content adapts when a track has no lessons left | **Cannot be determined** — two French vocabulary cards are hardcoded with no branching logic; there's no data source in a static file to test this against | Non-blocking for the prototype; needs an answer from the real content layer before backend work starts |
| 4 | Completing the lesson correctly shows Day 1 + preserved best streak + lifetime total together | **Pass** (for what a static mock can show) — verified by walking the flow: `finishLesson()` correctly renders all three stats together | — |
| 5 | Freeze toggle state is idempotent (can't be double-banked) | **N/A given #1** — shouldn't be tested for v1 at all. As built, the toggle is a plain boolean with no "already banked" guard | Flag as a **known issue for v2**, not a v1 blocker |
| 6 | Incorrect-answer feedback avoids punitive framing (coach, not scorekeeper) | **Pass** — `.option.incorrect` uses neutral gray, not a red/negative color, and reads "Not quite," not "Wrong" — matches the documented research-backed decision | — |
| 7 | Handles a user who already did today's lesson before this screen loads (the "shown too late" case) | **Fail** — no such state exists; the screen assumes it's always the first thing shown this session | **Blocks launch** if lapse-detection timing can't guarantee this never happens — needs an engineering answer on trigger timing, not just a UI fix |
| 8 | UI degrades gracefully if the Google Fonts request fails | **Pass** — `font-family` declarations include a generic `sans-serif` fallback after Roboto/Sora, so a blocked or offline font load doesn't break the layout | — |
| 9 | Completion screen's 3-stat row holds up with longer/localized numbers | **Fail risk, not yet tested** — column widths and font size were already tightened to fit three short values (per `change_log.md`); a real value like "1,247 lessons" wasn't tested and has a real overflow/wrap risk | Non-blocking for the demo; needs a design QA pass with production-realistic numbers before launch |
| 10 | Feature fails gracefully without a network connection | **Pass, for the wrong reason** — the file has zero network calls, so it can't fail from a network dependency it doesn't have. **This tells us nothing about how the real, data-backed feature behaves offline.** | Flag as **cannot be determined for the real feature** — retest once it's wired to real data |

**Summary:** 3 blockers (#1 scope mismatch, #2 no empty state, #7 no "already engaged today" handling), 1 deferred-not-blocking known issue (#5), 2 "cannot determine from a static file" items that need answers before backend work starts (#3, #10), 1 needs a follow-up design pass (#9).

## 3. First PR comment for Raj

> Quick question before I sign off — `spec-readiness.md` has us cutting the streak-freeze to v2, with just the best-streak stat and lesson shipping in v1. This PR still has the full freeze toggle wired up and functional end-to-end. Is that intentional — building it now behind a flag so v2 is a fast follow — or should this PR's scope actually match v1 only?
>
> If we *are* keeping it in for now: I don't see anything handling what happens if a user toggles the freeze on while offline — does that bank client-side and sync later, or fail silently? Not asking you to solve it in this PR, just want to make sure it doesn't become a silent gap the way the double-lapse case almost did before we caught it.
