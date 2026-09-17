# Streakly Comeback Screen — Results Memo

**To:** Marcus, Head of Product
**From:** PM, Engagement squad
**Recommendation, up front:** Scale the Comeback screen past the week-5 test — the data supports it, with one gap we should close before we call it proven.

## Situation

We shipped the Comeback screen — a best-streak stat and a 60-second lesson (the streak-freeze is deferred to v2) — to a randomized 50/50 test within the week-5 signup cohort, comeback vs. control. We were testing whether it recovers Day-7 retention specifically for users who break their streak in week 1, the exact population behind the 48%→39% drop.

## Evidence

- **Day-7 retention: comeback 76% vs. control 46% (+30 points, p = 0.002).** Isolated to the actual target population — users who broke their streak — it's 50% vs. 28% (+22 points, directionally right, not yet statistically significant at n=20/25).
- **Churn cut nearly in half: 26% vs. 54% (p = 0.004).**
- **Engagement flipped the old pattern:** comeback messaging is opened 28%→56% of the time across the four follow-ups (climbing, not fatiguing); the old approach sits flat at 4% the whole way through.

## Recommendation

Move the Comeback screen (stat + lesson, v1 scope) into Q3 as planned, and run one more cohort at a larger sample specifically on users who break their streak, before treating the target-population number as proven rather than promising.

## Ask

Approval to (1) proceed into the Q3 sprint at v1 scope, and (2) run a two-week extension at a larger sample to get the target-population read past the significance line — with a go/no-go on full rollout by the end of that window, not left open-ended.

## Risk if we wait

Every week without this, the ~80% of week-1 streak-breakers who currently never come back keep leaving at that rate, on a problem we've now shown a working, statistically significant fix for at the whole-cohort level.

---

## Marcus's three hardest questions

Stepping into character — skeptical Marcus, reading this memo before the meeting.

1. **"Fifty people per arm. That's the sample size you want me to take into a Q3 sprint conversation? Convince me this isn't noise before I bring it anywhere near the board."**

2. **"Walk me back through this — the number that actually clears significance is for users who never broke their streak in the first place. The ones we actually care about, the ones this whole feature is *for*, don't clear it yet. Why am I looking at a green number for the population that doesn't matter and a not-yet-proven number for the one that does?"**

3. **"You know I asked for a timeline before I'd commit to Q3. Give me the real one — not 'a couple more weeks,' an actual date I can hold you to — and tell me straight: what does it cost us if we wait for it instead of shipping now?"**
