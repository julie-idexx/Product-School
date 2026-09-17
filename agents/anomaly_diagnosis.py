#!/usr/bin/env python3
"""
Streakly Anomaly Diagnosis Agent

Chained off metric_pulse.py: only meant to run when metric_pulse's Day-7
retention or streak-break-rate alert has already fired (see
metric_pulse.py's --chain-anomaly flag). Runs a 5-step loop with an
explicit stop condition at each step, so a shaky signal never gets posted
to Slack dressed up as a finished diagnosis.

Honesty note on Step 3 (hypothesis generation): generating real hypotheses
is a reasoning task, not a data computation - a cron job can't actually do
it. generate_hypotheses() below is a deterministic heuristic that scores a
small set of candidate causes against which drivers moved. It's good enough
to test the loop's mechanics and stop-conditions end to end (which is what
the simulated test in the spec verifies), but it is NOT a substitute for a
real reasoning step. In production this function is where a real LLM call
(the same kind of reasoning a PM/Claude already did by hand in
05-decide/metric-findings.md and data/metric-diagnosis.md for the real
week-5 pilot) belongs instead.
"""

import argparse
import json
import os
from datetime import date, datetime

ALERT_THRESHOLD_PTS = 2
HYPOTHESIS_CONFIDENCE_THRESHOLD = 6

METRIC_DISPLAY_NAMES = {
    "day7_retention": "Day-7 retention",
    "streak_break_rate": "Streak-break rate",
}


def display_name(metric_name):
    return METRIC_DISPLAY_NAMES.get(metric_name, metric_name.replace("_", " ").title())


def format_time(run_dt):
    return run_dt.strftime("%a %b %-d, %-I:%M") + run_dt.strftime("%p").lower()

# name -> (unit, meaningful-move threshold). unit "pct_relative" means the
# threshold is a percent change relative to the "before" value, not points.
DRIVER_SPECS = {
    "streak_break_rate": ("pts", 2),
    "sessions_week1": ("pct_relative", 10),
    "push_optin_rate": ("pts", 2),
}


# ---------------------------------------------------------------- Step 1

def step1_threshold_check(metric_name, before, after):
    delta_pts = round((after - before) * 100) if abs(after) <= 1 and abs(before) <= 1 else round(after - before)
    passed = abs(delta_pts) >= ALERT_THRESHOLD_PTS
    verdict = "CONTINUE" if passed else "STOP - log only, no diagnosis needed"
    log_line = f"Step 1 (threshold check): {metric_name} moved {delta_pts:+d}pts -> {verdict}"
    return passed, delta_pts, log_line


# ---------------------------------------------------------------- Step 2

def step2_decompose(drivers):
    """drivers: {name: {"before": x, "after": y}}. Returns (moved_names, passed, log_lines)."""
    moved = []
    lines = ["Step 2 (metric tree decomposition):"]
    detail = {}
    for name, d in drivers.items():
        unit, threshold = DRIVER_SPECS.get(name, ("pts", 2))
        before, after = d["before"], d["after"]
        if unit == "pct_relative":
            rel = ((after - before) / before) * 100 if before else 0
            meaningful = abs(rel) >= threshold
            tag = " [MOVED]" if meaningful else ""
            lines.append(f"  {name}: {before} -> {after} ({rel:+.0f}%){tag}")
            detail[name] = {"before": before, "after": after, "change": rel, "unit": "%", "moved": meaningful}
        else:
            # accept either fractions (0.22) or whole points (22) - same auto-detect as step1
            scale = 100 if (abs(before) <= 1 and abs(after) <= 1) else 1
            delta = (after - before) * scale
            before, after = before * scale, after * scale
            meaningful = abs(delta) >= threshold
            tag = " [MOVED]" if meaningful else ""
            lines.append(f"  {name}: {before} -> {after} ({delta:+.1f}pts){tag}")
            detail[name] = {"before": before, "after": after, "change": delta, "unit": "pts", "moved": meaningful}
        if meaningful:
            moved.append(name)

    passed = len(moved) >= 2
    verdict = ">= 2 drivers moved -> CONTINUE" if passed else "< 2 drivers moved -> INCONCLUSIVE, STOP"
    lines.append(f"Step 2 gate: {len(moved)} driver(s) moved meaningfully ({moved}). {verdict}")
    return moved, passed, lines, detail


# ---------------------------------------------------------------- Step 3 (heuristic stand-in)

def generate_hypotheses(detail):
    """Score 3 candidate causes against the decomposition. See module docstring:
    this is a deterministic stand-in for a real reasoning step, not the real thing."""

    push = detail.get("push_optin_rate", {})
    sessions = detail.get("sessions_week1", {})
    break_rate = detail.get("streak_break_rate", {})

    hyps = []

    # H1: push delivery issue - supported when push opt-in and sessions both dropped together
    push_drop = push.get("moved") and push.get("change", 0) < 0
    sess_drop = sessions.get("moved") and sessions.get("change", 0) < 0
    conf = 3
    if push_drop and sess_drop:
        conf = 8 if (abs(push.get("change", 0)) >= 3 and abs(sessions.get("change", 0)) >= 15) else 7
    elif push_drop or sess_drop:
        conf = 5
    hyps.append({
        "text": "Push notification delivery issue",
        "confidence": conf,
        "rationale": "correlates with session drop" if (push_drop and sess_drop) else "partial signal only",
    })

    # H2: cohort/channel quality shift - supported when streak-break rate itself moved a lot
    conf2 = 6 if break_rate.get("moved") and abs(break_rate.get("change", 0)) >= 5 else 4
    hyps.append({
        "text": "New user cohort quality shift (channel mix)",
        "confidence": conf2,
        "rationale": "streak-break rate moved sharply" if break_rate.get("moved") else "streak-break rate moved, but not sharply",
    })

    # H3: catch-all - a recent product/copy change, always the lowest-confidence, needs-confirmation option
    hyps.append({
        "text": "Streak-reset copy or notification-copy regression after the last deploy",
        "confidence": 3,
        "rationale": "no direct signal for this in the decomposition - needs confirmation, not ruled out",
    })

    hyps.sort(key=lambda h: h["confidence"], reverse=True)
    return hyps


# ---------------------------------------------------------------- Step 4

SQL_TEMPLATES = {
    "Push notification delivery issue": (
        "SELECT date, COUNT(*) AS push_sent, SUM(delivered) AS push_delivered,\n"
        "       AVG(opened) AS open_rate\n"
        "FROM streakly_notifications\n"
        "WHERE sent_date >= CURRENT_DATE - 7\n"
        "GROUP BY date\n"
        "ORDER BY date;"
    ),
    "New user cohort quality shift (channel mix)": (
        "SELECT acquisition_channel, COUNT(*) AS n,\n"
        "       AVG(CASE WHEN day_7 THEN 1 ELSE 0 END) AS day7_retention_rate\n"
        "FROM users u JOIN retention r ON r.user_id = u.user_id\n"
        "WHERE u.cohort_week IN (CURRENT_WEEK, CURRENT_WEEK - 1)\n"
        "GROUP BY acquisition_channel, u.cohort_week\n"
        "ORDER BY acquisition_channel, u.cohort_week;"
    ),
    "Streak-reset copy or notification-copy regression after the last deploy": (
        "SELECT deploy_id, deployed_at, description\n"
        "FROM deploys\n"
        "WHERE deployed_at >= CURRENT_DATE - 7\n"
        "ORDER BY deployed_at DESC;"
    ),
}


def sql_for_top_hypothesis(top_hyp):
    return SQL_TEMPLATES.get(top_hyp["text"], "-- no SQL template registered for this hypothesis")


# ---------------------------------------------------------------- Formatting

def format_full_diagnostic(metric_name, delta_pts, before_pct, after_pct, decomposition_lines, hyps, run_dt):
    lines = [f"\U0001F50D Streakly Anomaly Detected, {format_time(run_dt)}", ""]
    direction = "dropped" if delta_pts < 0 else "rose"
    lines.append(f"Trigger: {display_name(metric_name)} {direction} {abs(delta_pts)}pts "
                 f"({round(before_pct*100)}% → {round(after_pct*100)}%) overnight")
    lines.append("")
    lines.append("Metric tree decomposition:")
    lines += ["  " + l.strip() for l in decomposition_lines if l.strip().startswith(tuple("abcdefghijklmnopqrstuvwxyz")) or ":" in l and "Step" not in l]
    lines.append("")
    lines.append("Top 3 hypotheses:")
    likelihood = lambda c: "high likelihood" if c >= 7 else ("medium" if c >= 5 else "low")
    for i, h in enumerate(hyps, 1):
        lines.append(f"{i}. {h['text']} ({likelihood(h['confidence'])}, {h['rationale']}) — confidence {h['confidence']}/10")
    lines.append("")
    lines.append(f"SQL to confirm hypothesis 1:")
    lines.append("```")
    lines.append(sql_for_top_hypothesis(hyps[0]))
    lines.append("```")
    lines.append("")
    lines.append("Logged to outcome-log.md. Run this query and reply with the output. I'll interpret.")
    return "\n".join(lines)


def format_low_confidence(metric_name, delta_pts, decomposition_lines, hyps, run_dt):
    lines = [f"⚠️ Streakly Anomaly — Low Confidence, {format_time(run_dt)}", ""]
    direction = "dropped" if delta_pts < 0 else "rose"
    lines.append(f"Trigger: {display_name(metric_name)} {direction} {abs(delta_pts)}pts overnight")
    lines.append("")
    lines.append("Metric tree decomposition:")
    lines += ["  " + l.strip() for l in decomposition_lines if ":" in l and "Step" not in l]
    lines.append("")
    lines.append(f"Top hypothesis: {hyps[0]['text']} — confidence {hyps[0]['confidence']}/10 "
                  f"(below the {HYPOTHESIS_CONFIDENCE_THRESHOLD}/10 threshold)")
    lines.append("")
    lines.append("Stopping here rather than posting a guess. Logged to outcome-log.md — needs a human "
                  "look before this becomes a diagnosis.")
    return "\n".join(lines)


def format_inconclusive(metric_name, delta_pts, decomposition_lines, run_dt):
    lines = [f"❓ Streakly Anomaly — Inconclusive, {format_time(run_dt)}", ""]
    direction = "dropped" if delta_pts < 0 else "rose"
    lines.append(f"Trigger: {display_name(metric_name)} {direction} {abs(delta_pts)}pts overnight")
    lines.append("")
    lines.append("Metric tree decomposition:")
    lines += ["  " + l.strip() for l in decomposition_lines if ":" in l and "Step" not in l]
    lines.append("")
    lines.append("Only one driver moved meaningfully — not enough to decompose the cause. "
                  "Flagged inconclusive rather than guessing at a 1-driver story.")
    return "\n".join(lines)


# ---------------------------------------------------------------- Step 5

def log_outcome(path, run_dt, metric_name, delta_pts, hyps, status):
    header_exists = os.path.exists(path)
    with open(path, "a") as f:
        if not header_exists:
            f.write("# Outcome Log — Streakly Anomaly Diagnoses\n\n"
                    "*Every anomaly diagnosis run, its ranked hypotheses, and what actually turned out to be true. "
                    "Fill in \"What actually happened\" once confirmed — an unfilled row is an open loop, not a finished one.*\n\n")
        f.write(f"## {run_dt.strftime('%Y-%m-%d %H:%M')} — {metric_name} moved {delta_pts:+d}pts ({status})\n\n")
        if hyps:
            f.write("| Rank | Hypothesis | Confidence | What actually happened |\n")
            f.write("|---|---|---|---|\n")
            for i, h in enumerate(hyps, 1):
                f.write(f"| {i} | {h['text']} | {h['confidence']}/10 | _TBD_ |\n")
        f.write("\n")


# ---------------------------------------------------------------- Orchestration

def run_diagnosis(metric_name, before, after, drivers, outcome_log_path, run_dt=None):
    """The full 5-step loop. Returns (status, slack_text) where status is one of
    'stopped_below_threshold' | 'inconclusive' | 'low_confidence' | 'posted'."""
    run_dt = run_dt or datetime.now()

    passed1, delta_pts, log1 = step1_threshold_check(metric_name, before, after)
    if not passed1:
        return "stopped_below_threshold", log1

    moved, passed2, log2, detail = step2_decompose(drivers)
    if not passed2:
        text = format_inconclusive(metric_name, delta_pts, log2, run_dt)
        log_outcome(outcome_log_path, run_dt, metric_name, delta_pts, [], "inconclusive")
        return "inconclusive", text

    hyps = generate_hypotheses(detail)
    if hyps[0]["confidence"] <= HYPOTHESIS_CONFIDENCE_THRESHOLD:
        text = format_low_confidence(metric_name, delta_pts, log2, hyps, run_dt)
        log_outcome(outcome_log_path, run_dt, metric_name, delta_pts, hyps, "low_confidence")
        return "low_confidence", text

    text = format_full_diagnostic(metric_name, delta_pts, before, after, log2, hyps, run_dt)
    log_outcome(outcome_log_path, run_dt, metric_name, delta_pts, hyps, "posted")
    return "posted", text


def main():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    parser = argparse.ArgumentParser(description="Streakly anomaly diagnosis agent")
    parser.add_argument("--simulate", help="Path to a JSON file describing a synthetic scenario "
                                            "(see agents/anomaly-diagnosis.md for the shape)")
    parser.add_argument("--outcome-log", default=os.path.join(base_dir, "../outcome-log.md"))
    args = parser.parse_args()

    if not args.simulate:
        print("No --simulate scenario given. This script is meant to be called from metric_pulse.py's "
              "--chain-anomaly flag with real decomposition data, or with --simulate for testing.")
        return

    with open(args.simulate) as f:
        scenario = json.load(f)

    status, text = run_diagnosis(
        scenario["metric_name"], scenario["before"], scenario["after"],
        scenario["drivers"], args.outcome_log,
    )
    print(text)
    print(f"\n[status: {status}]")


if __name__ == "__main__":
    main()
