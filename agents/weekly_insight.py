#!/usr/bin/env python3
"""
Streakly Weekly Insight Agent

Pulls three sources - retention metrics (data/), sprint completions
(change_log.md, supplemented by git log when change_log is sparse), and
the top NPS/user-feedback signal (a fresh weekly-synthesis-log.md entry if
one exists, otherwise the standing nps-analysis.md) - into a fixed 3-2-1
report: Done this week (3), Changed this week (2), Watch next week (1).

Reuses metric_pulse.py's retention math directly rather than
re-implementing it, so the two agents never quietly disagree about what
"this week" means for the same numbers.
"""

import argparse
import csv
import json
import os
import re
import subprocess
import urllib.request
from collections import defaultdict
from datetime import date, datetime, timedelta

import metric_pulse as mp

REPORTS_DIR_DEFAULT = "../reports"


# ---------------------------------------------------------------- Sprint completions

def parse_change_log(path, since, until):
    """Return (date, change_text) tuples for change_log.md rows inside [since, until]."""
    if not os.path.exists(path):
        return []
    rows = []
    with open(path) as f:
        for line in f:
            m = re.match(r"^\|\s*(\d{4}-\d{2}-\d{2})\s*\|\s*(.*?)\s*\|\s*.*\|\s*$", line)
            if not m:
                continue
            d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
            if since <= d <= until:
                rows.append((d, m.group(2)))
    return sorted(rows, reverse=True)


def git_log_subjects(repo_dir, since, until):
    try:
        out = subprocess.run(
            ["git", "-C", repo_dir, "log", f"--since={since}", f"--until={until + timedelta(days=1)}",
             "--pretty=%s"],
            capture_output=True, text=True, check=True,
        ).stdout
    except Exception:
        return []
    return [line.strip() for line in out.splitlines() if line.strip()]


def shorten(text, max_len=140):
    text = re.sub(r"\*\*|`", "", text)
    first_sentence = re.split(r"(?<=[.!?])\s", text)[0]
    candidate = first_sentence if len(first_sentence) <= max_len else text
    return candidate[:max_len].rstrip() + ("…" if len(candidate) > max_len else "")


def build_done_bullets(change_log_path, repo_dir, since, until, n=3):
    entries = parse_change_log(change_log_path, since, until)
    bullets = [shorten(text) for _, text in entries]

    if len(bullets) < n:
        seen = {b.lower()[:40] for b in bullets}
        for subj in git_log_subjects(repo_dir, since, until):
            if len(bullets) >= n:
                break
            key = subj.lower()[:40]
            if key in seen:
                continue
            seen.add(key)
            bullets.append(shorten(subj))

    return bullets[:n]


# ---------------------------------------------------------------- Retention signal

def top_channel_move(this_week, last_week):
    deltas = {}
    for ch in mp.CHANNELS:
        now = this_week["by_channel"][ch]["day7"]
        prev = last_week["by_channel"][ch]["day7"]
        if now is None or prev is None:
            continue
        deltas[ch] = mp.pts(now - prev)
    if not deltas:
        return None
    ch = max(deltas, key=lambda c: abs(deltas[c]))
    now_pct = round(this_week["by_channel"][ch]["day7"] * 100)
    d = deltas[ch]
    direction = "dropped" if d < 0 else "rose"
    trend = ", accelerating decline" if d <= -3 else (", recovering" if d >= 3 else "")
    return f"{ch.capitalize()} channel retention {direction} {abs(d)}pt{'s' if abs(d) != 1 else ''}, now {now_pct}%{trend}"


# ---------------------------------------------------------------- Push notification signal

def nudge_open_rate_move(nudges_path, users, this_week_num, last_week_num, nudge_type="streak_lost"):
    """Week-over-week open rate for the named nudge type, sent-date buckets ordered
    oldest-to-newest and treated as cohort_week 1..N by position (not by date math,
    since a live system's send cadence may not stay a fixed number of days apart).

    Guards against the same class of bug metric_pulse.py guards against for
    retention: once an A/B test is live, the experiment arms can get logged under
    *different* nudge_type values (comeback-arm traffic moves to nudge_type
    "comeback_screen" while control stays "streak_lost") - so a naive WoW
    comparison on nudge_type="streak_lost" alone silently compares "everyone" one
    week against "only the control arm" the next. That's not a real signal; it's
    the population definition changing underneath the metric.
    """
    if not os.path.exists(nudges_path):
        return None
    with open(nudges_path, newline="") as f:
        all_rows = list(csv.DictReader(f))

    all_dates = sorted(set(r["sent_date"] for r in all_rows))
    if len(all_dates) < 2:
        return None
    # oldest send-date = week 1, by position - matches the same ordinal week numbers
    # the rest of the report uses (this_week_num/last_week_num), so a --week override
    # applies consistently across both signals instead of this one silently always
    # looking at its own latest dates.
    if this_week_num > len(all_dates) or last_week_num < 1:
        return None
    this_d = all_dates[this_week_num - 1]
    last_d = all_dates[last_week_num - 1]

    if mp.has_active_experiment(users, this_week_num) or mp.has_active_experiment(users, last_week_num):
        return ("Push notification open rate comparison skipped this week - the nudge_type "
                "split changed because of the active A/B test (see metric_pulse.has_active_experiment); "
                "comparing it as-is would compare different populations, not a real week-over-week move")

    rows = [r for r in all_rows if r["nudge_type"] == nudge_type]
    by_date = defaultdict(list)
    for r in rows:
        by_date[r["sent_date"]].append(r)
    if this_d not in by_date or last_d not in by_date:
        return None

    def rate(d):
        rs = by_date[d]
        return sum(1 for r in rs if r["opened"] == "true") / len(rs)

    now, prev = rate(this_d), rate(last_d)
    delta = mp.pts(now - prev)
    if delta == 0:
        return None
    direction = "recovered" if delta > 0 else "dropped"
    return f"Push notification open rate {direction} {abs(delta)}pt{'s' if abs(delta) != 1 else ''} to {round(now * 100)}%"


# ---------------------------------------------------------------- NPS / user-feedback signal

def fresh_synthesis_entry(log_path, since):
    if not os.path.exists(log_path):
        return None
    with open(log_path) as f:
        text = f.read()
    m = re.search(r"^##\s*(\d{4}-\d{2}-\d{2})", text, re.MULTILINE)
    if not m:
        return None
    d = datetime.strptime(m.group(1), "%Y-%m-%d").date()
    if d < since:
        return None
    # first non-empty line after the date heading
    after = text[m.end():].strip().splitlines()
    return after[0].strip() if after else None


def standing_top_nps_theme(nps_path):
    if not os.path.exists(nps_path):
        return None
    with open(nps_path) as f:
        text = f.read()
    m = re.search(r"\|\s*1\s*\|\s*(.*?)\s*\|", text)
    return m.group(1).strip() if m else None


# ---------------------------------------------------------------- Watch next week

def top_open_item(stakeholders_dir, priority=("raj", "marcus", "lena")):
    for name in priority:
        path = os.path.join(stakeholders_dir, f"{name}.md")
        if not os.path.exists(path):
            continue
        with open(path) as f:
            text = f.read()
        section = text.split("## Open items", 1)
        if len(section) < 2:
            continue
        m = re.search(r"-\s*\*\*(.*?)\*\*", section[1])
        if m:
            return name.capitalize(), m.group(1).strip()
    return None, None


# ---------------------------------------------------------------- Assemble + format

def build_report(args, run_date):
    since = run_date - timedelta(days=7)

    users = mp.load_csv(args.users)
    retention = mp.load_csv(args.retention)
    channel_by_user = {u["user_id"]: u["acquisition_channel"] for u in users}

    this_week_id = args.week if args.week is not None else mp.latest_week(retention)
    last_week_id = this_week_id - 1
    this_week = mp.compute_week_metrics(retention, channel_by_user, this_week_id)
    last_week = mp.compute_week_metrics(retention, channel_by_user, last_week_id)
    experiment_active = mp.has_active_experiment(users, this_week_id)

    done = build_done_bullets(args.change_log, args.repo_dir, since, run_date)

    changed = []
    retention_move = top_channel_move(this_week, last_week)
    if retention_move:
        if experiment_active:
            retention_move += " (week includes an active A/B test - see metric-pulse.md)"
        changed.append(retention_move)

    fresh_theme = fresh_synthesis_entry(args.synthesis_log, since)
    if fresh_theme:
        changed.append(f"New user-feedback theme this week: {fresh_theme}")
    else:
        nudge_move = nudge_open_rate_move(args.nudges, users, this_week_id, last_week_id)
        if nudge_move:
            changed.append(nudge_move)
        else:
            standing = standing_top_nps_theme(args.nps)
            if standing:
                changed.append(f"No new feedback synthesized this week; standing top NPS theme is still: {standing}")

    who, item = top_open_item(args.stakeholders_dir)
    watch = [f"{who}'s open item: {item}"] if who else ["No open items flagged in any stakeholder profile."]

    return done[:3], changed[:2], watch[:1], {
        "this_week_cohort": this_week_id, "experiment_active": experiment_active,
    }


def format_report(done, changed, watch, run_date):
    lines = [f"\U0001F4CB Streakly Weekly Insight, {run_date.strftime('%a %b %-d')}", ""]
    lines.append("Done this week:")
    lines += [f"• {b}" for b in done]
    lines.append("")
    lines.append("Changed this week:")
    lines += [f"• {b}" for b in changed]
    lines.append("")
    lines.append("Watch next week:")
    lines += [f"• {b}" for b in watch]
    return "\n".join(lines)


def slack_summary(done, changed, watch):
    parts = ["*Streakly Weekly Insight — 3-2-1*"]
    parts.append("*Done:* " + " / ".join(done))
    parts.append("*Changed:* " + " / ".join(changed))
    parts.append("*Watch:* " + " / ".join(watch))
    return "\n".join(parts)


def post_to_slack(webhook_url, text):
    req = urllib.request.Request(
        webhook_url, data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Streakly weekly insight agent")
    parser.add_argument("--users", default=os.path.join(base_dir, "../data/users.csv"))
    parser.add_argument("--retention", default=os.path.join(base_dir, "../data/retention.csv"))
    parser.add_argument("--nudges", default=os.path.join(base_dir, "../data/nudges.csv"))
    parser.add_argument("--change-log", default=os.path.join(base_dir, "../change_log.md"))
    parser.add_argument("--nps", default=os.path.join(base_dir, "../02-research/nps-analysis.md"))
    parser.add_argument("--synthesis-log", default=os.path.join(base_dir, "../02-research/weekly-synthesis-log.md"))
    parser.add_argument("--stakeholders-dir", default=os.path.join(base_dir, "../04-team/stakeholders"))
    parser.add_argument("--repo-dir", default=os.path.join(base_dir, ".."))
    parser.add_argument("--reports-dir", default=os.path.join(base_dir, REPORTS_DIR_DEFAULT))
    parser.add_argument("--week", type=int, default=None)
    parser.add_argument("--post", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    run_date = date.today()
    done, changed, watch, meta = build_report(args, run_date)
    report = format_report(done, changed, watch, run_date)
    summary = slack_summary(done, changed, watch)

    print(report)
    print("\n--- Slack 3-2-1 summary ---\n")
    print(summary)

    if args.json:
        print("\n--- raw (--json) ---")
        print(json.dumps({"done": done, "changed": changed, "watch": watch, "meta": meta}, indent=2))

    os.makedirs(args.reports_dir, exist_ok=True)
    out_path = os.path.join(args.reports_dir, f"{run_date.isoformat()}.md")
    with open(out_path, "w") as f:
        f.write(report + "\n")
    print(f"\nSaved to {os.path.relpath(out_path, base_dir)}")

    if args.post:
        webhook = os.environ.get("SLACK_WEBHOOK_URL")
        if not webhook:
            print("[ERROR] --post given but SLACK_WEBHOOK_URL is not set. Nothing posted.")
            return
        status = post_to_slack(webhook, summary)
        print(f"[posted 3-2-1 summary to Slack, status {status}]")


if __name__ == "__main__":
    main()
