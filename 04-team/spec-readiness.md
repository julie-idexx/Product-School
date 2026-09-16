# Spec Readiness — Streakly Comeback Screen

*Simulated review: Claude in character as Raj (per [`04-team/stakeholders/raj.md`](stakeholders/raj.md)) reading [`docs/decision-brief.md`](../docs/decision-brief.md) as if it were the engineering spec for the Comeback screen.*

## 1. Readiness summary

**What was solid**

- The problem framing didn't get challenged at all — Raj went straight past "is this real" into "how do we build it." The converging evidence (interviews, NPS, competitive matrix) and the specific numbers (48%→39%, ~80% never return) did their job.
- The recommendation itself (Option 3, the full Comeback experience over "do nothing" or "freeze only") held up against his scrutiny — he never questioned *whether* to build it, only *what* "it" means at a ticket level.

**What needed work**

- **`docs/decision-brief.md` is a strategic recommendation, not a spec.** It has a situation, findings, and a recommended direction — but nothing about what ships, in what order, or what "done" means. That gap was the very first thing raised.
- **No v1/v2 scope cut existed.** "Build the full Comeback experience" reads as one shippable unit; it isn't. Resolved in conversation: **v1 = best-streak stat + comeback lesson only; the streak-freeze is explicitly deferred to v2.**
- **A real edge case had no owner.** Users who lapse twice in the same week — using Raj's own churn stat as the frame — had no defined behavior. The honest answer surfaced in conversation was that today, nothing happens for them; that's now written down as a deliberate v1 exclusion instead of a silent gap.
- **No measurement plan existed that survives partial treatment.** If a real subgroup of lapsed users never sees the feature, a single blended Day-7 number either overstates or dilutes the result depending on how it's read. Resolved: report both an intent-to-treat number and a treated-subgroup number, not one figure standing in for both questions.

**Bottom line:** the *why* was never in question. The *what ships first* and *how we'll know it worked* were the real gaps, and both now have answers — they just don't exist anywhere in writing yet outside this doc.

## 2. Rewrite — sections to add to the spec

*Drop this in as a new section of the decision brief (or the eventual engineering ticket). It's new content, not an edit to existing text — the decision brief didn't have a build-scope section at all.*

---

### Build Scope & Measurement (v1)

**In scope for v1**
- Best-streak stat (permanent record, shown separately from the current streak).
- Comeback lesson (60-second lesson continuing the user's existing track).

**Explicitly out of scope for v1**
- **One-tap streak-freeze.** Deferred to v2. Data-model work for the freeze field is still open (see Raj's stakeholder profile) and shouldn't block v1.
- **Users who lapse twice within the same week.** The Comeback screen does not trigger for this segment in v1 — they see no intervention and are expected to churn at the current baseline rate. This is a stated limitation, not an oversight. Candidate for v2, likely bundled with the freeze mechanic, since a repeat-lapse user is precisely who a freeze is meant to protect.

**Measurement plan**
- **Intent-to-treat metric:** Day-7 retention across *all* users who broke a streak in week 1, including the double-miss segment who received no treatment. This is the honest, whole-population number for Marcus and the business read.
- **Treated-subgroup metric:** Day-7 retention isolated to users who actually saw the Comeback screen (single-lapse only). This is the number that tells us whether the mechanism itself works, and prevents a real effect from being diluted by a population the v1 feature was never designed to reach.
- Both numbers get reported together. Neither stands alone.

---

## 3. Async message to Raj

> **Re: Comeback screen — scope confirmation before sprint kickoff**
>
> Closing the loop from our conversation. Here's what's going into the ticket:
>
> - **v1 scope:** best-streak stat + comeback lesson only. Streak-freeze is explicitly v2 — not in this sprint.
> - **Known v1 gap, documented not silent:** users who lapse twice in the same week get no intervention in v1. Flagged as a candidate for v2, likely paired with the freeze.
> - **Measurement:** we'll report Day-7 retention two ways — intent-to-treat (everyone eligible) and treated-subgroup (single-lapse users who actually saw the screen) — so a real effect doesn't get hidden or overstated.
>
> Flag anything above that doesn't match what you need before I bring this to Marcus and Lena. If it's silent, I'm reading that as confirmed.
