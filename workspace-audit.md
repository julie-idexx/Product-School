# Workspace Audit — Streakly / pm-workspace

*Full review of the current folder structure, every file in it, and `CLAUDE.md`, done before updating `CLAUDE.md` for next session.*

## 1. What's missing that would make Claude more useful next session

1. **`CLAUDE.md` itself was badly stale.** It was frozen at "in discovery — no designs, no committed scope, 8 weeks from sprint kickoff," even though the prototype has since been built, tested across multiple rounds, written up as a pressure-tested PRD, scoped with Raj (v1 = stat + lesson, freeze deferred to v2), run as a real randomized pilot with a significant Day-7 result, diagnosed, and turned into both a recommendation memo and a quarterly deck. A fresh session reading only `CLAUDE.md` would think none of that happened. *(Fixed in this update.)*
2. **The local project folder isn't actually a git repository.** There's no `.git` directory here — every push this session has gone through a temporary clone in `/tmp`, which has already been silently wiped and needed re-cloning twice. Next session, Claude has no local `git log`/`git status` to check and will re-derive the same clone-and-rsync workaround from scratch.
3. **An incomplete task has no trace anywhere.** The Lena design-review roleplay (meant to be saved to `04-team/design-review.md`) was interrupted before her three hardest questions were ever answered, and no file was ever saved. Nothing in the workspace records that this was started, so a future session has no way to know whether to resume it or that it was dropped.
4. **`data/experiment-design.md` exists locally but was never pushed to GitHub** — only `data/metric-diagnosis.md` made it into the repo. The raw CSVs and `data/README.md` were never pushed at all. Anyone (or any future session) working from the GitHub repo alone is missing this analysis entirely.
5. **The five per-module template files are still 100% unfilled**, even though the real work behind nearly every checklist item in them already exists elsewhere:
   - `01-orient/orientation.md` — project.md/strategy.md/change_log.md are all done; the "First Skill" line was never filled in even though `skills/weekly-status.md` exists.
   - `03-build/build.md` — the Prototype + Iteration Log table, the Hypothesis, and the Triad Session Plan all have real counterparts (`change_log.md`'s P3L2a entry, `03-build/hypothesis.md`, `03-build/triad-session.md`) that were never linked back in.
   - `04-team/collaboration.md` — Codebase Tour + Spec Readiness and the Design Review + QA edge-case table both have real files (`codebase-summary.md`, `spec-readiness.md`, `qa-checklist.md`'s edge-case list) that were never pointed to.
   - `05-decide/decide.md` — every field (Findings/Diagnosis/Memo, Experiment Design, Reusable Skills + Deck) already has a matching real artifact (`metric-findings.md`, `metric-diagnosis.md`, `recommendation-memo.md`, `data/experiment-design.md`, the `grounded-prd` and `weekly-status` skills, `presentation.pptx`) — none of it is reflected here.
   - `06-systems/systems.md` — the Workspace + Three Skills list has two of three (`grounded-prd`, `weekly-status`); the Agent Stack table is completely untouched.
6. **`06-systems/final-presentation.html` is still the bare stub** from day one — never generated, even though there's now more than enough material to actually build it.
7. **The Module 6 "Agent Stack" hasn't been started at all** — metric pulse, weekly insight, and anomaly-to-hypothesis agents are the one piece of the course structure with zero work behind it.
8. **`README.md`'s status table still shows every module unchecked (☐), and `strategy.md` still says "not yet committed" / "still in discovery."** Both actively contradict the real state of the project and would mislead anyone (or any session) reading them at face value.

## 2. Reorganization to reduce friction

1. **Make this folder an actual git repository.** `git init`, point it at the existing GitHub remote, and pull the history down, so normal `git status`/`add`/`commit`/`push` work in place. Every push this session has instead needed a throwaway clone elsewhere — fragile, and it's already broken twice when `/tmp` got cleared.
2. **Bring `data/` inside the project instead of as a sibling folder.** Right now the CSVs and their two analysis docs live one directory above `Product-School-main`, outside git entirely, while everything else lives inside it. One root, one git history.
3. **Feed the five module-template files from the real docs instead of leaving them permanently blank.** Each one's checklist already maps onto a real file elsewhere in the repo — a short linking pass would make the module structure actually reflect the work, instead of silently diverging from it the way `02-research/` already had to be fixed once this session.
4. **Remove (or `.gitignore`) `Day 3 - Data.zip`** at the project root — it's the already-extracted source of `data/`, now redundant clutter, and one accidental `git add -A` away from being committed.
5. **Close the Lena design-review loop deliberately** — either finish it, or note in `change_log.md` that it was intentionally dropped, so it's a documented decision instead of an invisible gap.

## 3. CLAUDE.md

Updated and saved directly — see [`CLAUDE.md`](CLAUDE.md). Summary of what changed: the Situation/Current Focus section now reflects the actual state (prototype tested, PRD pressure-tested, v1/v2 scope agreed, pilot run with a significant Day-7 result, diagnosis and recommendation memo written, quarterly deck built), the `Tone`/`Defaults`/`Never` fields are filled in from patterns observed across this session (flagged as inferred, not confirmed), and the Glossary now has the terms that actually recurred throughout.
