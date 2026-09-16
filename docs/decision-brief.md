# Decision Brief: Streakly Comeback Experience

**To:** Marcus, Head of Product
**From:** PM, Engagement squad
**Date:** 2026-09-14

## Situation

Day-7 retention dropped from 48% to 39% since the v2 streak/notification redesign, concentrated almost entirely in users who break their streak in week 1 and never return. Three independent discovery methods — user interviews, NPS feedback, and competitive research — have now converged on the same root cause and the same gap in the market.

## Customer Impact

- **Day-7 retention has dropped 9 points (48% → 39%)** since the v2 redesign shipped — the single biggest metric move tied to that launch.
- **Once a user misses two consecutive days, roughly 80% never return.** A broken streak isn't a dip in engagement — for most users, it's close to a permanent loss event.
- **The failure point is consistent across every source.** All 3 interview subjects and 8 of 10 NPS comments describe the same thing: the reset, not the content. Nobody in either dataset complained about the lessons themselves — the praise that does exist is specifically about lesson quality ("Love the lessons," "the first week was genuinely fun").
- **Real examples of the mechanism in action:** Tom (5 weeks in, proud of a 12-day streak) uninstalled after missing two days on a work trip and getting no way back in. A separate NPS respondent deleted the app after 3 weeks for the same reason: "the moment I lost my streak the whole thing lost its meaning."
- **This is a concentrated leak, not a broader growth problem.** It's happening against a backdrop of otherwise healthy growth — 2.1M registered users, 340K MAU, 28% YoY MAU growth — which means the fix is scoped to the week-1 experience, not the whole product.

## Key Findings

1. **Streak resets read as punishment, not motivation, across every research method.** Tom (churned) and Amara (day 4) in the interviews, plus 4 of 10 NPS comments, independently describe the reset in the same terms — "punishing," "pointless to start over," "start from scratch," "lost its meaning." This is convergent evidence, not a single anecdote.
2. **Fear of losing the streak starts before it's even broken.** Amara is only 4 days in and already anxious about missing a day — the week-1 problem includes anticipatory dread, not just the aftermath of an actual break (interview synthesis).
3. **Users are explicitly asking for what the category already ships.** 3 of 10 NPS comments and Tom's interview name a missing streak freeze; Duolingo, Babbel, Elevate, and Brilliant all already ship some form of pre-lapse protection (freeze, charge, or skip allowance). On this dimension, Streakly is behind the category baseline, not ahead of it.
4. **The real white space is what happens after a break — nobody solves that well.** Post-lapse recovery is nearly empty across all 5 competitors researched; only Duolingo has anything (a generic, one-time 2026 marketing campaign, not a personalized flow). Building a graceful comeback experience isn't just closing a competitive gap — it would be a genuine differentiator.
5. **Notification tone is actively working against retention, not just failing to help.** Tom's account of a harsh "you lost your streak" push, plus 2 of 10 NPS comments on notification fatigue ("got three in one afternoon and just turned them all off"), show the current re-engagement channel is compounding the problem it's meant to solve.

**Flag on sourcing:** a fourth source — Reddit sentiment on these competitors — was planned to cross-validate the competitive research, but couldn't be obtained (WebSearch and direct fetch tools were unable to access reddit.com in this environment). The findings above rest on user interviews, NPS feedback, and structured competitive research only, and have not been independently checked against public Reddit discussion.

## Options Considered

1. **Do nothing / monitor.** Let the v2 redesign settle and see if Day-7 recovers on its own. Lowest cost, but ignores three converging sources of evidence pointing at a specific, addressable cause, and does nothing about an ~80% permanent-loss rate on the specific event driving the drop.
2. **Add a streak freeze only.** Closes the competitive gap (matches Duolingo/Babbel/Elevate/Brilliant). But per the competitive matrix, a freeze alone is table stakes, not a differentiator — and it doesn't help users who've already hit zero, which is where the interview and NPS complaints are concentrated.
3. **Build the full Comeback experience** (best-streak stat + short comeback lesson + one-tap freeze). Addresses the reset-as-punishment theme, the "no recovery path" complaint, and the competitive white space at the same time. Most comprehensive option, and the only one that targets the post-break moment directly.

## Recommended Action

Move forward into scoping the Comeback experience (Option 3) as the lead hypothesis for recovering Day-7 retention.

## Why a New Engagement Tactic Is the Right Lever

Today, Streakly's entire model of stickiness rests on one mechanic: an unbroken streak. One NPS respondent said it plainly — "the streak is the only thing keeping me engaged, but the second I lost it, I was done." That's a single point of failure, and real life guarantees it breaks — Tom's own churn was triggered by a work trip, not by losing interest in the product itself.

Every competitor researched has already recognized this fragility and added a second layer of stickiness on top of the raw streak — a purchasable freeze, a banked charge, a skip allowance — because an all-or-nothing mechanic alone doesn't hold users through an ordinary interruption. Streakly doesn't have that second layer yet, which is likely why the failure mode shows up so cleanly and consistently across every dataset here: nothing currently catches a user between "streak intact" and "streak gone."

A new engagement tactic — the Comeback experience — doesn't replace the streak as a motivator; it adds a second, more resilient source of stickiness: recognition of progress that survives an interruption, not just progress that resets. That reframes a missed day from "you lost everything" to "your progress is still here, and there's an easy way back in" — converting what is currently a near-permanent loss event (~80% never return) into a recoverable one. Given the scale of that number, this is the single highest-leverage lever available for closing the Day-7 gap, not a nice-to-have on top of a freeze.

## Why Now

Interviews, NPS feedback, and competitive research all converge on the same cause and the same unclaimed white space at the same time discovery is already underway, with a fixed 8-week runway to sprint kickoff — and the competitive data shows a freeze alone (the cheaper option) would only bring Streakly to parity, not close the gap that's actually driving the ~80% permanent-loss rate behind the Day-7 drop.
