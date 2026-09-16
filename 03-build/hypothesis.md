# Hypothesis — Streakly Comeback Screen

## Source

Synthesized from [`docs/decision-brief.md`](../docs/decision-brief.md) (the approved recommendation) and [`change_log.md`](../change_log.md) (discovery kickoff through the P3L2a agentic interview round and the resulting prototype change).

## Learning synthesis

### What we know

- **Day-7 retention dropped 9 points (48% → 39%)** since the v2 streak/notification redesign, and it's concentrated in users who break their streak in week 1 — not a broad growth problem (decision brief).
- **Once a user misses two consecutive days, ~80% never return.** A broken streak is closer to a permanent-loss event than a dip (decision brief).
- **The streak reset reads as punishment, not motivation** — this is convergent across three independent research methods (interviews, NPS, competitive matrix), and none of it is about lesson quality. Nobody criticized the content; every complaint was about the mechanics and tone around a lapse (decision brief).
- **No competitor solves post-lapse recovery well.** Every competitor researched (Duolingo, Babbel, Elevate, Brilliant, Streaks) protects users *before* a streak breaks (freezes, charges, skip allowances); almost nothing exists for the moment after it's already broken. This is genuine, still-open white space (decision brief).
- **The comeback intent reads clearly without explanation.** In the P3L2a agentic interview round, all three personas (Priya, Tom, Amara) correctly understood what the screen was for on sight, and none described the tone as punishing or shame-inducing — a meaningful signal that the "coach not scorekeeper" reframe is landing at the surface level (change_log.md).
- **A single reset number can undercut gentler copy around it.** Tom and Amara both flagged that "Day 1" still read as "starting over" regardless of how the surrounding language was softened — this drove the most recent prototype change (adding a lifetime-lessons stat) (change_log.md).

### What we assume

- That showing a best-streak stat, a lifetime-lessons count, and a prospective freeze will change actual *return behavior* — not just make the moment *feel* better in an interview. Feeling less punished and coming back are related but not the same thing, and we have no behavioral data yet, only qualitative and simulated reactions.
- That **one 60-second lesson is enough of a re-engagement trigger** to meaningfully restart the daily habit loop, rather than being a one-time interaction that doesn't change what happens on day 2 of the comeback.
- That the **prospective-only freeze** (protects the *next* miss, doesn't restore what's already lost) is the right tradeoff. This was a deliberate call to stay consistent with the category and focus on the unclaimed post-lapse gap — but it hasn't been tested against a retroactive or hybrid alternative with real users, and the P3L2a round surfaced that all three personas wanted protection earlier (pre-lapse), which this decision doesn't yet address.
- That **agentic interview reactions (Claude in character) are a reasonable stand-in for real usability signal** in this discovery stage. They're useful for catching obvious friction fast, but they're a simulation constrained by the same research this prototype was built from — they can't surface anything genuinely novel that real users might, and they're not a substitute for the next round testing with actual people.
- That **"use data Streakly already has"** (best streak, lifetime lesson count, track progress) is engineering-feasible to compute and display at the exact moment a lapsed user reopens the app, without new instrumentation. Not yet confirmed with engineering.
- That a **single-screen structure** (stat + lesson + freeze toggle together, rather than a multi-step flow) is the right interaction shape. This was a PM judgment call from the build interview, not tested against alternatives.

### What we still don't know

- Whether **real users** react the way the three simulated personas did — this round used Claude-in-character as a stand-in for recruiting outside the room; nothing here has been shown to an actual human yet except, optionally, a classmate.
- Whether the Comeback screen **actually moves Day-7 retention** when shipped. Everything so far is qualitative (interviews, NPS themes, competitive research) or simulated (agentic interview) — there is no experiment result yet.
- Whether one good Comeback screen is enough, or whether — as Tom's skepticism suggests — users who've already churned once need to see the gentler tone hold up *repeatedly* before they'll trust it, which this single prototype can't demonstrate on its own.
- Whether **offering the freeze proactively** (before any lapse) would outperform the current reactive, post-lapse-only design — flagged in the last change_log entry but deliberately not yet tested.
- What the **right guardrail metrics** are (e.g., notification opt-out rate, lesson completion rate, freeze redemption rate) and what magnitude of Day-7 lift would justify shipping this versus a cheaper option — no experiment design exists yet.
- Whether this generalizes across Streakly's other tracks (guitar, coding, chess) or only works for the language-learning content this prototype demoed.

## Hypothesis

We believe that **the Comeback screen — a permanent best-streak stat, a 60-second lesson that continues the user's existing track, and a one-tap streak-freeze offer banked for their next miss — shown to users returning after a 2+ day lapse** will deliver **a measurable recovery in the ~80% of lapsed users who currently never come back** for Streakly users in their first 7 days, as measured by Day-7 retention rate.
