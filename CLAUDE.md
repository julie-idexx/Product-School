# CLAUDE.md — Persistent Memory

> The file Claude Code reads at the start of every session. Short, true, current — the difference between Claude building blind and building with context.

## The Product

*What it does, for whom, current focus.*

**Product:** Streakly — a consumer habit + micro-learning app. Users pick a track (languages, guitar, coding, chess), do a short daily lesson (5 min), and build a streak. The streak is the product's heartbeat. Launched 4 years ago, Series B ($42M), 2.1M registered users, 340K MAU, growing 28% YoY on MAU.

**My role:** PM, own the Engagement squad — home screen, daily lesson loop, streak mechanics, push notifications. Triad: Raj (Senior Engineer), Lena (Product Designer), me. Report to Marcus, Head of Product.

**Situation:** Acquisition works — users install, pick a track, finish their first lesson. The problem is what happens next: a large share of new users break their streak in week 1, and once it's gone, most never come back. Day-7 retention dropped from 48% to 39% over the last two quarters, right after a v2 redesign of the streak and notification system.

**Current focus:** The Comeback experience — no longer just a hypothesis, now a scoped, tested, piloted feature. Where it actually stands:

- **Built and tested:** prototype live (best-streak stat + 60-second lesson + streak-freeze toggle), tested across three research personas (Priya, Tom, Amara) and through an agentic interview round.
- **Scoped with Raj:** v1 = best-streak stat + comeback lesson only. The streak-freeze is explicitly **v2** — the prototype still shows it, but the agreed ticket scope doesn't ship it yet. Users who lapse twice in the same week are a named, deliberate v1 exclusion, not a silent gap.
- **Piloted, not just prototyped:** ran a real randomized test (week-5 signup cohort, comeback vs. control, n=50/arm). Day-7 retention: 76% vs. 46%, **+30 points, statistically significant (p = 0.002)**. Day-30 is directionally positive (+14 points) but **not yet statistically significant** at this sample size — the one thing still unproven.
- **Diagnosed:** among treated users who still churned, the strongest lead is an acquisition-channel/intent mismatch (paid/referral users retaining far worse than organic, even after seeing the screen) — see `data/metric-diagnosis.md`.
- **Written up:** a pressure-tested PRD (`docs/prd.md`, survived objections from Raj, Marcus, and a churned-user perspective — `docs/objection-log.md`), a results memo for Marcus (`docs/recommendation-memo.md`), and a 6-slide quarterly deck (`docs/presentation.pptx`).
- **Open ask, not yet answered:** the recommendation is to run a 2-week larger-sample extension focused on users who actually broke their streak, with a go/no-go date at the end of it — that extension hasn't been run yet. Also open: a design-review pass with Lena on the prototype was started and never finished (three of her questions are still unanswered).
- **Key tension, still live:** re-engagement nudges vs. notification fatigue. The pilot's early read is reassuring here — engagement climbed across follow-ups (28%→56%) rather than fatiguing — but that's from one small pilot, not confirmed at scale.

*Where to look for detail rather than re-deriving it: `docs/prd.md` (what's being built), `04-team/spec-readiness.md` (why the scope is what it is), `05-decide/metric-findings.md` + `data/metric-diagnosis.md` (what the pilot actually showed), `docs/recommendation-memo.md` (the ask to Marcus).*

## Recurring Workflows

Three one-command skills exist for the tasks that repeat every week — check these before treating a status update, research summary, or competitor check as a fresh task:

- **`skills/friday-status.md`** — trigger: *"Run my Friday status update for Streakly."* Self-gathers Shipped/In Progress/Blocked from `git log` and stakeholder open items; no notes need to be dictated. Saves to `status-updates.md`.
- **`skills/research-synthesis.md`** — trigger: *"Run my weekly research synthesis for Streakly."* Reads whatever's new in `02-research/inbox/` (drop raw feedback/tickets/NPS exports there between runs) and synthesizes it. Says "nothing new" honestly if the inbox is empty. Saves to `02-research/weekly-synthesis-log.md`.
- **`skills/competitive-pulse.md`** — trigger: *"Run my competitive pulse check for Streakly."* The one workflow that needs live web search rather than local files — checks Duolingo, Babbel, Elevate, Brilliant, and Streaks for material changes, cited to source. Saves to `02-research/competitive-pulse-log.md`.

## How I Want Claude to Work With Me

- **Interview first:** ask clarifying questions before building.
- **Tone:** *(inferred from this session, not yet confirmed — edit freely)* Direct and evidence-first. Comfortable with real statistical detail (z-tests, sample-size math, significance thresholds) as long as the plain-English meaning comes before the numbers, not after. No cheerleading language — say "not yet significant" plainly rather than smoothing it into something more confident-sounding than the data supports.
- **Defaults:** *(inferred — edit freely)* Cite every claim to a real file rather than asserting it. If a referenced file doesn't exist or is stale, say so instead of guessing or inventing its contents. Verify a prototype actually works in-browser before calling it done. Ask before pushing to GitHub every time — don't assume standing permission just because the last push was approved.
- **Never:** *(inferred — edit freely)* Never fabricate data, quotes, or file contents that aren't actually there. Never silently move, rename, or overwrite files without flagging it first.

## Glossary (my product's words)

| Term | Meaning |
|------|---------|
| Comeback screen | The feature: a screen shown to a user returning after breaking a streak, with a best-streak stat, a 60-second lesson, and (v2) a streak-freeze offer |
| Streak-freeze | A bankable protection against the *next* missed day — prospective only, does not restore a streak already lost |
| `broke_streak_week1` | The data flag for "this user broke their streak in their first week" — the exact population the feature targets |
| Intent-to-treat vs. treated-subgroup | The two-part measurement split agreed with Raj: report Day-7 retention across *everyone* eligible (honest whole-population number) and, separately, only those who actually saw the screen (isolates whether the mechanism itself works) |
| Triad | Me (PM) + Raj (Senior Engineer) + Lena (Product Designer) — the core working group for this feature |
| v1 / v2 | v1 = best-streak stat + lesson, agreed and scoped. v2 = the streak-freeze and the double-lapse-in-a-week case, deliberately deferred, not forgotten |
