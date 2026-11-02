# PM Sprint Status Agent — LLM-as-Judge Evaluation

Nov 1, 2026

## Verdict

The agent's reports score **3.88 / 5** on average: 3 of 6 weeks pass, 2 pass with edits and 1 fails (Sep 25). The numbers are almost always right (24 of 28 deterministic checks pass); the failures come from **lookahead** (using facts the agent could not have known on the report date) and from **plans that contradict their own numbers**.

- **Strongest:** the three most recent weeks (Oct 9, Oct 16, Oct 23) score 4.25 to 4.40. Every day count, point total and velocity figure checked out against the snapshots.
- **Weakest:** the two Sprint 40 reports (Sep 18, Sep 25) reference Sprint 41 planning, ATL-108 and the Apple entitlement before any of them appear on the board.
- **One decision-relevant error:** the Oct 23 report caps Sprint 43 at 23 pts, then lists 28 pts of work in priority order and leaves out the ATL-119 consent screen.

Not evaluated: the live n8n agent's tool use and approval flow. The n8n trial is expired, so this evaluation scores the report outputs the pipeline produced on the Atlas data.

## Method

Two passes ran on each of the 6 weekly Atlas reports (Sep 18 to Oct 23), using only the snapshots dated on or before each report as the allowed facts.

1. **Deterministic checks (28):** `ground_truth.py` recomputed ground truth from `jira_mock.md`; `det_checks.py` compared every number in the narratives (points, %, days blocked, velocity, days to GA) against it.
2. **Blind LLM judge:** a separate Claude Opus instance, which did not see the deterministic results, extracted every claim, labelled it Supported / Contradicted / Unsupported / Lookahead, listed missed risks and scored 7 criteria from 1 to 5 using `judge_prompt.md`.

| Criterion | Weight | What a 5 means |
| --- | --- | --- |
| Factual accuracy | 25% | No contradicted claims |
| Risk coverage | 20% | Every HIGH risk surfaced and ranked correctly |
| Grounding | 15% | Every claim traceable to the snapshot as of that date |
| Actionability | 15% | Each action has an owner, a date and a concrete step |
| RAG calibration | 10% | Status and headline tone match the data |
| Clarity | 10% | An exec gets it from the headline and first bullet |
| Internal consistency | 5% | Plans and asks agree with the report's own numbers |

Pass = weighted score of 4.0 or more and no contradicted claim. Fail = below 3.0, or a contradicted claim that changes a decision.

## Scores by week

Quality rose steadily once blockers and history appeared in the data; grounding and consistency are where points were lost.

| Week | Sprint | Accuracy | Grounding | Risk | Action | RAG | Consistency | Clarity | Weighted | Det. checks | Verdict |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Oct 23 | S42 close | 3 | 5 | 5 | 5 | 5 | 2 | 4 | 4.25 | 7/8 | Pass with edits |
| Oct 16 | S42 mid | 5 | 4 | 4 | 4 | 5 | 4 | 4 | 4.35 | 6/6 | Pass |
| Oct 9 | S41 close | 5 | 5 | 4 | 4 | 4 | 4 | 4 | 4.40 | 4/4 | Pass |
| Oct 2 | S41 mid | 5 | 4 | 4 | 4 | 4 | 5 | 4 | 4.30 | 3/3 | Pass |
| Sep 25 | S40 close | 3 | 1 | 3 | 3 | 4 | 2 | 4 | 2.85 | 2/4 | **Fail** |
| Sep 18 | S40 mid | 3 | 2 | 3 | 3 | 4 | 4 | 4 | 3.10 | 2/3 | Pass with edits |

The two passes agreed on every error the deterministic checks caught; the judge also found the Sep 18 lookahead and the Sep 25 sizing contradiction, which the checks did not cover.

## Errors found

Six errors across the six reports; three are lookahead, two are plans that contradict the report's own numbers, one is a miscount.

| Week | Type | Claim in the report | What the data shows |
| --- | --- | --- | --- |
| Oct 23 | Contradicted | Commit Sprint 43 at 23 pts or less, in order ATL-121, 122, 115, 112, 117, 116 | That list totals 28 pts (3+2+5+5+5+8); with the 4-pt bug buffer only 19 pts fit. ATL-119 consent screen, a release gate, is missing |
| Sep 25 | Lookahead | Sprint 41 is planned at 50 pts; ask to trim it from 50 to 30 | Sprint 41 planning was Mon Sep 28; the 50-pt commit was not known on Sep 25 |
| Sep 25 | Lookahead | Procurement ask for the VeriID contract (ATL-108) | ATL-108 and VeriID first appear in the Oct 2 snapshot |
| Sep 25 | Inconsistent | Action says size Sprint 41 at 18-20 pts | The ask in the same report says about 30 pts |
| Sep 18 | Contradicted | Five stories are in progress | Four are: ATL-101, 102, 103, 105 |
| Sep 18 | Lookahead | Apple entitlement risk on ATL-101, submit by Sep 21 | The entitlement dependency first appears on Oct 2 (a reasonable domain guess, but not in the data) |

The lookahead errors point to how the narratives were produced: written with the full six-week file in context, not one week at a time.

## Missed risks

The most consistent gap is the release: reports before Oct 16 never connect sprint slippage to the Nov 6 GA date.

| Week | Risk the report did not surface |
| --- | --- |
| Oct 23 | ATL-123 beta bug left out of the Sprint 43 plan; average velocity not updated to 18.3 pts after Sprint 42 closed at 10, so the 23-pt cap is still too high |
| Oct 16 | The report suggests deferring ATL-122 feature-flag config, yet its own fallbacks (consent copy and English-only behind the flag) depend on it; no statement of impact on GA |
| Oct 9 | No release view; ATL-115 E2E tests not started after 11 days; a 25-pt cap with 23 pts already carried leaves about 2 pts of new work |
| Oct 2 | All 16 of Lena's open pts are blocked and no reassignment is proposed; ATL-101 is 7 days overdue |
| Sep 25 | ATL-101 passed its Sep 25 due date with no ETA; no view of the Nov 6 release |
| Sep 18 | Omar holds 10 of 32 open pts and ATL-106 (High) is not started; 11 pts not started at the midpoint |

## Fixes to the agent

Five changes would clear every error and most missed risks; the first two matter most.

1. **Cut the context at the report date.** Give the narrative step only snapshots on or before that Friday, and exclude sprint rows whose planning date is later. This removes all three lookahead errors.
2. **Compute plan totals in code, not in the narrative.** When an action proposes a capacity cap and a priority list, have `analyze.py` sum the list and refuse or trim it if it exceeds the cap. Also refresh average velocity at sprint close so the next plan uses it.
3. **Add a release-impact line to every report.** Days to GA, open release-gate items and whether they fit remaining capacity. The data already has the GA date and gate notes.
4. **Act on every flag.** The analysis step did flag Lena's load on Oct 2, but the narrative gave it no action; require a specific action for every HIGH or Load flag, such as a reassignment.
5. **Count statuses from the data.** Inject status counts (e.g. in progress: 4) into the prompt so phrases like "five stories" come from computed values.

## Reusing the eval

```bash
python3 eval/ground_truth.py jira_mock.md eval/reports.json
python3 eval/det_checks.py eval/reports.json pm_agent/narratives.json   # writes eval/det_results.json
```

- `judge_prompt.md`: rubric and JSON output schema for the LLM judge. `judge_results.json`: this run's six judgments.
- **In n8n:** after `generate_weekly_report`, add an Anthropic node with `judge_prompt.md` as the system prompt and that week's snapshots, computed metrics and narrative as input. Route Fail to the existing approval step instead of publishing.
- **Use a different model as judge** than the generator (the agent runs Sonnet 5.5; this run judged with Opus) to reduce self-preference.

Limits: one judge run per week, no repeated sampling, so scores near a threshold (Sep 18 at 3.10) could move by a point. The live agent's tool calls and approval flow were not tested because the n8n trial is expired. The Phoenix sample report was not scored; its source snapshots are in the n8n data table, not in this repo.
