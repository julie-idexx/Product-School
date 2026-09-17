---
name: weekly-status
description: Turn raw, messy bullet-point notes into one or more formatted status updates — a team update and/or a leadership update — each calibrated to its specific audience using stakeholder profiles (04-team/stakeholders/*.md) when they exist. Use this whenever the user asks to write a weekly status update, standup summary, or leadership update, or wants to turn rough notes, Slack messages, or a brain dump into something polished enough to send to teammates or a manager — even if they don't say "skill" or name the sections explicitly. Trigger especially when the user names specific people the update is for (e.g. "for Raj and Lena," "update for Marcus") — that's the signal to calibrate per-audience rather than write one generic update.
---

# Weekly Status Update

Take raw bullet-point notes (standup notes, a Slack thread, a quick brain dump) and turn them into a clean, audience-ready update. The person using this skill usually has more context in their head than they wrote down — the job is to make the update readable and scannable for someone who has none of that context, without adding anything that wasn't actually said.

## Check the input against reality first

Before formatting anything, if the workspace has files that would confirm or contradict a claim in the raw notes (a doc, a decision brief, a prior deliverable), check them. If a claim doesn't hold up — something marked "complete" that another file shows was never actually obtained, a percentage that undersells work that's since finished — don't launder it into the update. Write what's actually true and say plainly why you adjusted it. A status update exists so the reader can trust it without re-verifying; passing along a claim you already know is wrong defeats the entire point, and for an audience like an engineer who explicitly doesn't want to be surprised later, it's worse than saying nothing.

## Audience calibration

If the update is going to more than one person, or the user names specific recipients, don't write one blended document — write one version per audience group, and calibrate each using that person's stakeholder profile if one exists in the workspace (check `04-team/stakeholders/` or wherever this project keeps them). What changes between versions:

- **Format and length** — someone who reads async in short bursts needs bullets and brevity; someone who wants the punchline before the details needs the headline in the first sentence, not buried in a Shipped section.
- **What gets foregrounded** — an engineering audience cares about what's blocking build work and what needs a decision from them specifically; a design audience cares about anything touching user-facing behavior or evidence; a leadership audience cares about how this connects to the metric they own and whether there's a decision or deadline they need to act on.
- **What gets left out** — cutting detail an audience doesn't need isn't hiding information, it's respecting that a leadership update skimmed in ten seconds needs a different density than a team update someone will actually read line by line.

## Output structure

Default to this template per audience, adapting section order or emphasis to match what that profile says they need first:

```
## Shipped
- ...

## In Progress
- ...

## Blockers
- ...

## Next Week / Ask
- ...
```

A leadership-calibrated version often needs a one-sentence headline *before* this structure — the recommendation or bottom line first, exactly the way that reader wants to receive it, with the structure underneath as backup detail they can skim into if they want more.

## Rules

- **3 bullets max per section.** Updates get skimmed, not read. If the raw notes have more than 3 relevant items for a section, choose the most significant ones for that specific audience rather than compressing everything into fewer, denser bullets.
- **Plain, declarative language.** Say what happened, is happening, or will happen. No jargon, no buzzwords, no hedging language ("leveraged," "synergies," "circling back," "socializing").
- **One sentence per bullet.** Each bullet is a complete, standalone statement — not a fragment or a to-do checkbox.
- **If a section is empty, say so.** Write "None" rather than dropping the heading. An update with no blockers listed at all reads as incomplete, not clean.
- **Don't invent specifics.** If the raw notes are vague, keep the bullet similarly general rather than guessing a percentage, a date, or a reason. Only include numbers, names, or causes that were actually in the input — or that you corrected against a workspace file, with the correction stated.
- **A person's own unavailability isn't news to report back to them.** If the notes mention that the recipient themselves is out or unavailable, that's context for how you frame the update (fully self-contained, no dependency on a live sync, an ask with a deadline that accounts for the gap) — not a bullet point telling them their own schedule.

## Example

**Raw notes** (Streakly Comeback screen, week of [date]):
```
Shipped: interview synthesis complete (Priya, Tom, Amara); competitive matrix done
(Duolingo, Babbel, Elevate; 2 white-space gaps); Reddit sentiment analysis complete,
gaps confirmed by real user friction; prototype v1 live and tested across three
personas.
In progress: PRD first draft, 70% done; usability session scheduling, 3 of 5 confirmed.
Blockers: Raj flagged the streak-freeze logic needs a data model change, estimate TBD;
Marcus out Thu-Fri, async review only.
```

Workspace check found: the "Reddit sentiment analysis complete" claim contradicts `docs/decision-brief.md`, which already discloses this was attempted but never obtained (tool access couldn't reach reddit.com). The "PRD 70% done" claim is stale — `docs/prd.md` shows the PRD is finished and has already been through objection-testing (`docs/objection-log.md`). Both get corrected below, not repeated. "Marcus out Thu-Fri" isn't a bullet in his own update — it shapes the update to be fully self-contained instead.

**Team update** (Raj + Lena — per `04-team/stakeholders/raj.md`: async-first, bullets, no surprises, hates ambiguity on blockers; per `04-team/stakeholders/lena.md`: prefers evidence-forward "here's what we found" framing):
```
## Shipped
- Interview synthesis complete (Priya, Tom, Amara).
- Competitive matrix done — Duolingo, Babbel, Elevate; 2 white-space gaps identified.
- Reddit sentiment analysis attempted, not completed — tool access couldn't reach
  reddit.com. Competitive gaps still rest on the structured research only.
- Prototype v1 live, tested across three personas.
- PRD complete and already pressure-tested — not still in draft.

## In Progress
- Usability session scheduling: 3 of 5 confirmed.

## Blockers
- Streak-freeze logic needs a data-model change, estimate still TBD — blocking v2
  scoping specifically, not the v1 build.

## Next Week / Ask
- Need the data-model estimate before the freeze work can be scoped into a sprint.
```

**Leadership update** (Marcus — per `04-team/stakeholders/marcus.md`: recommendation/headline first, one page, ties to the Day-7 number, comfortable following up async):
```
Headline: research and prototype testing are done and point to the same fix; the PRD
is written and already stress-tested. One open engineering estimate is the only thing
left before this is ready to scope for Q3.

## Shipped
- Research phase complete — interviews, competitive analysis, and prototype testing
  across three personas all converge on the same problem and fix.
- PRD written and pressure-tested, including against a churned user's specific
  objection.

## Blockers
- Data-model estimate for the streak-freeze is still open — no timeline yet.
- Keeping this fully async this week given your schedule — nothing here needs a live
  review, flag anything in writing.

## Next Week / Ask
- No decision needed from you this week. Next real checkpoint is once the estimate lands.
```
