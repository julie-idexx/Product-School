# Codebase Tour — HabitRPG/habitica

*Queried directly against [github.com/HabitRPG/habitica](https://github.com/HabitRPG/habitica) (default branch `develop`) as a stand-in "existing codebase" exercise for scoping the Streakly Comeback screen: a best-streak stat, a 60-second comeback lesson, and a one-tap streak-freeze, shown when a user breaks a streak.*

> **Note on this repo specifically:** its README currently states a **"No AI-Generated Code Policy"** — no LLM/AI-authored code will be accepted in PRs. That's a real governance fact worth knowing if you were actually shipping into this repo; it doesn't affect this read-only research exercise, but it's the kind of constraint that belongs in a spec's assumptions section for any *real* codebase your team touches.

## 1. PM-level tour

**What it does, in one sentence:** Habitica is an open-source habit- and task-tracker that turns your real life into an RPG — you complete Habits, Dailies, and To-Dos to earn gold and XP and keep your avatar's HP up, and you take damage for missing Dailies.

**How the codebase is organized**

```
website/
  server/        Node/Express API
    models/      Mongoose schemas (Task, User, Group, Challenge, ...)
    controllers/ REST endpoints, versioned (api-v3 is current)
    middlewares/ auth, rate limiting, error handling
    libs/        business logic too big for a controller (cron.js is here)
  client/        Vue 3 SPA (src/components, src/pages, src/store)
  common/        Logic shared between client and server — the actual
                 game rules (scoring, cron math, content definitions)
    script/ops/  one file per user action (scoreTask.js, buy/, equip.js...)
migrations/       one-off scripts for schema/data changes already run
test/              integration + unit tests, mirrors website/ structure
```

The split that matters most for a PM: **`common/`** holds the actual game-rule logic (how much a streak is worth, what happens on a miss) so both the Node server and the Vue client agree on it. **`server/`** is where that logic gets triggered and persisted. **`client/`** is what the user sees. A feature like Comeback almost always touches all three.

**The 3 most important files to know**

1. **[`website/server/libs/cron.js`](https://github.com/HabitRPG/habitica/blob/develop/website/server/libs/cron.js)** — the daily reset job. This is the single file that decides what happens to a user the next time they open the app after a missed day: HP loss, streak resets, buffs clearing, achievements. Anything "what happens after a lapse" runs through here.
2. **[`website/server/models/task.js`](https://github.com/HabitRPG/habitica/blob/develop/website/server/models/task.js)** — the Task schema. `streak` is a field on an individual Daily task (`streak: { $type: Number, default: 0 }`), not on the user account. This one line is the most important architectural fact in the whole repo for this exercise.
3. **[`website/common/script/ops/scoreTask.js`](https://github.com/HabitRPG/habitica/blob/develop/website/common/script/ops/scoreTask.js)** — the shared logic that runs every time a task is checked or unchecked: it increments/decrements `task.streak`, grants a streak-based gold bonus, fires a `STREAK_ACHIEVEMENT` notification every 21 days, and — critically — already contains streak-freeze-equivalent logic (see below).

**Key data models, and what they tell you about product decisions**

- **`task.streak` lives on the Task, not the User.** Habitica's mental model is "each of your Dailies has its own streak," not "you have one account-wide streak." There's no single hero number anywhere in this schema — that's a deliberate difference from Streakly's one-track, one-streak model, and it's the single biggest reason a Comeback-style feature isn't a small add-on here.
- **`user.stats.buffs.streaks` (a "Chilling Frost" buff)** — this *is* Habitica's existing streak-freeze. In `scoreTask.js`: `if (!user.stats.buffs.streaks || task.challenge.id || task.group.id) task.streak = 0;`. It's single-use and gets cleared every cron run (`server/libs/cron.js`, `streaks: false`). Product read: protecting a streak from a miss is a *solved, first-class concept* here already — but it's tied to a consumable potion/buff, not a standing toggle a user turns on once.
- **`user.lastCron` / `user._cronSignature`** — cron isn't a nightly batch job. It's computed lazily: the server checks `daysUserHasMissed()` on the next request from that specific user (`website/server/libs/user/index.js`, returned to the client as `needsCron`), and `_cronSignature` exists purely to stop the same user's cron from double-firing if two requests race. Product read: this system was built to scale to millions of users across every timezone without a midnight cron storm — a real infra constraint, not an accident.
- **`user.achievements.streak`** (milestone count, +1 every 21 days) plus a dedicated **`components/achievements/streak.vue`** celebration modal with explicit client-side dedup (`lastShownStreakCount`) — tells you Habitica already treats streak milestones as a big, celebrated, *permanent* moment, conceptually close to Streakly's "best-streak stat," but implemented as a milestone counter, not a stored "longest streak ever" value.
- **`notifications` and `pushDevices` are embedded arrays directly on the User document** (`UserNotificationSchema`, `PushDeviceSchema` in `server/models/user/schema.js`), not a separate notifications service or table. Anything that needs to notify a user is a document mutation, not a service call.

## 2. Mapping the Comeback screen onto this codebase

**Closest existing precedent — and it's a good one:** Habitica already has a "welcome back" modal: **[`yesterdailyModal.vue`](https://github.com/HabitRPG/habitica/blob/develop/website/client/src/components/tasks/yesterdailyModal.vue)** (`$t('welcomeBack')` / "Check off yesterday's Dailies"). It's shown *before* cron finalizes, letting a user retroactively check off yesterday's misses to avoid the hit. The key difference from Streakly's Comeback screen: this intervenes **within the grace window, pre-reset** (exactly one missed day), not **after the loss has already landed** (Streakly's 2+ day threshold, post-reset). Same UX pattern — a modal that intercepts the normal flow for a lapsed user — different point on the timeline. That's a useful thing to say out loud in a spec: "we're building the *after* version of a pattern this team already ships the *before* version of."

**Where it would live:**
- Client: a new Vue component near `client/src/components/tasks/` (alongside `yesterdailyModal.vue`) or `client/src/components/achievements/` (alongside `streak.vue`), surfaced from `client/src/pages/user-main.vue` — the main app screen — gated on the same `user.needsCron` flag that already triggers the Yesterdaily modal today (`client/src/components/notifications.vue`).
- Server: a new endpoint in `server/controllers/api-v3/` (or an extension of `user.js`), reusing the existing `daysUserHasMissed()` check in `server/libs/user/index.js` rather than duplicating lapse-detection logic.

**What it would touch or depend on:**
- `server/libs/cron.js` — to detect "just returned after a 2+ day lapse" without fighting the existing daily-reset pass.
- `server/models/task.js` — wherever a per-user "best streak" or freeze flag would need to attach, since streak state currently lives per-task.
- `common/script/ops/scoreTask.js` — the existing Chilling Frost pattern is the natural template for a new freeze mechanic, even though it can't be reused as-is (see below).
- `server/models/user/schema.js` — `achievements.streak`, `notifications`, `pushDevices` for surfacing the moment and celebrating the best-streak stat.
- Client: `notifications.vue` and `components/achievements/streak.vue` for the trigger and celebration pattern.

**Blast radius — what else could break:**
- `cron.js` is one large function that runs for *every* active user, every day, and mutates HP, gold, mana, buffs, achievements, and streaks **together in a single pass**. Hooking Comeback-trigger logic into that same pass risks corrupting unrelated state (health, currency, achievements) for users who never even lapsed — not just the lapsed ones a bug might target.
- Streaks aren't always private: `scoreTask.js` explicitly branches on `task.challenge.id || task.group.id` — some Dailies are shared inside a Guild or Challenge. A Comeback feature scoped to "my streak" needs to explicitly exclude (or very deliberately handle) tasks that belong to a group, or it could reset or "protect" a streak that isn't the user's alone to lose.
- The client already has to defensively dedupe the streak-achievement celebration (`lastShownStreakCount`) to avoid showing it twice from race conditions. Any new "you're back!" celebration moment inherits the same risk and needs the same guard.

## 3. What this would change about how I write the spec

**Data that doesn't exist yet:**
- **No "best streak ever" field.** The closest thing, `achievements.streak`, counts how many 21-day milestones were hit — not the longest streak length. A literal best-streak stat needs a new persisted field.
- **No "lesson" content type.** Habitica has exactly four task types (Habit, Daily, To-Do, Reward). A 60-second "comeback lesson" has no analog anywhere in this schema — it's not a smaller version of an existing thing, it's a new content concept.
- **No standing, bankable "freeze for next time."** The existing protection (`stats.buffs.streaks`) is single-use, tied to a specific consumable (Chilling Frost), and auto-clears every cron run. A Streakly-style "one-tap bank a freeze" is a different mechanic, not a reuse of this one.

**Existing constraints to call out in the ticket:**
- Lapse detection is **lazy and per-user** (`needsCron`, computed on that user's next request), guarded against double-firing by `_cronSignature`. Any new trigger needs to hook into or explicitly replicate that pattern — it can't assume a nightly batch job exists to hang off of.
- **`preferences.dayStart`** means "missed a day" is a per-user configurable boundary, not midnight UTC for everyone. A "2+ day lapse" threshold has to respect each user's own day-start setting.
- Streak state can be **shared across users** (challenge/group Dailies) — scope decisions need to explicitly say whether Comeback applies to those or only to solo tasks.

**The one thing engineers will ask before kickoff:**
*"Does the Comeback trigger reuse the existing lazy `needsCron`/`daysUserHasMissed` check that already runs on every login, or does it run as a separate, independent check?"* Reusing it means less new code and no risk of disagreeing with the existing reset logic, but it means changes live inside the highest-blast-radius file in the repo. A separate check is safer to ship in isolation but duplicates missed-day math that already exists, with the very real risk it drifts out of sync with `cron.js` over time. Nearly every other implementation choice — where the endpoint lives, what the rollback plan looks like, how it's tested — depends on the answer to this one question, so it needs to be resolved before the ticket is scoped, not during implementation.
