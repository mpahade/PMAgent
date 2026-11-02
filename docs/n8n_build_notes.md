# PM Sprint Status Agent - build notes (n8n)

Plan & architecture doc: https://claude.ai/artifact/VNW47QG7XTDZWjQUFKBgqy

## n8n assets (folder "PM Status Agent", personal project)
- Workflow: PM Agent - Weekly Sprint Status Report - https://madhumita.app.n8n.cloud/workflow/mUAVbQQcu8w2To3c
  Triggers: Friday 3pm schedule, "Run Report Now", "Called by PM Agent". Config node: data_source (sample|jira), jql, team_name, story_points_field, sprint_field.
- Workflow: PM Agent - Sprint Memory Lookup (agent tool, input issue_key) - https://madhumita.app.n8n.cloud/workflow/DAdH0cegIOTX4KE6
- Agent (draft): PM Sprint Status Agent - https://madhumita.app.n8n.cloud/projects/gfY6gUNKDliwoA3f/agents/gWt2cnMJshpVMMu6
  Tools: sprint_memory_lookup, get_past_reports, generate_weekly_report (approval required). Model anthropic/claude-sonnet-5-5.
- Data table pm_issue_snapshots (id v4rsUiIzb8KD362F): 41 demo rows, weeks 2026-10-02..2026-10-23
- Data table pm_weekly_reports (id sxu2s57R9dK3r4aP): 1 report (2026-10-23)

## Status (2026-10-25)
- n8n Cloud trial expired: executions blocked. Pipeline logic verified offline on seeded data.
- Agent validation pending: needs an Anthropic API credential + both workflows published.

## Go-live
1. Upgrade n8n (or self-host). 2. Jira Cloud credential on the Jira node. 3. Config: data_source=jira, jql, team_name.
4. Clear demo rows, Run Report Now. 5. Anthropic credential on the agent. 6. Publish workflows, validate + publish agent.
