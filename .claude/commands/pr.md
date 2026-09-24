---
description: "Create a PR from the current branch targeting main"
disable-model-invocation: true
---

Create a pull request from the current branch:

1. **Get branch info**: Run `git branch --show-current` to get the current branch name. If it starts with a ticket key (for example `PROJ-12`), carry that key into the title.

2. **Gather changes**:
   - Run `git log main..HEAD --oneline` for commit history
   - Run `git diff main...HEAD --stat` for changed files summary

3. **Create the PR** with the `gh` CLI, which takes the owner and repo from the current checkout:

   ```
   gh pr create --base main --head "$(git branch --show-current)" \
     --title "<title>" --body "<body>"
   ```

   - `title`: Conventional Commit style, `{type}: {concise description of changes}` (under 70 chars), prefixed with the ticket key if step 1 found one
   - `body`: use this template and keep the whole body shorter than the diff it describes:
     - `## Summary`: at most 5 one-line bullets, what changed and why
     - `## Risk`: one line on what could break and how widely
     - `## Test plan`: a checklist of what was actually run

     Leave out anything a reviewer can read from the diff itself.

4. **Report**: Show the PR URL and a summary of what was included.
