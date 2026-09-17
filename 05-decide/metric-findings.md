# Metric Findings — Streakly Comeback Screen

*Source: `data/users.csv`, `data/retention.csv`, `data/sessions.csv`, `data/comeback_sends.csv`. Column names used exactly as they appear in the files. A fifth file, `data/nudges.csv`, also exists in the folder but wasn't part of the four requested questions, so it isn't used below.*

**Design note found in the data, before the results:** `variant` in `users.csv` is blank for `cohort_week` 1–4 and only set to `comeback`/`control` for `cohort_week = 5` (50/50 split). So this isn't one continuous rollout — it's four unsplit cohorts followed by a single randomized A/B test in week 5. That shapes how Q1 and Q3 below need to be read together, not separately.

## Q1: Day-7 retention by cohort_week

```sql
SELECT cohort_week,
       AVG(CASE WHEN day_7 = 'true' THEN 1 ELSE 0 END) AS day_7_retention_rate,
       COUNT(*) AS n
FROM retention
GROUP BY cohort_week
ORDER BY cohort_week;
```

| cohort_week | day_7_retention_rate | n |
|---|---|---|
| 1 | 0.370 | 100 |
| 2 | 0.370 | 100 |
| 3 | 0.310 | 100 |
| 4 | 0.270 | 100 |
| 5 | 0.610 | 100 |

**What it means for scaling:** Weeks 1–4 are flat-to-declining (37% → 27%) — consistent with the original problem statement (Day-7 retention eroding). Week 5 jumps to 61%, but **week 5 blends both the comeback and control arms together** — it is not, by itself, evidence the feature works. It's the first sign something changed for that cohort; Q3 is what actually isolates why.

## Q2: Day-7 retention for `broke_streak_week1 = true` vs `false`

```sql
SELECT broke_streak_week1,
       AVG(CASE WHEN day_7 = 'true' THEN 1 ELSE 0 END) AS day_7_retention_rate,
       COUNT(*) AS n
FROM retention
GROUP BY broke_streak_week1;
```

| broke_streak_week1 | day_7_retention_rate | n |
|---|---|---|
| false | 0.458 | 310 |
| true | 0.268 | 190 |
| **gap** | **19.0 points** | |

**What it means for scaling:** Yes — this confirms the core premise directly in the data, independent of the experiment. Users who break their streak in week 1 retain 19 points worse at Day-7 than users who don't (26.8% vs 45.8%). This is the exact population the Comeback screen targets, and it's the same magnitude of problem the original decision brief was built on — the data matches the diagnosis before we even look at whether the fix works.

## Q3: Week-5 Day-7 and Day-30 by variant (comeback vs control)

```sql
SELECT u.variant,
       AVG(CASE WHEN r.day_7  = 'true' THEN 1 ELSE 0 END) AS day_7_retention_rate,
       AVG(CASE WHEN r.day_30 = 'true' THEN 1 ELSE 0 END) AS day_30_retention_rate,
       AVG(CASE WHEN r.churned = 'true' THEN 1 ELSE 0 END) AS churn_rate,
       COUNT(*) AS n
FROM retention r
JOIN users u ON u.user_id = r.user_id
WHERE r.cohort_week = 5
  AND u.variant IN ('comeback', 'control')
GROUP BY u.variant;
```

| variant | day_7_retention_rate | day_30_retention_rate | churn_rate | n |
|---|---|---|---|---|
| comeback | 0.760 | 0.360 | 0.260 | 50 |
| control | 0.460 | 0.220 | 0.540 | 50 |
| **lift** | **+30.0 points** | **+14.0 points** | **−28.0 points** | |

Two-proportion significance check (comeback vs control, n=50/arm):
- Day-7: z = 3.08, p = 0.002 — **significant**
- Day-30: z = 1.54, p = 0.123 — **not significant at conventional thresholds**
- Churned: z = 2.86, p = 0.004 — **significant**

**What it means for scaling:** This is the randomized comparison that actually isolates the feature's effect — same cohort, same signup week, split only by variant. The Day-7 lift (+30 points) and the churn reduction are large and statistically significant even at n=50 per arm. That's a strong early signal. **The Day-30 lift is directionally positive (+14 points) but not statistically significant yet** — at this sample size, we can't yet claim the effect holds a full month out, only that it doesn't reverse. Recommendation: don't read this as "ship to 100% immediately" — read it as "the Day-7 mechanism clearly works, run it longer or larger before betting the Day-30 story on it too."

## Q4: comeback_sends.csv open rate by send_number, comeback vs control

```sql
SELECT send_number,
       variant,
       AVG(CASE WHEN opened = 'true' THEN 1 ELSE 0 END) AS open_rate,
       AVG(CASE WHEN acted_on = 'true' THEN 1 ELSE 0 END) AS acted_on_rate,
       COUNT(*) AS n
FROM comeback_sends
GROUP BY send_number, variant
ORDER BY send_number, variant;
```

| send_number | variant | open_rate | acted_on_rate | n |
|---|---|---|---|---|
| 1 | comeback | 0.28 | 0.16 | 50 |
| 1 | control | 0.04 | 0.00 | 50 |
| 2 | comeback | 0.38 | 0.12 | 50 |
| 2 | control | 0.04 | 0.00 | 50 |
| 3 | comeback | 0.46 | 0.12 | 50 |
| 3 | control | 0.04 | 0.00 | 50 |
| 4 | comeback | 0.56 | 0.28 | 50 |
| 4 | control | 0.04 | 0.00 | 50 |

**What it means for scaling:** Two findings here, and one is a genuine surprise.

1. **Comeback vastly outperforms control at every send** (28–56% open rate vs a flat 4% for control across all four sends). Whatever control users received, almost nobody engaged with it — the contrast alone supports scaling over doing nothing.
2. **Open rate climbs with each successive send for the comeback variant (28% → 38% → 46% → 56%), and the increase from send 1 to send 4 is itself statistically significant (z = 2.84, p = 0.005).** This directly contradicts the notification-fatigue concern raised in the original NPS research ("got three in one afternoon and just turned them all off"). Here, later reminders perform *better*, not worse — and `acted_on_rate` also jumps on send 4 specifically (28%, versus 12–16% on sends 1–3). That send-4 pattern is worth a follow-up question before scaling the full 4-send cadence as-is: is it a genuine "last chance" effect, or an artifact of this cohort/sample size? Not answerable from this data alone.

## Overall recommendation

The data supports moving forward, with one condition. The causal evidence (Q3, randomized) and the engagement evidence (Q4) both clear a real statistical bar at Day-7, and Q2 confirms the underlying problem this feature targets is real and roughly the size the decision brief described. The one thing that isn't yet proven is durability past Day-7 — Day-30 is directionally right but not significant at n=50/arm. **Recommendation: scale the send cadence and Comeback screen past week 5, but treat Day-30 retention as an open question to keep measuring, not a result to report as settled.**
