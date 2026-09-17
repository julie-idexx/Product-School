# Objection Log — Streakly Comeback Screen PRD

*Pressure-testing [`docs/prd.md`](prd.md) against three reviewers in sequence: Raj and Marcus in character per their stakeholder profiles, then Tom, the churned user the whole initiative is built around.*

## 1. Raj (engineering)

**Q1 — "Where did the measurement plan go?"**
"We already agreed on this — intent-to-treat vs. treated-subgroup, so a real effect doesn't get diluted by users the feature never touches. That's in `spec-readiness.md`. This PRD's Success Metrics section just says 'Day-7 retention among users who broke a streak.' Is that shorthand for the split we agreed on, or did it get flattened back into one number? I need it written down, not implied — I'm not re-having the dilution argument after this ships."

**Q2 — "You're still shipping an open question I already asked."**
"I asked what happens for a user who's never set a streak before there was even a PRD. The double-lapse case got answered — documented, out of scope for v1, clean. The 'no prior streak' case is still just sitting in Open Questions, unresolved. I'm not scoping a sprint around an undefined case. Either give me the behavior or tell me whose desk it's blocked on — Lena's or mine — because right now it's nobody's."

## 2. Marcus (Head of Product)

**Q1 — "Still no date."**
"I asked for a rollout timeline before I'd commit to Q3. This document doesn't have one — no date, no lift threshold, nothing that tells me when I get an actual answer instead of another open question. I don't need the PRD to solve that, but I need to know where it's being solved and by when."

**Q2 — "What does the excluded segment cost me?"**
"Non-Goals says users who lapse twice in the same week get nothing in v1. Fine — that can be a real scoping choice. But nobody's told me how many of our actual lapsed users that is, or what it costs on the Day-7 number I report up. Don't hand me a scope cut without the number attached to it."

## 3. Tom (churned user — 12-day streak lost, switched to Duolingo)

**Q1 — "My streak still says zero. What actually changed?"**
"Okay, so I open the app and it shows me I had 12 days, gives me a lesson, tells me I'm 'back in.' Fine. But my streak? Still zero. You're telling me the counter still resets — it's just got a nicer screen standing next to it now. That's not nothing, but it's not what made me quit either. What made me quit was the reset itself, and the reset is still happening."

**Q2 — "The one thing that would've actually saved me isn't even here."**
"The freeze — the thing that protects you *next* time — that's what I wanted. That's the whole reason I switched to Duolingo, because at least there a missed day doesn't wipe everything. And that's not in this version. It's pushed to v2. So walk me through it: I come back, I do the lesson, I feel good for a day — and then I miss two days again next month. What happens then? Do I just end up right back here, doing this exact same thing over again?"

## Verdict — which objection kills the initiative if unaddressed

**Tom's second question.** Raj's and Marcus's objections are real, but they're both process gaps in the document — a missing citation, a missing date. Both are fixable by editing the PRD before the next review; neither one says the feature doesn't work.

Tom's does. He's not asking for a cleaner spec — he's asking whether v1 actually closes the specific, well-evidenced gap the whole decision brief was built on (`competitive-matrix.md`'s "White Space for Streakly": nobody offers real post-lapse recovery, and pre-lapse protection is table stakes everywhere else). Deferring the freeze to v2 means v1 gives Tom a nicer moment of acknowledgment, but not the actual mechanism he named as the reason he left. If v1 ships without it and a Tom-shaped user lapses a second time with nothing new to show for it, the read isn't "this feature needs a data-model fix" — it's "this didn't work for the person it was supposed to be for," and that's the kind of result that gets an initiative killed on outcomes, not on paperwork. Raj's and Marcus's gaps can be fixed by Thursday. Tom's is a bet on whether v1 alone is enough, and right now the PRD doesn't argue that case — it just defers the part of the fix he'd recognize as the fix.
