"""Generates jira_mock.md: 6 weekly snapshots of a synthetic Jira project."""

SNAPS = [
    ("2026-09-18", "Sprint 40", "mid-sprint"),
    ("2026-09-25", "Sprint 40", "sprint close"),
    ("2026-10-02", "Sprint 41", "mid-sprint"),
    ("2026-10-09", "Sprint 41", "sprint close"),
    ("2026-10-16", "Sprint 42", "mid-sprint"),
    ("2026-10-23", "Sprint 42", "sprint close"),
]

SPRINTS = [
    ("Sprint 40", "2026-09-14", "2026-09-25", "Core signup flow: social sign-in, account API, welcome screens", 34),
    ("Sprint 41", "2026-09-28", "2026-10-09", "Verification & profile setup: KYC, profile screens, push opt-in", 50),
    ("Sprint 42", "2026-10-12", "2026-10-23", "Release hardening: magic link, consent, localisation, E2E tests", 42),
    ("Sprint 43", "2026-10-26", "2026-11-06", "Release sprint (planning Mon Oct 26) - Onboarding v2 GA on Nov 6", None),
]

TEAM = [
    ("Maya Chen", "Product Manager", "-"),
    ("Lena Fischer", "Backend engineer (tech lead)", "100%"),
    ("Omar Haddad", "Backend engineer", "100%"),
    ("Priya Nair", "iOS engineer", "100%"),
    ("Jordan Kim", "Android engineer", "100%"),
    ("Sofia Reyes", "Product designer", "100%"),
    ("Ben Carter", "QA engineer", "50% from Oct 5 (lent to Payments regression)"),
]

# per-snapshot state: (status, status_since, note) or None if not on the board in that snapshot
I = []

def issue(key, summary, typ, prio, pts, who, created, due, states):
    I.append(dict(key=key, summary=summary, type=typ, prio=prio, pts=pts, who=who,
                  created=created, due=due, states=states))

N = None
# ---------------- Sprint 40 ----------------
issue("ATL-101", "Google & Apple sign-in", "Story", "High", 8, "Lena Fischer", "2026-09-08", "2026-09-25", [
    ("In Progress", "2026-09-15", ""),
    ("In Progress", "2026-09-15", "Google done; Apple flow in progress. Carried to Sprint 41"),
    ("Blocked", "2026-09-29", "Waiting on Apple 'Sign in with Apple' entitlement for prod bundle ID (Apple review)"),
    ("Done", "2026-10-07", "Entitlement approved Oct 6; shipped to staging Oct 7"),
    N, N])
issue("ATL-102", "Onboarding screens design v2", "Story", "High", 5, "Sofia Reyes", "2026-09-08", "2026-09-22", [
    ("In Progress", "2026-09-14", ""),
    ("Done", "2026-09-22", "Signed off by Maya"),
    N, N, N, N])
issue("ATL-103", "Welcome carousel - iOS", "Story", "Medium", 3, "Priya Nair", "2026-09-08", "2026-09-25", [
    ("In Progress", "2026-09-16", ""),
    ("Done", "2026-09-23", ""),
    N, N, N, N])
issue("ATL-104", "Welcome carousel - Android", "Story", "Medium", 3, "Jordan Kim", "2026-09-08", "2026-09-25", [
    ("To Do", "2026-09-14", ""),
    ("Done", "2026-09-24", ""),
    N, N, N, N])
issue("ATL-105", "Account creation API v2", "Story", "High", 5, "Omar Haddad", "2026-09-08", "2026-09-23", [
    ("In Progress", "2026-09-14", ""),
    ("Done", "2026-09-22", ""),
    N, N, N, N])
issue("ATL-106", "Email verification service", "Story", "High", 5, "Omar Haddad", "2026-09-08", "2026-09-25", [
    ("To Do", "2026-09-14", ""),
    ("In Review", "2026-09-24", "PR #188 open. Carried to Sprint 41"),
    ("Done", "2026-09-30", ""),
    ("Done", "2026-09-30", ""),
    N, N])
issue("ATL-107", "Analytics events for onboarding funnel", "Task", "Medium", 3, "Jordan Kim", "2026-09-09", "2026-10-02", [
    ("To Do", "2026-09-14", ""),
    ("To Do", "2026-09-14", "Not started. Carried to Sprint 41"),
    ("In Progress", "2026-09-30", ""),
    ("Done", "2026-10-08", ""),
    N, N])
issue("ATL-109", "Crash on Android 12 when rotating during signup", "Bug", "High", 2, "Jordan Kim", "2026-09-11", "2026-09-18", [
    ("Done", "2026-09-17", "Hotfix released 1.14.2"),
    ("Done", "2026-09-17", ""),
    N, N, N, N])

# ---------------- Sprint 41 ----------------
issue("ATL-108", "KYC identity verification - VeriID integration", "Story", "Highest", 8, "Lena Fischer", "2026-09-21", "2026-10-16", [
    N, N,
    ("Blocked", "2026-09-30", "VeriID vendor contract pending Procurement; no sandbox API keys"),
    ("Blocked", "2026-09-30", "Procurement: contract with Legal for DPA review. Carried to Sprint 42"),
    ("Blocked", "2026-09-30", "Still no sandbox keys. Lena building against mocked VeriID responses"),
    ("Blocked", "2026-09-30", "Legal DPA review ongoing, no ETA. Release Nov 6 cannot pass KYC without it"),
])
issue("ATL-110", "Profile setup screen - iOS", "Story", "Medium", 5, "Priya Nair", "2026-09-22", "2026-10-09", [
    N, N,
    ("In Progress", "2026-09-29", ""),
    ("Done", "2026-10-08", ""),
    N, N])
issue("ATL-111", "Profile setup screen - Android", "Story", "Medium", 5, "Jordan Kim", "2026-09-22", "2026-10-09", [
    N, N,
    ("To Do", "2026-09-28", ""),
    ("In Progress", "2026-10-05", "Carried to Sprint 42"),
    ("Done", "2026-10-15", ""),
    ("Done", "2026-10-15", ""),
])
issue("ATL-112", "Push notification opt-in flow", "Story", "High", 5, "Priya Nair", "2026-09-22", "2026-10-16", [
    N, N,
    ("To Do", "2026-09-28", ""),
    ("In Review", "2026-10-08", "PR #219 awaiting review from Mobile Platform team. Carried to Sprint 42"),
    ("In Review", "2026-10-08", "PR #219 still unreviewed; pinged platform lead Oct 14"),
    ("In Review", "2026-10-08", "PR #219: 1 of 2 required approvals; second reviewer on leave until Oct 28"),
])
issue("ATL-113", "Rate limiting on signup endpoint", "Story", "High", 3, "Omar Haddad", "2026-09-22", "2026-10-09", [
    N, N,
    ("In Progress", "2026-09-29", ""),
    ("Done", "2026-10-06", ""),
    N, N])
issue("ATL-114", "Accessibility audit of onboarding screens", "Task", "Medium", 3, "Sofia Reyes", "2026-09-22", "2026-10-09", [
    N, N,
    ("In Progress", "2026-09-30", ""),
    ("Done", "2026-10-07", "4 contrast issues filed into design v2.1"),
    N, N])
issue("ATL-115", "E2E test suite for onboarding (Detox + Espresso)", "Task", "High", 5, "Ben Carter", "2026-09-22", "2026-10-30", [
    N, N,
    ("To Do", "2026-09-28", ""),
    ("To Do", "2026-09-28", "Ben at 50% on Payments regression. Carried to Sprint 42"),
    ("To Do", "2026-09-28", ""),
    ("To Do", "2026-09-28", "Not started. Release gate for Nov 6"),
])

# ---------------- Sprint 42 ----------------
issue("ATL-116", "Passwordless magic-link login", "Story", "High", 8, "Omar Haddad", "2026-10-05", "2026-10-23", [
    N, N, N, N,
    ("In Progress", "2026-10-13", ""),
    ("In Progress", "2026-10-13", "~60% done; slowed by ATL-120 bug fix. Will carry to Sprint 43"),
])
issue("ATL-117", "Save onboarding progress (resume later)", "Story", "Medium", 5, "Lena Fischer", "2026-10-05", "2026-10-23", [
    N, N, N, N,
    ("In Progress", "2026-10-14", ""),
    ("In Review", "2026-10-22", "PR #231 open"),
])
issue("ATL-118", "Localisation: ES / FR / DE strings", "Task", "Medium", 3, "Sofia Reyes", "2026-10-05", "2026-10-21", [
    N, N, N, N,
    ("Blocked", "2026-10-13", "Waiting on translation vendor (LinguaPro) delivery"),
    ("Done", "2026-10-21", "Strings delivered Oct 20, merged Oct 21"),
])
issue("ATL-119", "Terms & privacy consent screen", "Story", "High", 3, "Priya Nair", "2026-10-05", "2026-10-23", [
    N, N, N, N,
    ("Blocked", "2026-10-13", "Awaiting Legal approval of GDPR consent copy"),
    ("Blocked", "2026-10-13", "Legal reviewing copy together with VeriID DPA; no date given"),
])
issue("ATL-120", "Email verification link expires after 5 min instead of 24 h", "Bug", "Highest", 2, "Omar Haddad", "2026-10-14", "2026-10-17", [
    N, N, N, N,
    ("In Progress", "2026-10-14", "Added mid-sprint (prod incident INC-342)"),
    ("Done", "2026-10-17", "Hotfix 1.15.1"),
])
issue("ATL-122", "Feature-flag rollout config for onboarding v2", "Task", "High", 2, "Omar Haddad", "2026-10-15", "2026-10-30", [
    N, N, N, N,
    ("To Do", "2026-10-15", "Added mid-sprint"),
    ("To Do", "2026-10-15", "Not started. Needed before the Nov 6 staged rollout"),
])
issue("ATL-121", "Apple sign-in fails for 'Hide My Email' relay users", "Bug", "Highest", 3, "Lena Fischer", "2026-10-19", "2026-10-27", [
    N, N, N, N, N,
    ("In Progress", "2026-10-20", "Added mid-sprint; ~4% of iOS signups affected on staging"),
])
issue("ATL-123", "Profile photo upload hangs on slow networks", "Bug", "Medium", 2, "Jordan Kim", "2026-10-20", "2026-10-30", [
    N, N, N, N, N,
    ("To Do", "2026-10-20", "Added mid-sprint (found in beta)"),
])

SPRINT_OF = {i: s[1] for i, s in enumerate(SNAPS)}
SHORT = {"Sprint 40": "S40", "Sprint 41": "S41", "Sprint 42": "S42"}


def sprint_history(it, upto):
    seen = []
    for j in range(upto + 1):
        if it["states"][j] is not None:
            s = SHORT[SPRINT_OF[j]]
            if s not in seen:
                seen.append(s)
    return seen


def esc(t):
    return t.replace("|", "\\|")


out = []
w = out.append
w("# Jira Mock Data - ATLAS (Mobile Onboarding v2)\n")
w("> **Synthetic data** for testing the PM Sprint Status Agent. All people, issues, vendors and PR numbers are fictional.\n")
w("## Project\n")
w("| Field | Value |\n|---|---|")
w("| Project key | ATL |")
w("| Project | Atlas - Mobile Onboarding v2 |")
w("| Board | ATL Scrum board (2-week sprints, Mon-Fri) |")
w("| Release | Onboarding v2 GA - **2026-11-06** (staged rollout behind a feature flag) |")
w("| Snapshot cadence | Weekly, Fridays 17:00 ET (mid-sprint and sprint close) |")
w("| Statuses | To Do -> In Progress -> In Review -> Done; Blocked can occur at any point |")
w("")
w("## Team\n")
w("| Name | Role | Allocation |\n|---|---|---|")
for n, r, a in TEAM:
    w(f"| {n} | {r} | {a} |")
w("")
w("## Sprints\n")
w("| Sprint | Start | End | Goal | Committed at planning (pts) |\n|---|---|---|---|---|")
for s, a, b, g, c in SPRINTS:
    w(f"| {s} | {a} | {b} | {g} | {c if c is not None else 'not planned yet'} |")
w("")
w("## Field reference\n")
w("- **Status since**: date the issue entered its current status (use it for days-in-status / days-blocked).")
w("- **Sprints**: every sprint the issue has been in; more than one means it was carried over.")
w("- **Added**: `planned` = in the sprint at planning; `mid-sprint` = added after the sprint started (scope change).")
w("- **Pts**: story points. Done points count toward velocity in the sprint where the issue reached Done.")
w("- Each snapshot shows the **active sprint board** at that moment. Issues finished in an earlier sprint do not reappear.\n")

for idx, (date, sprint, kind) in enumerate(SNAPS):
    rows = [it for it in I if it["states"][idx] is not None]
    start = [s for s in SPRINTS if s[0] == sprint][0][1]
    w("---\n")
    w(f"## Snapshot {idx + 1} - {date} ({sprint}, {kind})\n")
    w("| Key | Summary | Type | Priority | Status | Status since | Assignee | Pts | Sprints | Added | Created | Due | Notes |")
    w("|---|---|---|---|---|---|---|---|---|---|---|---|---|")
    for it in rows:
        st, since, note = it["states"][idx]
        added = "mid-sprint" if it["created"] > start else "planned"
        sh = ", ".join(sprint_history(it, idx))
        w(f"| {it['key']} | {esc(it['summary'])} | {it['type']} | {it['prio']} | {st} | {since} | {it['who']} | "
          f"{it['pts']} | {sh} | {added} | {it['created']} | {it['due']} | {esc(note) or '-'} |")
    w("")

open("jira_mock.md", "w").write("\n".join(out))

# quick metrics for verification
for idx, (date, sprint, kind) in enumerate(SNAPS):
    rows = [it for it in I if it["states"][idx] is not None]
    tot = sum(r["pts"] for r in rows)
    done = sum(r["pts"] for r in rows if r["states"][idx][0] == "Done")
    blk = [r["key"] for r in rows if r["states"][idx][0] == "Blocked"]
    carry = [r["key"] for r in rows if len(sprint_history(r, idx)) > 1 and r["states"][idx][0] != "Done"]
    print(date, sprint, f"scope={tot} done={done} n={len(rows)} blocked={blk} carry_open={carry}")
