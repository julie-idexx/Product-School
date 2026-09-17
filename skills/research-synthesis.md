---
name: research-synthesis
description: Run the recurring weekly research synthesis for Streakly with a single trigger phrase and no additional input - summarizes new user feedback, support tickets, or NPS comments dropped in 02-research/inbox/ since the last run, using the same rigor (themes ranked by frequency, direct quotes, contradictions named) as the existing interview-synthesis.md and nps-analysis.md. Use whenever the user says something like "run my weekly research synthesis," "summarize this week's feedback," or pastes the trigger phrase below.
---

# Weekly Research Synthesis

**Trigger prompt** — paste this to run it:
> Run my weekly research synthesis for Streakly.

## Where new material comes from

There's no live feed of support tickets or NPS comments wired into this workspace, so this skill depends on a simple convention instead: new raw material — an exported CSV, a batch of comments, a pasted ticket log — gets dropped into `02-research/inbox/` between runs. That's the only place this skill looks for "new" input; it doesn't re-synthesize the same interviews or NPS batch every week; and if the inbox is empty, the honest result is "nothing new this week," not a fabricated theme to fill the space.

## Steps to run, in order

1. **Check `02-research/inbox/` for anything besides its own README.** If it's empty, report that plainly and stop — don't manufacture a synthesis from files already covered in `02-research/interview-synthesis.md` or `02-research/nps-analysis.md`.
2. **Read everything found, in full.** Same standard as the original syntheses: don't skim for keywords, actually read what people said.
3. **Synthesize with the same structure those two files already use** — themes ranked by how often they recur, a direct quote backing each one (not paraphrase), and any contradiction between sources named explicitly rather than smoothed over. If a new theme doesn't have a real quote behind it, it's a hunch, not a theme — leave it out or flag it as unconfirmed.
4. **Check whether anything new changes an existing finding.** If the new material reinforces a theme already in `interview-synthesis.md` or `nps-analysis.md`, say so and cite which one. If it contradicts one, flag that explicitly rather than letting the two documents quietly disagree with each other.
5. **Archive what was processed.** Move the files read out of `02-research/inbox/` into `02-research/inbox/archive/` (create it if needed) so the next run doesn't re-process them.

## Output format

A dated entry with: what was reviewed (file names, rough volume — "14 support tickets," "1 NPS export"), themes found (ranked, each with a quote), and an explicit line on whether this changes anything in the existing research docs.

## Where it's saved

Append as a new dated section to `02-research/weekly-synthesis-log.md` (create it if it doesn't exist), newest entry at the top. If a theme is significant enough to actually change `interview-synthesis.md` or `nps-analysis.md`, say so in the log entry and make that edit too — don't leave a real update sitting only in the log while the source-of-truth docs go stale.
