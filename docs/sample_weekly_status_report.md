# Weekly Status Report - Phoenix - Checkout Revamp

**Sprint 42** (Oct 20 – Oct 31, 2026) · Week of **Oct 23, 2026** · Overall status: 🔴 **RED**

## 1. Executive summary
- **Sprint 42 is off track:** 4 of 49 committed points are done (8%), while ~27% of the sprint has elapsed. The team committed 213% of its average velocity (23 pts).
- **Biggest risk:** PHX-101 *Payment gateway 3DS2 integration* has been blocked for 18 days waiting on Stripe sandbox credentials. It is overdue (due Oct 17), has spanned 3 sprints, and now also blocks PHX-122 *Fraud scoring webhook*.
- **Since last week:** blockers went from 2 to 3 (PHX-122 is new; none were resolved), and items carried over from earlier sprints went from 2 to 4.
- **Help needed:** an exec escalation to Stripe for PHX-101, Legal sign-off for PHX-110, and a platform-team reviewer for PR #482 (PHX-107).

## 2. Sprint health
| Metric | This week | vs last week (Oct 16, Sprint 41 close) |
|---|---|---|
| Committed points | 49 | 52 |
| Done points | 4 (8%) | 25 (48%) |
| % of sprint elapsed | ~27% | - |
| Open items | 10 of 12 | 5 |
| Blocked items | 3 | 2 ▲ |
| Carried-over items (open, 2+ sprints) | 4 | 2 ▲ |
| Avg velocity (Sprints 40–41) | 23 pts | - |

## 3. Risk flags
| Severity | Type | Issue | Detail | Recommended action | Owner |
|---|---|---|---|---|---|
| HIGH | Blocker / Overdue / Carry-over | PHX-101 | 3DS2 integration blocked 18 days on vendor sandbox creds; due Oct 17; 3rd sprint | Escalate to the Stripe account manager via the Eng Director by Tue Oct 27; if there's no ETA by Thu, decide whether to descope 3DS2 from the release | Priya Shah / Eng Director |
| HIGH | Blocker | PHX-110 | EU VAT calc blocked 9 days on Legal sign-off for rounding rules | Book a 30-min decision meeting with Legal by Tue Oct 27; build against the proposed rule behind a flag | Ana Gomez / PM |
| HIGH | Carry-over | PHX-107 | Cart multi-currency refactor in its 3rd sprint; PR #482 in review for 10 days | Platform lead to assign a reviewer today; set a 48h review SLA | Dev Patel / Platform lead |
| HIGH | Over-commitment | - | 49 pts committed vs 23 pts average velocity | Re-plan at Monday stand-up: move ~20 pts (e.g. PHX-131, PHX-127) to Sprint 43 | PM / Team |
| MEDIUM | Blocker | PHX-122 | Fraud scoring webhook depends on PHX-101 | Start with stubbed 3DS2 responses so the work can begin before PHX-101 clears | Priya Shah |
| MEDIUM | Carry-over | PHX-110 | Spanned 2 sprints (Sprint 41 to 42) | See the Legal action above | Ana Gomez |
| MEDIUM | Carry-over | PHX-115 | Load test still To Do after 18 days, 2nd sprint | Pull it into this week; it's a release gate before Oct 31 | Tom Okafor |
| MEDIUM | Burndown | - | 8% done vs ~27% elapsed | Track daily; review again at mid-sprint (Oct 27) | PM |
| MEDIUM | Load | - | Priya Shah holds 13 open pts, all of it blocked | Reassign PHX-122 or pair her with Marcus | PM |

## 4. Blockers
- **PHX-101** Payment gateway 3DS2 integration · Priya Shah · **18 days** · Waiting on Stripe sandbox credentials (escalated Oct 21, no ETA) · *Carried over (blocked since Oct 9)*
- **PHX-110** EU VAT tax calculation · Ana Gomez · **9 days** · Needs Legal sign-off on VAT rounding rules · *Carried over (blocked since Oct 16)*
- **PHX-122** Fraud scoring webhook · Priya Shah · **2 days** · Depends on PHX-101 · ***New this week***

## 5. Stuck for more than one sprint
| Issue | Owner | Sprints | Timeline (weekly snapshots) | Diagnosis |
|---|---|---|---|---|
| **PHX-101** 3DS2 integration (8 pts) | Priya Shah | 3 (S40 → S42) | Oct 2 In Progress → Oct 9 Blocked → Oct 16 Blocked → Oct 23 Blocked | Vendor dependency with no ETA; needs exec escalation or a descope decision |
| **PHX-107** Cart multi-currency refactor (8 pts) | Dev Patel | 3 (S40 → S42) | Oct 2 In Progress → Oct 9 In Progress → Oct 16 In Review → Oct 23 In Review | Stalled in code review; reviewer capacity, not engineering effort |
| **PHX-110** EU VAT calculation (5 pts) | Ana Gomez | 2 (S41 → S42) | Oct 9 To Do → Oct 16 Blocked → Oct 23 Blocked | Waiting on a policy decision from Legal |
| **PHX-115** Load test checkout API (3 pts) | Tom Okafor | 2 (S41 → S42) | Oct 9 To Do → Oct 16 To Do → Oct 23 To Do | Never started; keeps losing out to feature work |

## 6. Completed this week
- **PHX-120** Apple Pay button (3 pts) - Priya Shah
- **PHX-135** Release checklist & runbook (1 pt) - Marcus Lee

## 7. Week-over-week trends
- **Blockers rising:** 0 → 1 → 2 → 3 over the last four snapshots. One was added this week and none were resolved.
- **Carry-over growing:** 0 → 2 → 2 → 4 open items spanning more than one sprint. Two items (PHX-101, PHX-107) are now in their 3rd sprint.
- **Commitment keeps outpacing delivery:** Sprint 40 delivered 21 of 37 pts and Sprint 41 delivered 25 of 52. Sprint 42 committed 49 against a 23-pt average.

## 8. Asks & decisions needed
1. **Eng Director:** escalate the Stripe 3DS2 sandbox access (PHX-101) by Tue Oct 27.
2. **Legal:** decide the VAT rounding rule for PHX-110 by Tue Oct 27.
3. **Platform lead:** assign a reviewer to PR #482 (PHX-107) within 24h.
4. **Product:** approve moving ~20 pts out of Sprint 42 and decide whether 3DS2 stays in the Oct 31 release.

---
*Generated by PM Sprint Status Agent from 4 weekly Jira snapshots in memory (Oct 2 – Oct 23). Sample data: "Phoenix - Checkout Revamp" is a demo project.*
