# Integrations Reference

<!-- TODO: Fill in your Jira project key and GitHub repo below -->

## Jira integration

MCP tools from the Atlassian server are available for Jira operations. The project key is **YOUR_KEY** and the Jira site is accessed via a `cloudId` (use the site URL).

- **Read a ticket**: `mcp__atlassian__getJiraIssue`: fetch issue details by key.
- **Search tickets**: `mcp__atlassian__searchJiraIssuesUsingJql`: query with JQL (e.g. `project = YOUR_KEY AND status = "In Progress"`). Use `mcp__atlassian__search` for free-text Rovo search.
- **Create a ticket**: `mcp__atlassian__createJiraIssue`: requires `projectKey`, `issueTypeName` (Task, Bug, Story), and `summary`.
- **Update a ticket**: `mcp__atlassian__editJiraIssue`: update fields like summary, description, assignee.
- **Transition status**: `mcp__atlassian__transitionJiraIssue`: move a ticket through workflow states. Call `mcp__atlassian__getTransitionsForJiraIssue` first to get valid transition IDs.
- **Add a comment**: `mcp__atlassian__addCommentToJiraIssue`: post a comment (Markdown supported).

All Atlassian MCP tools require `cloudId`. Use `mcp__atlassian__getAccessibleAtlassianResources` to discover it if needed.

## GitHub integration

MCP tools from the GitHub server and the `gh` CLI are both available.

- **Branches**: `mcp__github__create_branch` to create, `mcp__github__list_branches` to list. Branch names should include the Jira ticket key (e.g. `PROJ-12-add-feature`).
- **Pull requests**:
  - Create: `mcp__github__create_pull_request`, set `base: "main"`, `head` to feature branch. Include the Jira ticket key in the PR title or body.
  - Read: `mcp__github__pull_request_read`, use `method: "get"` for details, `"get_diff"` for diff, `"get_review_comments"` for review threads, `"get_files"` for changed files.
  - Update: `mcp__github__update_pull_request`, change title, body, state, or request reviewers.
  - Merge: `mcp__github__merge_pull_request`, prefer `merge_method: "squash"` for clean history.
  - Reply to review comments: `mcp__github__add_reply_to_pull_request_comment`.
- **Issues**: `mcp__github__list_issues`, `mcp__github__search_issues`, `mcp__github__issue_read`, `mcp__github__issue_write`.
- **Commits**: `mcp__github__list_commits` to view commit history.
- **CLI alternative**: The `gh` CLI is also available via Bash for operations like `gh pr view`, `gh pr create`, `gh issue list`, etc.

## Workflow: Jira + GitHub together

1. Pick up or create a Jira ticket.
2. Transition the ticket to **In Progress**.
3. Create a branch named `PROJ-12-short-description` from `main`.
4. Make changes, commit with messages referencing the ticket key.
5. Push and open a PR targeting `main`. Include the ticket key in the PR title.
6. After merge, transition the Jira ticket to **Done**.
