"""PM Sprint Status Agent - analysis step.

Parses jira_mock.md (weekly Jira snapshots) and computes, for every snapshot week:
sprint health, velocity, week-over-week deltas, blockers, carry-overs, review stalls,
overdue items, scope change, per-person load, risk flags and an overall RAG status.

Usage: python3 analyze.py jira_mock.md reports.json
"""
import json
import re
import sys
from datetime import date, timedelta

SEV_ORDER = {"HIGH": 0, "MEDIUM": 1, "LOW": 2}


def d(s):
    return date.fromisoformat(s)


def split_row(line):
    cells = re.split(r"(?<!\\)\|", line.strip())[1:-1]
    return [c.strip().replace("\\|", "|") for c in cells]


def parse_table(lines, i):
    """Parse a markdown table starting at lines[i] (header). Returns (rows, next_index)."""
    header = split_row(lines[i])
    rows = []
    i += 2  # skip separator
    while i < len(lines) and lines[i].strip().startswith("|"):
        rows.append(dict(zip(header, split_row(lines[i]))))
        i += 1
    return rows, i


def parse(path):
    lines = open(path).read().splitlines()
    sprints, snaps, release = {}, [], None
    i = 0
    while i < len(lines):
        ln = lines[i]
        m_rel = re.match(r"\| Release \| .*?(\d{4}-\d{2}-\d{2})", ln)
        if m_rel:
            release = m_rel.group(1)
        if ln.startswith("## Sprints"):
            j = i + 1
            while not lines[j].startswith("|"):
                j += 1
            rows, i = parse_table(lines, j)
            for r in rows:
                c = r["Committed at planning (pts)"]
                sprints[r["Sprint"]] = dict(start=r["Start"], end=r["End"], goal=r["Goal"],
                                            committed=int(c) if c.isdigit() else None)
            continue
        m = re.match(r"## Snapshot (\d+) - (\d{4}-\d{2}-\d{2}) \((Sprint \d+), (.+)\)", ln)
        if m:
            j = i + 1
            while not lines[j].startswith("|"):
                j += 1
            rows, i = parse_table(lines, j)
            for r in rows:
                r["Pts"] = int(r["Pts"])
                r["Sprints"] = [s.strip() for s in r["Sprints"].split(",")]
                r["Notes"] = "" if r["Notes"] == "-" else r["Notes"]
            snaps.append(dict(n=int(m.group(1)), date=m.group(2), sprint=m.group(3), kind=m.group(4), issues=rows))
            continue
        i += 1
    return sprints, snaps, release


def workdays(a, b):
    """Weekdays from a to b inclusive."""
    n, x = 0, a
    while x <= b:
        if x.weekday() < 5:
            n += 1
        x += timedelta(days=1)
    return n


def analyze(sprints, snaps, release):
    reports = []
    velocity = {}  # sprint -> done pts at close
    by_key_hist = {}  # key -> list of (date, status, sprint)
    for s in snaps:
        for it in s["issues"]:
            by_key_hist.setdefault(it["Key"], []).append((s["date"], it["Status"], s["sprint"]))

    for idx, s in enumerate(snaps):
        sd = d(s["date"])
        sp = sprints[s["sprint"]]
        prev = snaps[idx - 1] if idx > 0 else None
        issues = s["issues"]
        scope = sum(i["Pts"] for i in issues)
        done = [i for i in issues if i["Status"] == "Done"]
        done_pts = sum(i["Pts"] for i in done)
        open_ = [i for i in issues if i["Status"] != "Done"]
        elapsed = workdays(d(sp["start"]), min(sd, d(sp["end"]))) / workdays(d(sp["start"]), d(sp["end"]))
        added = [i for i in issues if i["Added"] == "mid-sprint"]
        is_close = s["kind"] == "sprint close"
        if is_close:
            velocity[s["sprint"]] = done_pts
        prior_vel = {k: v for k, v in velocity.items() if k != s["sprint"]}
        avg_vel = round(sum(prior_vel.values()) / len(prior_vel), 1) if prior_vel else None

        def days_in(i):
            return (sd - d(i["Status since"])).days

        blocked = [dict(key=i["Key"], summary=i["Summary"], owner=i["Assignee"], pts=i["Pts"], prio=i["Priority"],
                        days=days_in(i), note=i["Notes"], sprints=i["Sprints"]) for i in open_ if i["Status"] == "Blocked"]
        prev_blocked = {i["Key"] for i in prev["issues"] if i["Status"] == "Blocked"} if prev else set()
        now_blocked = {b["key"] for b in blocked}
        for b in blocked:
            b["new"] = b["key"] not in prev_blocked
        resolved_blockers = sorted(prev_blocked - now_blocked) if prev else []
        review_stalls = [i for i in open_ if i["Status"] == "In Review" and days_in(i) >= 5]
        not_started = [i for i in open_ if i["Status"] == "To Do" and days_in(i) >= 7]
        carry = [i for i in open_ if len(i["Sprints"]) > 1]
        overdue = [i for i in open_ if d(i["Due"]) < sd]
        prev_done_keys = {i["Key"] for i in prev["issues"] if i["Status"] == "Done"} if prev else set()
        completed = [dict(key=i["Key"], summary=i["Summary"], owner=i["Assignee"], pts=i["Pts"], type=i["Type"])
                     for i in done if i["Key"] not in prev_done_keys or (prev and prev["sprint"] != s["sprint"])]
        completed = [c for c in completed if c["key"] not in prev_done_keys]

        load = {}
        for i in open_:
            p = load.setdefault(i["Assignee"], dict(open_pts=0, blocked_pts=0, items=0))
            p["open_pts"] += i["Pts"]
            p["items"] += 1
            if i["Status"] == "Blocked":
                p["blocked_pts"] += i["Pts"]

        status_counts = {}
        for i in issues:
            status_counts[i["Status"]] = status_counts.get(i["Status"], 0) + i["Pts"]

        # ---------- risk flags (merged per issue) ----------
        flags = {}

        def flag(key, sev, typ, detail, owner, summary=""):
            f = flags.setdefault(key, dict(issue=key, summary=summary, sev=sev, types=[], details=[], owner=owner))
            if SEV_ORDER[sev] < SEV_ORDER[f["sev"]]:
                f["sev"] = sev
            f["types"].append(typ)
            f["details"].append(detail)

        for b in blocked:
            sev = "HIGH" if b["days"] >= 7 or b["prio"] == "Highest" else "MEDIUM"
            flag(b["key"], sev, "Blocker", f"Blocked {b['days']} days: {b['note']}", b["owner"], b["summary"])
        for i in review_stalls:
            flag(i["Key"], "HIGH" if days_in(i) >= 10 else "MEDIUM", "Review stall",
                 f"In Review for {days_in(i)} days. {i['Notes']}".strip(), i["Assignee"], i["Summary"])
        for i in not_started:
            flag(i["Key"], "HIGH" if len(i["Sprints"]) > 1 and i["Priority"] in ("High", "Highest") else "MEDIUM",
                 "Not started", f"To Do for {days_in(i)} days", i["Assignee"], i["Summary"])
        for i in carry:
            flag(i["Key"], "HIGH" if len(i["Sprints"]) >= 3 else "MEDIUM", "Carry-over",
                 f"In sprint {len(i['Sprints'])} ({', '.join(i['Sprints'])})", i["Assignee"], i["Summary"])
        for i in overdue:
            flag(i["Key"], "MEDIUM", "Overdue", f"Due {i['Due']} ({(sd - d(i['Due'])).days} days late)",
                 i["Assignee"], i["Summary"])

        team_flags = []
        if avg_vel and sp["committed"] and sp["committed"] > 1.2 * avg_vel:
            team_flags.append(dict(issue="-", summary="Sprint commitment", sev="HIGH" if sp["committed"] > 1.6 * avg_vel else "MEDIUM",
                                   types=["Over-commitment"], owner="PM / Team",
                                   details=[f"{sp['committed']} pts committed vs {avg_vel} pts average velocity"]))
        if added:
            ap = sum(i["Pts"] for i in added)
            team_flags.append(dict(issue="-", summary="Scope change", sev="MEDIUM" if ap < 0.2 * (sp["committed"] or scope) else "HIGH",
                                   types=["Scope creep"], owner="PM",
                                   details=[f"+{ap} pts added mid-sprint ({', '.join(i['Key'] for i in added)})"]))
        gap = elapsed * 100 - (done_pts / scope * 100)
        if gap >= 20:
            team_flags.append(dict(issue="-", summary="Burndown", sev="HIGH" if gap >= 40 else "MEDIUM", types=["Burndown"],
                                   owner="PM", details=[f"{round(done_pts / scope * 100)}% done vs {round(elapsed * 100)}% of sprint elapsed"]))
        for who, p in load.items():
            if p["blocked_pts"] and p["blocked_pts"] >= 0.6 * p["open_pts"] and p["open_pts"] >= 5:
                team_flags.append(dict(issue="-", summary="Load", sev="MEDIUM", types=["Load"], owner="PM",
                                       details=[f"{who}: {p['blocked_pts']} of {p['open_pts']} open pts are blocked"]))
            elif p["open_pts"] >= 13:
                team_flags.append(dict(issue="-", summary="Load", sev="MEDIUM", types=["Load"], owner="PM",
                                       details=[f"{who} holds {p['open_pts']} open pts"]))

        all_flags = sorted(flags.values(), key=lambda f: (SEV_ORDER[f["sev"]], f["issue"])) + \
            sorted(team_flags, key=lambda f: SEV_ORDER[f["sev"]])

        # ---------- RAG ----------
        done_pct = done_pts / scope * 100
        long_blockers = [b for b in blocked if b["days"] >= 7]
        if is_close:
            rag = "RED" if done_pct < 50 else "AMBER" if (done_pct < 80 or blocked) else "GREEN"
        else:
            rag = "RED" if (long_blockers and gap >= 30) else "AMBER" if (blocked or gap >= 15 or len(carry) >= 2) else "GREEN"

        # ---------- timelines for stuck items ----------
        stuck = []
        for i in carry + [x for x in review_stalls if x not in carry] + [x for x in not_started if x not in carry]:
            hist = [h for h in by_key_hist[i["Key"]] if h[0] <= s["date"]]
            stuck.append(dict(key=i["Key"], summary=i["Summary"], owner=i["Assignee"], pts=i["Pts"],
                              sprints=i["Sprints"], timeline=[dict(date=h[0], status=h[1]) for h in hist]))

        reports.append(dict(
            week=s["date"], snapshot=s["n"], sprint=s["sprint"], kind=s["kind"], sprint_start=sp["start"],
            sprint_end=sp["end"], sprint_goal=sp["goal"], release=release,
            days_to_release=(d(release) - sd).days if release else None,
            committed=sp["committed"], scope=scope, scope_added=sum(i["Pts"] for i in added),
            added_keys=[i["Key"] for i in added], done_pts=done_pts, done_pct=round(done_pct),
            elapsed_pct=round(elapsed * 100), items_total=len(issues), items_open=len(open_),
            status_pts=status_counts, avg_velocity=avg_vel, velocity=dict(velocity),
            blocked=blocked, resolved_blockers=resolved_blockers,
            carry_open=[i["Key"] for i in carry], review_stalls=[i["Key"] for i in review_stalls],
            not_started=[i["Key"] for i in not_started], overdue=[i["Key"] for i in overdue],
            completed=completed, load=load, flags=all_flags, stuck=stuck, rag=rag,
            open_issues=[dict(key=i["Key"], summary=i["Summary"], status=i["Status"], owner=i["Assignee"],
                              pts=i["Pts"], prio=i["Priority"], due=i["Due"]) for i in open_],
        ))

    # week-over-week deltas
    for idx, r in enumerate(reports):
        p = reports[idx - 1] if idx else None
        r["prev"] = None if not p else dict(week=p["week"], sprint=p["sprint"], done_pts=p["done_pts"],
                                            done_pct=p["done_pct"], scope=p["scope"], blocked=len(p["blocked"]),
                                            carry=len(p["carry_open"]), items_open=p["items_open"], rag=p["rag"])
        r["trend"] = dict(weeks=[x["week"] for x in reports[: idx + 1]],
                          blocked=[len(x["blocked"]) for x in reports[: idx + 1]],
                          carry=[len(x["carry_open"]) for x in reports[: idx + 1]],
                          done_pct=[x["done_pct"] for x in reports[: idx + 1]],
                          rag=[x["rag"] for x in reports[: idx + 1]])
    return reports


if __name__ == "__main__":
    src, dst = sys.argv[1], sys.argv[2]
    sprints, snaps, release = parse(src)
    reps = analyze(sprints, snaps, release)
    json.dump(reps, open(dst, "w"), indent=1)
    for r in reps:
        print(r["week"], r["sprint"], r["kind"], r["rag"], f"done {r['done_pts']}/{r['scope']} ({r['done_pct']}% vs {r['elapsed_pct']}% elapsed)",
              "blocked", [(b["key"], b["days"]) for b in r["blocked"]], "carry", r["carry_open"],
              "avg_vel", r["avg_velocity"], "flags", len(r["flags"]))
