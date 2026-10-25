# Jira Mock Data - ATLAS (Mobile Onboarding v2)

> **Synthetic data** for testing the PM Sprint Status Agent. All people, issues, vendors and PR numbers are fictional.

## Project

| Field | Value |
|---|---|
| Project key | ATL |
| Project | Atlas - Mobile Onboarding v2 |
| Board | ATL Scrum board (2-week sprints, Mon-Fri) |
| Release | Onboarding v2 GA - **2026-11-06** (staged rollout behind a feature flag) |
| Snapshot cadence | Weekly, Fridays 17:00 ET (mid-sprint and sprint close) |
| Statuses | To Do -> In Progress -> In Review -> Done; Blocked can occur at any point |

## Team

| Name | Role | Allocation |
|---|---|---|
| Maya Chen | Product Manager | - |
| Lena Fischer | Backend engineer (tech lead) | 100% |
| Omar Haddad | Backend engineer | 100% |
| Priya Nair | iOS engineer | 100% |
| Jordan Kim | Android engineer | 100% |
| Sofia Reyes | Product designer | 100% |
| Ben Carter | QA engineer | 50% from Oct 5 (lent to Payments regression) |

## Sprints

| Sprint | Start | End | Goal | Committed at planning (pts) |
|---|---|---|---|---|
| Sprint 40 | 2026-09-14 | 2026-09-25 | Core signup flow: social sign-in, account API, welcome screens | 34 |
| Sprint 41 | 2026-09-28 | 2026-10-09 | Verification & profile setup: KYC, profile screens, push opt-in | 50 |
| Sprint 42 | 2026-10-12 | 2026-10-23 | Release hardening: magic link, consent, localisation, E2E tests | 42 |
| Sprint 43 | 2026-10-26 | 2026-11-06 | Release sprint (planning Mon Oct 26) - Onboarding v2 GA on Nov 6 | not planned yet |

## Field reference

- **Status since**: date the issue entered its current status (use it for days-in-status / days-blocked).
- **Sprints**: every sprint the issue has been in; more than one means it was carried over.
- **Added**: `planned` = in the sprint at planning; `mid-sprint` = added after the sprint started (scope change).
- **Pts**: story points. Done points count toward velocity in the sprint where the issue reached Done.
- Each snapshot shows the **active sprint board** at that moment. Issues finished in an earlier sprint do not reappear.

---

## Snapshot 1 - 2026-09-18 (Sprint 40, mid-sprint)

| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATL-101 | Google & Apple sign-in | Story | High | In Progress | 2026-09-15 | Lena Fischer | 8 | S40 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-102 | Onboarding screens design v2 | Story | High | In Progress | 2026-09-14 | Sofia Reyes | 5 | S40 | planned | 2026-09-08 | 2026-09-22 | - |
| ATL-103 | Welcome carousel - iOS | Story | Medium | In Progress | 2026-09-16 | Priya Nair | 3 | S40 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-104 | Welcome carousel - Android | Story | Medium | To Do | 2026-09-14 | Jordan Kim | 3 | S40 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-105 | Account creation API v2 | Story | High | In Progress | 2026-09-14 | Omar Haddad | 5 | S40 | planned | 2026-09-08 | 2026-09-23 | - |
| ATL-106 | Email verification service | Story | High | To Do | 2026-09-14 | Omar Haddad | 5 | S40 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-107 | Analytics events for onboarding funnel | Task | Medium | To Do | 2026-09-14 | Jordan Kim | 3 | S40 | planned | 2026-09-09 | 2026-10-02 | - |
| ATL-109 | Crash on Android 12 when rotating during signup | Bug | High | Done | 2026-09-17 | Jordan Kim | 2 | S40 | planned | 2026-09-11 | 2026-09-18 | Hotfix released 1.14.2 |

---

## Snapshot 2 - 2026-09-25 (Sprint 40, sprint close)

| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATL-101 | Google & Apple sign-in | Story | High | In Progress | 2026-09-15 | Lena Fischer | 8 | S40 | planned | 2026-09-08 | 2026-09-25 | Google done; Apple flow in progress. Carried to Sprint 41 |
| ATL-102 | Onboarding screens design v2 | Story | High | Done | 2026-09-22 | Sofia Reyes | 5 | S40 | planned | 2026-09-08 | 2026-09-22 | Signed off by Maya |
| ATL-103 | Welcome carousel - iOS | Story | Medium | Done | 2026-09-23 | Priya Nair | 3 | S40 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-104 | Welcome carousel - Android | Story | Medium | Done | 2026-09-24 | Jordan Kim | 3 | S40 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-105 | Account creation API v2 | Story | High | Done | 2026-09-22 | Omar Haddad | 5 | S40 | planned | 2026-09-08 | 2026-09-23 | - |
| ATL-106 | Email verification service | Story | High | In Review | 2026-09-24 | Omar Haddad | 5 | S40 | planned | 2026-09-08 | 2026-09-25 | PR #188 open. Carried to Sprint 41 |
| ATL-107 | Analytics events for onboarding funnel | Task | Medium | To Do | 2026-09-14 | Jordan Kim | 3 | S40 | planned | 2026-09-09 | 2026-10-02 | Not started. Carried to Sprint 41 |
| ATL-109 | Crash on Android 12 when rotating during signup | Bug | High | Done | 2026-09-17 | Jordan Kim | 2 | S40 | planned | 2026-09-11 | 2026-09-18 | - |

---

## Snapshot 3 - 2026-10-02 (Sprint 41, mid-sprint)

| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATL-101 | Google & Apple sign-in | Story | High | Blocked | 2026-09-29 | Lena Fischer | 8 | S40, S41 | planned | 2026-09-08 | 2026-09-25 | Waiting on Apple 'Sign in with Apple' entitlement for prod bundle ID (Apple review) |
| ATL-106 | Email verification service | Story | High | Done | 2026-09-30 | Omar Haddad | 5 | S40, S41 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-107 | Analytics events for onboarding funnel | Task | Medium | In Progress | 2026-09-30 | Jordan Kim | 3 | S40, S41 | planned | 2026-09-09 | 2026-10-02 | - |
| ATL-108 | KYC identity verification - VeriID integration | Story | Highest | Blocked | 2026-09-30 | Lena Fischer | 8 | S41 | planned | 2026-09-21 | 2026-10-16 | VeriID vendor contract pending Procurement; no sandbox API keys |
| ATL-110 | Profile setup screen - iOS | Story | Medium | In Progress | 2026-09-29 | Priya Nair | 5 | S41 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-111 | Profile setup screen - Android | Story | Medium | To Do | 2026-09-28 | Jordan Kim | 5 | S41 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-112 | Push notification opt-in flow | Story | High | To Do | 2026-09-28 | Priya Nair | 5 | S41 | planned | 2026-09-22 | 2026-10-16 | - |
| ATL-113 | Rate limiting on signup endpoint | Story | High | In Progress | 2026-09-29 | Omar Haddad | 3 | S41 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-114 | Accessibility audit of onboarding screens | Task | Medium | In Progress | 2026-09-30 | Sofia Reyes | 3 | S41 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-115 | E2E test suite for onboarding (Detox + Espresso) | Task | High | To Do | 2026-09-28 | Ben Carter | 5 | S41 | planned | 2026-09-22 | 2026-10-30 | - |

---

## Snapshot 4 - 2026-10-09 (Sprint 41, sprint close)

| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATL-101 | Google & Apple sign-in | Story | High | Done | 2026-10-07 | Lena Fischer | 8 | S40, S41 | planned | 2026-09-08 | 2026-09-25 | Entitlement approved Oct 6; shipped to staging Oct 7 |
| ATL-106 | Email verification service | Story | High | Done | 2026-09-30 | Omar Haddad | 5 | S40, S41 | planned | 2026-09-08 | 2026-09-25 | - |
| ATL-107 | Analytics events for onboarding funnel | Task | Medium | Done | 2026-10-08 | Jordan Kim | 3 | S40, S41 | planned | 2026-09-09 | 2026-10-02 | - |
| ATL-108 | KYC identity verification - VeriID integration | Story | Highest | Blocked | 2026-09-30 | Lena Fischer | 8 | S41 | planned | 2026-09-21 | 2026-10-16 | Procurement: contract with Legal for DPA review. Carried to Sprint 42 |
| ATL-110 | Profile setup screen - iOS | Story | Medium | Done | 2026-10-08 | Priya Nair | 5 | S41 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-111 | Profile setup screen - Android | Story | Medium | In Progress | 2026-10-05 | Jordan Kim | 5 | S41 | planned | 2026-09-22 | 2026-10-09 | Carried to Sprint 42 |
| ATL-112 | Push notification opt-in flow | Story | High | In Review | 2026-10-08 | Priya Nair | 5 | S41 | planned | 2026-09-22 | 2026-10-16 | PR #219 awaiting review from Mobile Platform team. Carried to Sprint 42 |
| ATL-113 | Rate limiting on signup endpoint | Story | High | Done | 2026-10-06 | Omar Haddad | 3 | S41 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-114 | Accessibility audit of onboarding screens | Task | Medium | Done | 2026-10-07 | Sofia Reyes | 3 | S41 | planned | 2026-09-22 | 2026-10-09 | 4 contrast issues filed into design v2.1 |
| ATL-115 | E2E test suite for onboarding (Detox + Espresso) | Task | High | To Do | 2026-09-28 | Ben Carter | 5 | S41 | planned | 2026-09-22 | 2026-10-30 | Ben at 50% on Payments regression. Carried to Sprint 42 |

---

## Snapshot 5 - 2026-10-16 (Sprint 42, mid-sprint)

| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATL-108 | KYC identity verification - VeriID integration | Story | Highest | Blocked | 2026-09-30 | Lena Fischer | 8 | S41, S42 | planned | 2026-09-21 | 2026-10-16 | Still no sandbox keys. Lena building against mocked VeriID responses |
| ATL-111 | Profile setup screen - Android | Story | Medium | Done | 2026-10-15 | Jordan Kim | 5 | S41, S42 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-112 | Push notification opt-in flow | Story | High | In Review | 2026-10-08 | Priya Nair | 5 | S41, S42 | planned | 2026-09-22 | 2026-10-16 | PR #219 still unreviewed; pinged platform lead Oct 14 |
| ATL-115 | E2E test suite for onboarding (Detox + Espresso) | Task | High | To Do | 2026-09-28 | Ben Carter | 5 | S41, S42 | planned | 2026-09-22 | 2026-10-30 | - |
| ATL-116 | Passwordless magic-link login | Story | High | In Progress | 2026-10-13 | Omar Haddad | 8 | S42 | planned | 2026-10-05 | 2026-10-23 | - |
| ATL-117 | Save onboarding progress (resume later) | Story | Medium | In Progress | 2026-10-14 | Lena Fischer | 5 | S42 | planned | 2026-10-05 | 2026-10-23 | - |
| ATL-118 | Localisation: ES / FR / DE strings | Task | Medium | Blocked | 2026-10-13 | Sofia Reyes | 3 | S42 | planned | 2026-10-05 | 2026-10-21 | Waiting on translation vendor (LinguaPro) delivery |
| ATL-119 | Terms & privacy consent screen | Story | High | Blocked | 2026-10-13 | Priya Nair | 3 | S42 | planned | 2026-10-05 | 2026-10-23 | Awaiting Legal approval of GDPR consent copy |
| ATL-120 | Email verification link expires after 5 min instead of 24 h | Bug | Highest | In Progress | 2026-10-14 | Omar Haddad | 2 | S42 | mid-sprint | 2026-10-14 | 2026-10-17 | Added mid-sprint (prod incident INC-342) |
| ATL-122 | Feature-flag rollout config for onboarding v2 | Task | High | To Do | 2026-10-15 | Omar Haddad | 2 | S42 | mid-sprint | 2026-10-15 | 2026-10-30 | Added mid-sprint |

---

## Snapshot 6 - 2026-10-23 (Sprint 42, sprint close)

| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| ATL-108 | KYC identity verification - VeriID integration | Story | Highest | Blocked | 2026-09-30 | Lena Fischer | 8 | S41, S42 | planned | 2026-09-21 | 2026-10-16 | Legal DPA review ongoing, no ETA. Release Nov 6 cannot pass KYC without it |
| ATL-111 | Profile setup screen - Android | Story | Medium | Done | 2026-10-15 | Jordan Kim | 5 | S41, S42 | planned | 2026-09-22 | 2026-10-09 | - |
| ATL-112 | Push notification opt-in flow | Story | High | In Review | 2026-10-08 | Priya Nair | 5 | S41, S42 | planned | 2026-09-22 | 2026-10-16 | PR #219: 1 of 2 required approvals; second reviewer on leave until Oct 28 |
| ATL-115 | E2E test suite for onboarding (Detox + Espresso) | Task | High | To Do | 2026-09-28 | Ben Carter | 5 | S41, S42 | planned | 2026-09-22 | 2026-10-30 | Not started. Release gate for Nov 6 |
| ATL-116 | Passwordless magic-link login | Story | High | In Progress | 2026-10-13 | Omar Haddad | 8 | S42 | planned | 2026-10-05 | 2026-10-23 | ~60% done; slowed by ATL-120 bug fix. Will carry to Sprint 43 |
| ATL-117 | Save onboarding progress (resume later) | Story | Medium | In Review | 2026-10-22 | Lena Fischer | 5 | S42 | planned | 2026-10-05 | 2026-10-23 | PR #231 open |
| ATL-118 | Localisation: ES / FR / DE strings | Task | Medium | Done | 2026-10-21 | Sofia Reyes | 3 | S42 | planned | 2026-10-05 | 2026-10-21 | Strings delivered Oct 20, merged Oct 21 |
| ATL-119 | Terms & privacy consent screen | Story | High | Blocked | 2026-10-13 | Priya Nair | 3 | S42 | planned | 2026-10-05 | 2026-10-23 | Legal reviewing copy together with VeriID DPA; no date given |
| ATL-120 | Email verification link expires after 5 min instead of 24 h | Bug | Highest | Done | 2026-10-17 | Omar Haddad | 2 | S42 | mid-sprint | 2026-10-14 | 2026-10-17 | Hotfix 1.15.1 |
| ATL-122 | Feature-flag rollout config for onboarding v2 | Task | High | To Do | 2026-10-15 | Omar Haddad | 2 | S42 | mid-sprint | 2026-10-15 | 2026-10-30 | Not started. Needed before the Nov 6 staged rollout |
| ATL-121 | Apple sign-in fails for 'Hide My Email' relay users | Bug | Highest | In Progress | 2026-10-20 | Lena Fischer | 3 | S42 | mid-sprint | 2026-10-19 | 2026-10-27 | Added mid-sprint; ~4% of iOS signups affected on staging |
| ATL-123 | Profile photo upload hangs on slow networks | Bug | Medium | To Do | 2026-10-20 | Jordan Kim | 2 | S42 | mid-sprint | 2026-10-20 | 2026-10-30 | Added mid-sprint (found in beta) |
