"""Deterministic checks: narrative numbers vs computed ground truth. Usage: python3 eval/det_checks.py eval/reports.json pm_agent/narratives.json"""
import json, sys
R = {r["week"]: r for r in json.load(open(sys.argv[1]))}
N = json.load(open(sys.argv[2]))

def blocked_days(r, k):
    return next((b["days"] for b in r["blocked"] if b["key"] == k), None)

checks = {
 "2026-09-18": [
  ("done 2 of 34 (6%)", lambda r: (r["done_pts"], r["scope"], r["done_pct"]) == (2, 34, 6)),
  ("'Five stories are in progress'", lambda r: r["status_pts"] and sum(1 for k in ["ATL-101","ATL-102","ATL-103","ATL-105"]) == 5),
  ("no blockers", lambda r: not r["blocked"]),
 ],
 "2026-09-25": [
  ("closed 18 of 34 (53%)", lambda r: (r["done_pts"], r["scope"], r["done_pct"]) == (18, 34, 53)),
  ("carrying 16 pts, 3 items", lambda r: r["open_pts"] == 16 and r["items_open"] == 3),
  ("Sprint 41 planned at 50 pts (known on Sep 25?)", lambda r: False),  # planning was Mon Sep 28
  ("ATL-108 referenced (not on board as of Sep 25)", lambda r: False),
 ],
 "2026-10-02": [
  ("5 of 50 (10%)", lambda r: (r["done_pts"], r["scope"], r["done_pct"]) == (5, 50, 10)),
  ("2.8x of 18-pt avg", lambda r: r["avg_velocity"] == 18.0 and round(50 / 18, 1) == 2.8),
  ("two blockers, both new", lambda r: len(r["blocked"]) == 2 and all(b["new"] for b in r["blocked"])),
 ],
 "2026-10-09": [
  ("27 pts, 54%", lambda r: (r["done_pts"], r["done_pct"]) == (27, 54)),
  ("best sprint so far", lambda r: r["velocity"]["Sprint 41"] > r["velocity"]["Sprint 40"]),
  ("ATL-108 blocked 9 days", lambda r: blocked_days(r, "ATL-108") == 9),
  ("carrying 23 pts, 4 items", lambda r: r["open_pts"] == 23 and r["items_open"] == 4),
 ],
 "2026-10-16": [
  ("5 of 46 (11%) vs 50% elapsed", lambda r: (r["done_pts"], r["scope"], r["done_pct"], r["elapsed_pct"]) == (5, 46, 11, 50)),
  ("22.5 avg velocity", lambda r: r["avg_velocity"] == 22.5),
  ("blockers 1 -> 3", lambda r: len(R["2026-10-09"]["blocked"]) == 1 and len(r["blocked"]) == 3),
  ("ATL-108 16 days", lambda r: blocked_days(r, "ATL-108") == 16),
  ("ATL-112 in review 8 days", lambda r: r["days_in_status"]["ATL-112"] == 8),
  ("ATL-115 not started 18 days", lambda r: r["days_in_status"]["ATL-115"] == 18),
 ],
 "2026-10-23": [
  ("10 of 51 (20%)", lambda r: (r["done_pts"], r["scope"], r["done_pct"]) == (10, 51, 20)),
  ("lowest of 3 sprints: 10 vs 18, 27", lambda r: r["velocity"] == {"Sprint 40": 18, "Sprint 41": 27, "Sprint 42": 10}),
  ("41 open pts, ~2x 22.5 avg", lambda r: r["open_pts"] == 41 and 1.7 < 41 / 22.5 < 2.0),
  ("GA in 14 days", lambda r: r["days_to_release"] == 14),
  ("ATL-108 23d, ATL-119 10d", lambda r: blocked_days(r, "ATL-108") == 23 and blocked_days(r, "ATL-119") == 10),
  ("ATL-112 15d review, ATL-115 25d", lambda r: r["days_in_status"]["ATL-112"] == 15 and r["days_in_status"]["ATL-115"] == 25),
  ("9 pts added mid-sprint", lambda r: r["scope_added"] == 9),
  ("Sprint 43 order fits the 23-pt cap (3+2+5+5+5+8)", lambda r: 3 + 2 + 5 + 5 + 5 + 8 <= 23),
 ],
}
out, tot, ok = {}, 0, 0
for w, cs in checks.items():
    res = []
    for name, fn in cs:
        try:
            passed = bool(fn(R[w]))
        except Exception as e:
            passed = False
        res.append(dict(check=name, passed=passed)); tot += 1; ok += passed
        print(("PASS " if passed else "FAIL ") + w + "  " + name)
    out[w] = res
print(f"\n{ok}/{tot} deterministic checks passed")
json.dump(out, open("eval/det_results.json", "w"), indent=1)
