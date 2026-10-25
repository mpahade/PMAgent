# PM Sprint Status Agent

A project-management agent that reviews weekly Jira snapshots and produces a weekly sprint status report: RAG status, sprint health, risk flags with recommended actions, blockers, stuck items, trends and asks.

The data is **synthetic**: a demo project, "Atlas - Mobile Onboarding v2", with 23 issues across three 2-week sprints and six weekly snapshots (Sep 18 – Oct 23, 2026). People, vendors and PR numbers are fictional.

## Files

| Path | What it is |
|---|---|
| `jira_mock.md` | Mock Jira data: project, team, sprints, and one table per weekly snapshot |
| `gen_jira_mock.py` | Script that generates `jira_mock.md` (edit it to change the scenario) |
| `pm_agent/analyze.py` | Parses the snapshots and computes metrics, risk flags and RAG for every week |
| `pm_agent/narratives.json` | The agent's judgment for each week: headline, summary, recommended actions, asks |
| `pm_agent/template.html` | Report page template with a week switcher |
| `pm_agent/build.py` | Combines metrics + narratives into the final report page |
| `atlas_status.html` | The built report. Open it in any browser |

## How it works

1. **Analyze**: `analyze.py` computes the numbers deterministically, so the figures are always traceable to the data:
   done vs scope vs time elapsed, velocity, mid-sprint scope adds, blockers (days blocked, new vs resolved), review stalls, not-started work, carry-overs, overdue items, per-person load, and a RAG status.
2. **Judge**: the agent (Claude) reads the computed week and writes the narrative into `narratives.json`: what matters, recommended actions per risk, and named asks with dates.
3. **Render**: `build.py` produces a single self-contained HTML report.

## Run it

```bash
python3 gen_jira_mock.py                       # optional: regenerate the mock data
python3 pm_agent/analyze.py jira_mock.md reports.json
python3 pm_agent/build.py pm_agent/template.html reports.json pm_agent/narratives.json atlas_status.html
```

Requires Python 3.9+, no extra packages. To report on a new week, append a snapshot to `jira_mock.md`, rerun `analyze.py`, add that week's entry to `narratives.json`, then rebuild.

### RAG rules
- **Sprint close:** RED if done < 50%; AMBER if done < 80% or anything is blocked; otherwise GREEN.
- **Mid-sprint:** RED if a blocker is 7+ days old and done % trails elapsed % by 30+ points; AMBER if anything is blocked, the gap is 15+ points, or 2+ items carried over; otherwise GREEN.
