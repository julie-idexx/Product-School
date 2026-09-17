# Metric Diagnosis — Streakly Day-7 Retention

*Follow-on to [`05-decide/metric-findings.md`](../05-decide/metric-findings.md). All numbers below are freshly queried from `data/*.csv`, not restated from the earlier doc.*

## 1. Metric tree — what actually moves Day-7 retention

```
Day-7 Retention
│
├─ Streak-Start Rate            (users.csv: goal_set_date present)
│    → 100% in every cohort, every week. Everyone sets a goal.
│    → NOT a lever here — it never varies, so it can't explain any
│      of the movement we see in Day-7 retention.
│
├─ Streak-Break Rate, Week 1    (broke_streak_week1)
│    → wk1: 26%  wk2: 39%  wk3: 45%  wk4: 35%  wk5: 45%
│    → THE primary driver of the weeks 1–4 decline (see §2).
│    │
│    └─ Recovery Rate | Broke   (day_7 retention among broke=true)
│         → flat ~23% across weeks 1–4 (no recovery mechanism existed yet)
│         → wk5 target population (broke=true): comeback 50% vs control 28%
│           (directionally the mechanism working, not yet significant — see §3)
│
├─ Retention Rate | Never Broke (day_7 retention among broke=false)
│    → wk1: 42%  wk2: 46%  wk3: 36%  wk4: 29%  wk5: comeback 93% / control 64%
│    → A SECOND, independent driver of the weeks 1–4 decline, not explained
│      by the break-rate lever at all (see §2).
│
├─ Comeback Engagement Rate     (comeback_sends: opened / acted_on; sessions: screen='comeback')
│    → Does not exist before wk5 — no mechanism to engage with.
│    → wk5 comeback arm: ~92% open at least one send, ~50–57% act on at least one.
│    → Exposure alone does not differentiate outcomes (see §4) — opening the
│      send is not where the effect comes from.
│
└─ Notification Opt-In Rate
     → Not present as a field in any of the four tables. Cannot be decomposed
       from this data — if this lever matters, it needs its own column.
```

## 2. What caused the decline in weeks 1–4 — specifically

Two separate, additive causes, not one:

**Cause 1 — Streak-break rate nearly doubled.** `broke_streak_week1` rose from 26% (week 1) to 45% (week 3), dipping to 35% in week 4. Broken-streak users retain far worse regardless of week (~23% flat), so simply having more of them each week drags the blended number down. This alone explains most, but not all, of the decline.

**Cause 2 — Users who never broke their streak also retained worse over time, and this is not explained by more breaking.** Day-7 retention *among users who kept their streak intact* fell from 41.9% (week 1) to 45.9% (week 2) to 36.4% (week 3) to 29.2% (week 4) — a real, independent decline inside the "successful" population. Ruled out as explanations, directly from the data: acquisition-channel mix is nearly identical across cohorts 1–4 (organic/paid/referral each ~33–34% every week), platform mix is flat (60/40 iOS/Android every week), and session volume/duration per user is flat (~3.2 sessions/user, ~230–240 seconds/session across all four weeks). None of those shifted, so none of them explain it.

**Honest limit:** the specific mechanism behind Cause 2 isn't identifiable from `users.csv`, `retention.csv`, `sessions.csv`, or `comeback_sends.csv` alone — there's no column here that tracks notification tone, cadence, or app version. It's consistent with the same v2 streak/notification redesign already named as the trigger for the original 48%→39% drop (these four cohorts run April 6–27, 2026, immediately before the week-5 experiment), but that's contextual, not something these four tables prove on their own.

## 3. What week-5 treatment vs. control tells us about what the Comeback screen actually fixed

Splitting week 5 by the population the feature is actually designed for changes the story from the blended number:

| Population | Metric | comeback | control | gap | significance |
|---|---|---|---|---|---|
| **Broke streak (the target population)** | day_7 | 50.0% (10/20) | 28.0% (7/25) | +22.0 pts | p = 0.130 (not significant at n=20/25) |
| | day_30 | 30.0% (6/20) | 12.0% (3/25) | +18.0 pts | not tested (n too small) |
| **Never broke streak** | day_7 | 93.3% (28/30) | 64.0% (16/25) | +29.3 pts | **p = 0.007 (significant)** |

This is the honest, specific finding, and it cuts against the simple story: **the strongest, most statistically confident effect in the entire dataset is happening in the population the feature isn't designed to touch at all** (users who never broke their streak, so the Comeback screen never fires for them by design). The effect on the actual target population — people who broke their streak and were shown the recovery mechanism — is directionally right (+22 pts) but doesn't clear significance yet at this sample size.

Checked and ruled out as an explanation: pre-existing imbalance between arms. Platform, acquisition channel, and average pre-break `current_streak` are all closely matched between the comeback and control arms within the never-broke subgroup (e.g., avg streak 12.57 vs 12.36). This isn't an obvious randomization failure on the columns available.

What this leaves as the live question: either (a) simply knowing a safety net exists reduces anticipatory anxiety and improves engagement even for users who never need it — which would directly match the interview research's "single most important insight" (Amara's dread of losing her streak before she'd ever broken it) — or (b) this is a small-sample artifact (n=25–30 per group) that won't hold at scale. **The data as it stands supports the mechanism working on its target population but doesn't yet prove it at a statistically confident level — the confident result is arguably a side effect, not the main effect.**

## 4. Four ranked hypotheses — why some treated users still churned

*Grounded in the week-5 comeback-arm split: 13 users churned despite treatment, 37 retained. Both groups opened at least one send at the same rate (92% each) and visited a comeback-screen session at nearly the same rate (85% vs 84%) — exposure does not separate them. What does separate them is below.*

### H1 — Acquisition-channel / intent mismatch
**Testable prediction:** "Users acquired via paid or referral channels who break their streak and see the Comeback screen will still churn at a meaningfully higher rate than organic users who see the same screen, because their initial motivation to build the habit was lower going in — the screen can't compensate for that."
- **Likelihood rank:** 1 (highest)
- **Confidence: 7/10** — the split is stark and directly visible with no extra assumptions: 92% of churned-despite-treatment users are paid/referral vs. only 8% organic, while retained users are 43% organic — nearly the mirror image. n=13 is small, but the pattern is large and specific, not a marginal lean.
- **Confirms it:** At a larger sample, organic streak-breakers who see the Comeback screen retain significantly better than paid/referral streak-breakers who see the same screen, holding open/acted-on rates constant.
- **Rules it out:** At scale, organic and paid/referral streak-breakers who see the Comeback screen retain at statistically indistinguishable rates — meaning this channel split in the n=13 sample was noise.

### H2 — Engagement without conversion
**Testable prediction:** "Users who visit the comeback screen session multiple times but never open a 'lesson' screen session afterward will churn at a much higher rate than users who move from comeback-screen view into an actual lesson session."
- **Likelihood rank:** 2
- **Confidence: 6/10** — directly supported by two independent signals: churned users' sessions skew toward the `comeback` screen itself (39% of their sessions vs. 28% for retained) and away from `lesson` (18% vs. 23%), and 77% of churned users (10/13) end at `current_streak = 0` — meaning for most of them, the restart mechanically never happened.
- **Confirms it:** Among treated users, day-7 retention for "viewed comeback screen, then later opened a lesson session" is dramatically higher than "viewed comeback screen, never opened a lesson session."
- **Rules it out:** Churned users who *did* have a completed `lesson` session logged still ended at `current_streak = 0` at the same rate as those who never opened one — meaning the break isn't at the view→lesson step, it's somewhere after lesson completion.

### H3 — No freeze banked before a second lapse
**Testable prediction:** "Users who opened at least one comeback_send but never acted on any of them will disproportionately churn if they lapse a second time, because they went into that second lapse with nothing banked — recreating the exact 'cold reset, nothing offered' experience the feature exists to fix."
- **Likelihood rank:** 3
- **Confidence: 4/10** — directionally consistent (46% of churned acted on at least one send vs. 57% of retained, an 11-point gap) but modest relative to n=13, and the available data has no field for a *second* lapse event — `broke_streak_week1` only captures the first one — so the specific "second lapse" mechanism in the prediction can't be confirmed or ruled out with what exists today, only the correlation with acting.
- **Confirms it:** A field capturing a second in-window lapse, cross-referenced with prior `acted_on` history, shows churn concentrated specifically in "opened but never acted, then lapsed again" users.
- **Rules it out:** At a larger sample, churn rates are statistically indistinguishable between "acted on at least once" and "never acted on" — the 11-point gap was noise.

### H4 — Pre-break streak length was too short to carry emotional weight
**Testable prediction:** "Among treated users who broke their streak, those with a shorter pre-break streak will churn at a higher rate after seeing the Comeback screen than those with a longer pre-break streak, because 'your record is still yours' means less when the record was short."
- **Likelihood rank:** 4 (lowest)
- **Confidence: 3/10** — plausible and consistent with the feature's own design logic (the best-streak stat is the core reassurance), but this dataset has no column for "streak length at the moment it broke" — only a single final `current_streak` snapshot and the binary `broke_streak_week1` flag. This one can't actually be tested with what's here; it's the weakest-evidenced of the four, not because it's wrong, but because there's no data point to check it against yet.
- **Confirms it:** A field for streak length at the moment of breaking shows churned-despite-treatment users had systematically shorter pre-break streaks than retained-despite-treatment users.
- **Rules it out:** Pre-break streak length is evenly distributed across churned and retained treated users.

## 5. Which one to test first

**H1 — acquisition-channel/intent mismatch.** Two reasons, together:

1. **It has the strongest existing evidence** (7/10, the sharpest and most specific pattern in the data) — prioritizing it isn't a guess, it's following the signal that's already loudest.
2. **It's the cheapest to test and the highest-stakes if true.** Confirming or ruling it out doesn't require building anything — it's a larger-sample re-run of a query that already exists. But the answer changes the whole strategy: if H1 holds at scale, no amount of UX polish on the Comeback screen (H2, H3) will move the needle for paid/referral users, and the real fix is either a different intervention for that segment or a hard look at whether that acquisition spend is buying durable users at all. Validating H1 first tells us whether H2/H3 are even worth a sprint, or whether we'd be tuning a screen that was never going to save that segment.
