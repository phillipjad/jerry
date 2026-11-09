---
name: project-state
description: Conventions for writing a Jerry project's state (RESUME.md, WORKTRACKER.md rows, evidence/ and work/ files) and for committing and pushing a projects root kept in git with jerry projects save. Use when updating a focused project's RESUME.md or work history, recording finished work or evidence, closing a project, or when the user asks to commit, push, sync or save project state. Not for work item entities (use worktracker) or for commits to code repositories.
version: "1.0.0"
allowed-tools: Read, Write, Edit, Bash
activation-keywords:
  - "project state"
  - "save project state"
  - "commit project state"
  - "push project state"
  - "sync the project"
  - "update the resume"
  - "update RESUME.md"
  - "pick up here"
  - "record evidence"
  - "close the project"
  - "mark the project done"
  - "jerry projects save"
  - "/project-state"
  - "/jerry:project-state"
---

<!-- SPDX-License-Identifier: Apache-2.0 -->

# Project state

Two paths below come from Jerry, not from you:

- `{project_dir}`: the focused project's folder. Jerry's session-start context and
  `jerry focus show` print it as `{project_dir} = <path>`; use that path.
- `{root}`: the projects root that holds the project's folder. `jerry projects show <id>` prints it
  on its `root:` line.

A project's state lives in `{project_dir}`. In a root kept in git, teammates and your other sessions
read these files without this conversation. So:

- Refer to things by names that last: absolute dates, PR and issue numbers, branch names, file
  paths. Never "today", "the fix above", "my branch" or "as discussed".
- State each fact once, briefly. For detail, link to the file that holds it instead of repeating it.

## What goes where

- `RESUME.md` opens with `## Pick up here` (its first level-2 heading, at most 3,000 characters).
  It holds only what to do next and pointers to where the detail lives. Jerry injects it at session
  start, so every line there costs every session.
- Finished work goes in the work history, not in `RESUME.md`: rows in `WORKTRACKER.md`, raw data,
  logs and screenshots under `evidence/`, analysis and drafts under `work/`.
- When an item that a `RESUME.md` line or a hand-off row tracks completes, update that line or row.
  Do not add prose beside it.
- To close a project, set `status = "done"` or `"abandoned"` in its `project.toml`. The registry
  then moves it out of the main table into a collapsed table for that status.

## Scrub before committing

Never commit:

- credentials, tokens, keys or tenant secrets;
- personal email addresses;
- your home path: write `~/` instead;
- a session scratchpad path: write `<scratchpad>` instead.

`jerry projects save` refuses a file that holds your home path, a Claude Code scratchpad path or a
well-known token or private key shape, and names the file and line. It cannot recognise email
addresses or other secrets: check for those yourself.

## Save a root kept in git

1. Before editing, pull: `git -C "{root}" pull --rebase`.
2. Edit the project's files.
3. Commit:

   ```bash
   uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry projects save -m "Record the QA hand-off"
   ```

   It saves each focused project; pass IDs to save others. For each project it commits the whole
   top-level folder, so a parent's link to a new sub-project comes along, plus the root's
   `README.md` with the registry refreshed. Nothing else is committed, and changes you staged
   elsewhere stay staged. It stops before committing when `jerry projects check` reports an error
   or the scrub finds something.
4. Push only when the user allows it: run the same command with `--push` added. It pulls with
   rebase (stashing other uncommitted work and restoring it), then pushes the current branch.

### When `--push` reports "pull failed"

`save` has already aborted the rebase. Your commit is still in the local branch, and nothing was
pushed.

1. Run `git -C "{root}" pull --rebase`.
2. For each conflicted file, edit it to keep both sides' changes. For `README.md`, take either
   side, then run `uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry projects index --write`.
3. Run `git -C "{root}" add` on each resolved file.
4. Run `git -C "{root}" rebase --continue`.
5. Run the `save` command again with `--push`.

If step 1 fails without a conflict (no upstream branch, no network), report the error to the user.

Write commit subjects in the imperative mood, about 50 characters. Save at each milestone, not once
at the end: small commits conflict less. `save` commits to the current branch; the repository's
own rules on branches and reviews still apply. A root outside git has nothing to save.
