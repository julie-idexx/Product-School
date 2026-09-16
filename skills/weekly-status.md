---
name: weekly-status
description: Turn raw, messy bullet-point notes into a formatted leadership status update with Shipped, In Progress, Blockers, and Next Week sections. Use this whenever the user asks to write a weekly status update, leadership update, or standup summary, or wants to turn rough notes, Slack messages, or a brain dump into something polished enough to send to a manager or leadership team — even if they don't say "skill" or name the sections explicitly.
---

# Weekly Status Update

Take raw bullet-point notes (standup notes, a Slack thread, a quick brain dump) and turn them into a clean, leadership-ready weekly update. The person using this skill usually has more context in their head than they wrote down — the job is to make the update readable and scannable for someone who has none of that context, without adding anything that wasn't actually said.

## Output structure

Always use this exact template:

```
## Shipped
- ...

## In Progress
- ...

## Blockers
- ...

## Next Week
- ...
```

## Rules

- **3 bullets max per section.** Leadership updates get skimmed, not read. If the raw notes have more than 3 relevant items for a section, choose the 3 most significant for a leadership audience rather than compressing everything into fewer, denser bullets.
- **Plain, declarative language.** Say what happened, is happening, or will happen. No jargon, no buzzwords, no hedging language ("leveraged," "synergies," "circling back," "socializing"). Write "Shipped the onboarding redesign," not "Successfully delivered against onboarding redesign objectives."
- **One sentence per bullet.** Each bullet is a complete, standalone statement — not a fragment or a to-do checkbox.
- **If a section is empty, say so.** Write "None" under Blockers (or whichever section) rather than dropping the heading. A leadership update with no blockers listed at all reads as incomplete, not clean.
- **Don't invent specifics.** If the raw notes are vague (e.g., "working on payments still"), keep the bullet similarly general rather than guessing a percentage, a date, or a reason. Only include numbers, names, or causes that were actually in the input.

## Example

**Input (raw notes):**
```
- finished the new signup flow, QA passed
- still working on payment integration, about 70% done
- waiting on legal review for the new terms of service, blocking launch
- next week: start onboarding email sequence, kick off analytics dashboard
```

**Output:**
```
## Shipped
- Finished the new signup flow; QA passed.

## In Progress
- Payment integration is about 70% complete.

## Blockers
- Legal review of the new terms of service is blocking launch.

## Next Week
- Start the onboarding email sequence.
- Kick off the analytics dashboard.
```
