# Streakly Comeback Screen — Quarterly Review Deck (6 slides)

*Backbone: [`docs/recommendation-memo.md`](recommendation-memo.md) and [`05-decide/metric-findings.md`](../05-decide/metric-findings.md). Every number and quote below traces to a source file — none invented.*

## Slide 1 — The Problem

**Headline number:** Day-7 retention dropped from **48% → 39%** since the v2 streak/notification redesign. (`decision-brief.md`)

**Headline insight:** Once a user misses two consecutive days, **~80% never return** — closer to a permanent-loss event than a dip. (`decision-brief.md`)

## Slide 2 — Why Now

- Problem alignment already happened — Marcus approved the decision brief tying this drop to the v2 redesign. (`decision-brief.md`)
- Since then: three independent research methods (interviews, NPS, competitive research) converged on the same fix — no competitor in the category offers real *post-lapse* recovery, only *pre-lapse* prevention. (`decision-brief.md`)
- We didn't stop at a hypothesis: we built it and ran it as a live randomized pilot. What follows is data, not a pitch. (`recommendation-memo.md`)

## Slide 3 — The Proposal

**What it is:** The Comeback screen — a best-streak stat and a 60-second lesson, v1 scope. (`recommendation-memo.md`)

**What it isn't:**
- Not retroactive restoration of the streak already lost — no competitor in the category does this. (`decision-brief.md`)
- Not a request to roll out to 100% today — the ask (Slide 6) is to keep validating at a larger sample first. (`recommendation-memo.md`)

## Slide 4 — Evidence

- **Pilot design:** a randomized 50/50 split, comeback vs. control, within the week-5 signup cohort. (`recommendation-memo.md`)
- **User voice:** Tom — *"There was no way to recover it, nothing. So I gave up."* Amara — *"I don't want to lose everything I've built after four days."* (`02-research/interview-synthesis.md`)
- **Day-7 retention:** comeback 76% vs. control 46% — **+30 points, p = 0.002 (significant)**. (`05-decide/metric-findings.md`)
- **Engagement:** comeback messaging open rate climbs 28% → 56% across four sends — not fatiguing, the reverse — vs. a flat 4% for control. (`05-decide/metric-findings.md`)
- **Honest gap:** Day-30 lift is directionally positive (+14 points) but **not yet statistically significant** at this sample size. (`05-decide/metric-findings.md`)

## Slide 5 — The Plan

- Move the current v1 scope (stat + lesson) into the Q3 sprint. (`recommendation-memo.md`)
- Run a two-week extension at a larger sample, focused specifically on users who broke their streak, to get that target-population read past the significance line. (`recommendation-memo.md`)
- **Go/no-go on full rollout at the end of that two-week window — not left open-ended.** (`recommendation-memo.md`)
- **Risk if we wait:** every week without this, the ~80% of week-1 streak-breakers who currently never return keep leaving at that rate, on a problem we've already shown a working, significant fix for. (`recommendation-memo.md`)

## Slide 6 — The Ask

1. Approval to proceed into the Q3 sprint at v1 scope.
2. Approval to run the two-week larger-sample extension, with a go/no-go date attached at the end of it. (`recommendation-memo.md`)
