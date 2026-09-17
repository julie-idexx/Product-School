#!/usr/bin/env python3
"""
Streakly Metric Pulse Agent

Monitors Day-7 retention rate and streak-break rate, week over week, broken
down by acquisition channel. Formats a Slack digest and (optionally) posts
it. Designed to run nightly; the digest itself is meant to land Monday 8am.

Data model note: this project's sample data is organized by weekly signup
cohort (`cohort_week`), not a rolling daily timestamp. "This week" is
therefore defined as the most recent cohort_week present in retention.csv,
and "last week" as the one before it — each cohort's Day-7 outcome is
exactly the Day-7 number that would have "just landed" for that week. In a
live system with real per-user event timestamps, replace `latest_week()` /
`previous_week()` with a real rolling 7-day window instead of a cohort id.

Caveat this agent does NOT hide: cohort_week 5 in the sample data is an
active A/B test (comeback vs. control). This agent reports the blended,
whole-population number on purpose — it's a business-health monitor, not an
experiment read. The experiment-specific split already lives in
05-decide/metric-findings.md and data/metric-diagnosis.md.
"""

import argparse
import csv
import json
import os
import sys
import urllib.request
from collections import defaultdict
from datetime import date

BASELINE_DAY7 = 0.39
ALERT_THRESHOLD_PTS = 2
CHANNELS = ["organic", "paid", "referral"]


def load_csv(path):
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


def as_bool(v):
    return v.strip().lower() == "true"


def latest_week(retention_rows):
    return max(int(r["cohort_week"]) for r in retention_rows)


def rate(rows, flag_field):
    if not rows:
        return None
    return sum(1 for r in rows if as_bool(r[flag_field])) / len(rows)


def has_active_experiment(users, week):
    """True if any user signed up in this cohort_week carries a non-blank variant -
    i.e. this week's population is (partly) inside a live A/B test, so a plain
    week-over-week comparison will conflate the treatment effect with organic
    movement. Detected from data, not hardcoded, so it still fires correctly
    against a future snapshot where a different week is the experiment week."""
    return any(
        u["cohort_week"] == str(week) and u.get("variant", "").strip()
        for u in users
    )


def compute_week_metrics(retention_rows, channel_by_user, week):
    week_rows = [r for r in retention_rows if int(r["cohort_week"]) == week]
    overall = {
        "day7": rate(week_rows, "day_7"),
        "break": rate(week_rows, "broke_streak_week1"),
        "n": len(week_rows),
    }
    by_channel = {}
    for ch in CHANNELS:
        ch_rows = [r for r in week_rows if channel_by_user.get(r["user_id"]) == ch]
        by_channel[ch] = {
            "day7": rate(ch_rows, "day_7"),
            "break": rate(ch_rows, "broke_streak_week1"),
            "n": len(ch_rows),
        }
    return {"overall": overall, "by_channel": by_channel}


def pts(delta):
    """Round a fractional delta to whole percentage points."""
    return round(delta * 100)


def arrow(delta_pts):
    if delta_pts == 0:
        return "→ flat"
    if delta_pts < 0:
        return f"↓ {abs(delta_pts)}pt{'s' if abs(delta_pts) != 1 else ''}"
    return f"↑ {delta_pts}pt{'s' if delta_pts != 1 else ''}"


def pct(x):
    return f"{round(x * 100)}%" if x is not None else "n/a"


def build_digest(this_week, last_week, run_date, experiment_note=None):
    day7_now = this_week["overall"]["day7"]
    day7_prev = last_week["overall"]["day7"]
    day7_delta = pts(day7_now - day7_prev) if (day7_now is not None and day7_prev is not None) else 0

    break_now = this_week["overall"]["break"]
    break_prev = last_week["overall"]["break"]
    break_delta = pts(break_now - break_prev) if (break_now is not None and break_prev is not None) else 0

    day7_alert = abs(day7_delta) >= ALERT_THRESHOLD_PTS
    break_alert = abs(break_delta) >= ALERT_THRESHOLD_PTS

    lines = []
    lines.append(f"\U0001F4CA Streakly Retention Pulse, {run_date.strftime('%a %b %-d')}")
    if experiment_note:
        lines.append(f"⚠️ {experiment_note}")
    lines.append("")
    alert_tag = " ⚠️ ALERT" if day7_alert else ""
    lines.append(f"Day-7 retention: {pct(day7_now)} ({arrow(day7_delta)} vs last week){alert_tag}")
    lines.append(f"(baseline: {pct(BASELINE_DAY7)})")
    lines.append("")
    lines.append("By channel:")

    channel_deltas = {}
    for ch in CHANNELS:
        now = this_week["by_channel"][ch]["day7"]
        prev = last_week["by_channel"][ch]["day7"]
        d = pts(now - prev) if (now is not None and prev is not None) else 0
        channel_deltas[ch] = d
        watch = "  ← watch this" if abs(d) >= ALERT_THRESHOLD_PTS else ""
        lines.append(f"  {ch.capitalize()}: {pct(now)} ({arrow(d)}){watch}")

    lines.append("")
    break_alert_tag = " ⚠️ ALERT" if break_alert else ""
    lines.append(f"Streak-break rate: {pct(break_now)} ({arrow(break_delta)} vs last week){break_alert_tag}")
    lines.append("By channel:")
    for ch in CHANNELS:
        now = this_week["by_channel"][ch]["break"]
        prev = last_week["by_channel"][ch]["break"]
        d = pts(now - prev) if (now is not None and prev is not None) else 0
        watch = "  ← watch this" if abs(d) >= ALERT_THRESHOLD_PTS else ""
        lines.append(f"  {ch.capitalize()}: {pct(now)} ({arrow(d)}){watch}")

    lines.append("")
    top_channel = max(channel_deltas, key=lambda c: abs(channel_deltas[c]))
    top_delta = channel_deltas[top_channel]
    if abs(top_delta) >= ALERT_THRESHOLD_PTS:
        direction = "drop accelerating" if top_delta < 0 else "notable improvement"
        action = " Check campaign changes from last week." if top_delta < 0 else ""
        lines.append(f"Top signal: {top_channel.capitalize()} channel {direction}.{action}")
    else:
        lines.append("Top signal: no channel moved past threshold this week.")

    lines.append("")
    lines.append("Next: run anomaly diagnosis? Reply YES to trigger.")

    return "\n".join(lines), {
        "day7_now": day7_now, "day7_delta_pts": day7_delta, "day7_alert": day7_alert,
        "break_now": break_now, "break_delta_pts": break_delta, "break_alert": break_alert,
        "channel_deltas_pts": channel_deltas,
    }


def post_to_slack(webhook_url, text):
    req = urllib.request.Request(
        webhook_url,
        data=json.dumps({"text": text}).encode(),
        headers={"Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as resp:
        return resp.status


def main():
    parser = argparse.ArgumentParser(description="Streakly metric pulse agent")
    parser.add_argument("--users", default="../data/users.csv")
    parser.add_argument("--retention", default="../data/retention.csv")
    parser.add_argument("--post", action="store_true", help="Actually post to Slack (default: dry run, prints only)")
    parser.add_argument("--json", action="store_true", help="Also print the raw computed metrics as JSON")
    parser.add_argument("--week", type=int, default=None,
                         help="Treat this cohort_week as 'this week' instead of the latest one present "
                              "(for backtesting / demoing against a specific past week)")
    parser.add_argument("--chain-anomaly", action="store_true",
                         help="If either alert fires, immediately run anomaly_diagnosis.py's 5-step loop "
                              "using the real per-channel + streak-break-rate decomposition already "
                              "computed here. No-op if neither alert fired - this is the 'only triggers "
                              "on alert' chaining, not an unconditional second run.")
    parser.add_argument("--outcome-log", default=None,
                         help="Passed through to anomaly_diagnosis.py if --chain-anomaly fires")
    args = parser.parse_args()

    base_dir = os.path.dirname(os.path.abspath(__file__))
    users_path = os.path.join(base_dir, args.users)
    retention_path = os.path.join(base_dir, args.retention)

    users = load_csv(users_path)
    retention = load_csv(retention_path)
    channel_by_user = {u["user_id"]: u["acquisition_channel"] for u in users}

    this_week_id = args.week if args.week is not None else latest_week(retention)
    last_week_id = this_week_id - 1

    this_week = compute_week_metrics(retention, channel_by_user, this_week_id)
    last_week = compute_week_metrics(retention, channel_by_user, last_week_id)

    experiment_note = None
    if has_active_experiment(users, this_week_id):
        experiment_note = (
            f"Note: cohort_week {this_week_id} includes an active A/B test. "
            "Movement below blends the treatment effect with organic change - "
            "see 05-decide/metric-findings.md before treating this as a pure "
            "organic signal."
        )
    elif has_active_experiment(users, last_week_id):
        experiment_note = (
            f"Note: last week (cohort_week {last_week_id}) included an active "
            "A/B test. This week's comparison is against a treatment-mixed "
            "baseline, not a clean prior week."
        )

    digest, metrics = build_digest(this_week, last_week, date.today(), experiment_note)

    print(digest)

    if args.json:
        print("\n--- raw metrics (--json) ---")
        print(json.dumps(metrics, indent=2))

    if args.post:
        webhook = os.environ.get("SLACK_WEBHOOK_URL")
        if not webhook:
            print("\n[ERROR] --post given but SLACK_WEBHOOK_URL is not set. Nothing posted.", file=sys.stderr)
            sys.exit(1)
        status = post_to_slack(webhook, digest)
        print(f"\n[posted to Slack, status {status}]")

    if args.chain_anomaly:
        if not (metrics["day7_alert"] or metrics["break_alert"]):
            print("\n[--chain-anomaly: neither alert fired, anomaly_diagnosis not triggered]")
        else:
            import anomaly_diagnosis as ad
            outcome_log = args.outcome_log or os.path.join(base_dir, "../outcome-log.md")
            # Real decomposition: streak-break rate plus each channel's Day-7 rate,
            # since that IS the actual metric tree this data supports - unlike the
            # simulated scenarios, real data here has no push-opt-in or sessions
            # fields, so generate_hypotheses() will have much less to work with.
            # See agents/anomaly-diagnosis.md for why Step 3 is a heuristic stand-in.
            drivers = {"streak_break_rate": {"before": round(last_week["overall"]["break"] * 100, 1),
                                              "after": round(this_week["overall"]["break"] * 100, 1)}}
            for ch in CHANNELS:
                drivers[f"channel_{ch}"] = {
                    "before": round(last_week["by_channel"][ch]["day7"] * 100, 1),
                    "after": round(this_week["by_channel"][ch]["day7"] * 100, 1),
                }
            metric_name = "day7_retention" if metrics["day7_alert"] else "streak_break_rate"
            before = last_week["overall"]["day7"] if metrics["day7_alert"] else last_week["overall"]["break"]
            after = this_week["overall"]["day7"] if metrics["day7_alert"] else this_week["overall"]["break"]
            print("\n[--chain-anomaly: alert fired, running anomaly_diagnosis]\n")
            status, text = ad.run_diagnosis(metric_name, before, after, drivers, outcome_log)
            print(text)
            print(f"\n[anomaly_diagnosis status: {status}]")


if __name__ == "__main__":
    main()
