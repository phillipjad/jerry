# Jerry (derivative)

An independent derivative of [Jerry Framework](https://github.com/geekatron/jerry), a Claude Code
plugin for project-based work: work tracking, orchestration, problem-solving, systems engineering
and adversarial quality review. It is licensed under the Apache License 2.0, like upstream, and
is not affiliated with or endorsed by the upstream project.

## Quick Start Guide

Jerry organizes work into PROJ directories. Each one is a folder named `PROJ-NNN-slug` that holds
a `project.toml` with its title, status and links, and a `RESUME.md` whose `## Pick up here`
section says where the work stands. Keep them in a `projects/` folder next to the code they
describe; a sub-project nests inside its parent as `PROJ-NNN.N-slug`.

Ask for what you want in plain language, and Claude runs the matching command:

- "Start a project for the checkout redesign" runs `projects new checkout-redesign` and focuses it.
- "Work on PROJ-004" runs `focus set PROJ-004`.
- "Also pull in PROJ-002" runs `focus add PROJ-002`.
- "Add a sub-project to PROJ-004 for the payment form" runs
  `projects new payment-form --parent PROJ-004`.

If multi-step work starts without a named project, Claude asks you to pick one, create one or work
without one. The same commands also run from a terminal:

```sh
uv run --project /path/to/jerry jerry projects new checkout-redesign --title "Checkout redesign"
uv run --project /path/to/jerry jerry projects list
uv run --project /path/to/jerry jerry projects check
```

Because each project keeps its plan, links and next steps in the repository, every session starts
with the right context, agents put their output in the right place and stay on task, and people
can still reason about a large project many months after it ships.

## Why this derivative exists

Upstream Jerry ties each session to exactly one project, named by the `JERRY_PROJECT`
environment variable before Claude Code starts. That model does not fit work that spans several
related projects, or teams that keep their projects in a shared repository next to the code they
change. This derivative is built for that kind of work:

- **Several projects per session.** A session keeps a focus set of one or more projects, chosen
  during the session instead of at launch. Subagents inherit it.
- **Projects found where they live.** Jerry looks in the folder of projects you are standing in,
  then `./projects`, then `../projects`, then in roots listed in `~/.jerry/config.toml`, like
  other tooling that searches upward for its config.
- **Projects that relate to each other.** Sub-projects nest inside their parent with dotted IDs
  (`PROJ-004.1`), and projects declare typed links: `related`, `depends_on`, `supersedes`, `uses`.
- **Hooks whose context reaches the model.** Current Claude Code reads SessionStart context only
  from `hookSpecificOutput.additionalContext`; upstream's hooks print a top-level
  `additionalContext` field, so their context is dropped.
- **Windows as a first-class platform.** Upstream's hook commands leave `${CLAUDE_PLUGIN_ROOT}`
  unquoted, which breaks on backslash paths and paths with spaces.

These changes alter Jerry's core model rather than patch it, so they are made here as an
evolution of the upstream design. The skills that carry Jerry's methodology are kept and adapted.
The runtime around them is rewritten to be much smaller.

## Requirements

- [Claude Code](https://code.claude.com/docs).
- [`uv`](https://docs.astral.sh/uv/) on `PATH`. The hooks run as
  `uv run --no-project --python ">=3.11" ...`, so uv downloads Python 3.11 or later if it is
  missing. The first CLI call creates `.venv` in the plugin directory and installs two packages
  from PyPI.

## Install

The repository is a Claude Code plugin; it does not ship a marketplace. Add an entry for it to a
marketplace you control, with a `github` source pinned to a tag and its commit:

```json
{
  "name": "jerry",
  "source": {
    "source": "github",
    "repo": "phillipjad/jerry",
    "ref": "v1.0.0",
    "sha": "<40-character commit SHA of v1.0.0>"
  }
}
```

Then install it with `claude plugin install jerry@<your-marketplace>`.

To develop or try a clone without a marketplace, load it for one session:

```sh
claude --plugin-dir /path/to/jerry
```

## Projects

A project is a folder named `PROJ-NNN-slug` that holds a `project.toml`. A sub-project sits
directly inside its parent and extends the parent's number: `PROJ-NNN.N-slug`, nesting as deep as
needed. The slug uses lowercase letters, digits and single hyphens, starts with a letter, and is
at most 40 characters. A folder without `project.toml` is not a project.

```text
projects/
  README.md                      registry, generated between markers
  PROJ-001-namek-saga/
    project.toml
    RESUME.md
    PROJ-001.1-dragon-balls/
      project.toml
      RESUME.md
  PROJ-002-android-saga/
    project.toml
    RESUME.md
```

### project.toml

The ID comes from the folder name and is not repeated in the file.

```toml
title = "Namek Saga"
status = "active"               # active, paused, done or abandoned
summary = "Reach Namek and stop Frieza."
related = ["PROJ-002"]
depends_on = []
supersedes = []
uses = []
```

`title`, `status` and `summary` are required, and a key other than these and the four link
lists is an error. The link lists hold project IDs, and each link shows on its target as the
inverse: `depends_on` as `blocks`, `supersedes` as `superseded_by`, `uses` as `used_by`, and
`related` as `related`.

### RESUME.md

Every project has a `RESUME.md` whose first level-2 heading is `## Pick up here`: the next steps
and pointers, at most 3,000 characters. History goes below it. Jerry injects this section for
each focused project at session start. A parent's `RESUME.md` links to each child's `RESUME.md`;
`projects new --parent` adds the link.

### Registry

A root's `README.md` can hold a generated table of its projects between two marker lines:

```markdown
<!-- jerry:index:start -->
<!-- jerry:index:end -->
```

`projects index --write` rewrites the table and `projects new` refreshes it. `projects check`
and session start report a table that no longer matches the projects.

## Discovery

Jerry searches from the directory the session starts in (outside a session, the CLI's working
directory). Every root found contributes, nearest first:

1. The enclosing root: the nearest directory, from the start directory upward, that directly
   holds a project and is not a project itself, so starting inside a projects folder or a
   project works.
2. `./projects`
3. `../projects`
4. The `roots` listed in `~/.jerry/config.toml` (`%USERPROFILE%\.jerry\config.toml` on Windows).

Only direct children of a root and of project folders are scanned. An ID found in two roots
resolves to the nearer one, with a warning; the same ID twice in one root is an error. A session
keeps the roots it found at start, so a `cd` during the session does not change what Jerry sees.

```toml
roots = [
  "~/work/projects",
  'C:\path\to\projects',
]
```

Roots must be absolute or start with `~`; a missing root is skipped with a warning. Write Windows
paths in single quotes: TOML treats a backslash in double quotes as an escape, so
`"C:\path\to\projects"` fails to parse, while a single-quoted literal string keeps every
backslash. Forward slashes (`"C:/path/to/projects"`) also work.

## Session focus

Each Claude Code session has a focus: one or more projects, or none. The first focused project
is the primary one, `{project_dir}`, where skills and agents write their output. The focus is
stored in `~/.jerry/sessions/<session id>.json`.

At session start Jerry injects, within about 9,000 characters:

- the plugin root and the CLI command for this session;
- the rule to invoke a matching Jerry skill proactively (H-22);
- the focus, and each focused project's `## Pick up here` section;
- warnings, such as shadowed IDs, a stale registry or config errors;
- an index of the discovered projects, shortened to fit.

When nothing is focused and tracked work starts (multi-step work, or changes to files or external
systems) without a named project, Claude asks you to pick a project, create one, or work without
one. Quick questions skip the ask. A session that cannot ask works without a project.

Claude runs the `focus` commands when you pick a project or ask for a change. `focus set <id>...`
replaces the focus (the first ID is primary), `focus add <id>...` adds to it, `focus none` works
without a project, and `focus show` prints the focus with each Pick up here section.

Subagents inherit the focus: each one is told `{project_dir}` and the other focused projects,
and never changes the focus itself. Resuming a session or compacting it keeps the focus. `/clear`
and a fork start a new session with nothing focused; Jerry then names the last focus used from
the same directory, if there was one, and the command that restores it.

## CLI reference

Claude runs the CLI as `uv run --project "<plugin root>" jerry ...`; the session-start context
gives it the exact command with `--session <id>`. From a terminal, use the path of your clone.

| Command | Does |
|---|---|
| `projects list` | List discovered projects by root |
| `projects show <id>` | Show one project with its links, inverse links, children and files |
| `projects new <slug> [--parent <id>] [--title <text>]` | Create the next-numbered project with `project.toml` and a `RESUME.md` stub; in a session, add it to the focus |
| `projects index [--write]` | Print each root's registry table, or rewrite it in `README.md` |
| `projects check` | Validate every project; exit 1 on any error |
| `focus show` / `set <id>...` / `add <id>...` / `none` | Show or change the session focus |
| `ast parse <file>` | Print a markdown file's tokens and AST as JSON |
| `ast frontmatter <file>` | Print a file's blockquote frontmatter as JSON |
| `ast validate <file> [--schema <type>] [--nav]` | Validate the navigation table and, with `--schema`, an entity type (epic, feature, story, enabler, task or bug) |
| `ast modify <file> --key <key> --value <value>` | Set one frontmatter field and write the file |

Every `projects` and `focus` command also takes:

- `--root <dir>`: use only this root instead of discovery; repeatable.
- `--session <id>`: the session whose stored roots and focus apply. Defaults to
  `$CLAUDE_CODE_SESSION_ID`. The `focus` commands need one.

`projects check` reports invalid folder names and nesting, invalid `project.toml` files, unknown
or self links, duplicate IDs in one root, a stale registry, a missing or oversized
`## Pick up here`, a parent `RESUME.md` that does not link a child's, and paths longer than 180
characters relative to their root, which keeps clones within Windows path limits.

## Permissions

By default Claude Code asks before each CLI call. To allow them, add a rule to
`permissions.allow` in `~/.claude/settings.json` or a project's `.claude/settings.json`:

```json
{
  "permissions": {
    "allow": ["Bash(uv run --project * jerry *)"]
  }
}
```

The plugin's path changes with every installed version, so a rule naming it would stop matching
after an update; this one uses `*` instead. That makes it broad: `*` matches any text, so the rule also allows any other command that
starts with `uv run --project` and contains ` jerry `. For a narrower setup, leave the rule out
and approve each call when Claude Code asks.

## Skills

Skills trigger from plain requests: each skill's description lists the requests it handles, and
the session-start context tells Claude to invoke a matching skill without being asked (H-22). You
can also run one directly as `/jerry:<name>`.

| Skill | For |
|---|---|
| `adversary` | Adversarial review of a finished deliverable, scored against a quality gate |
| `architecture` | Hexagonal, DDD and CQRS design: layer checks, design reviews, diagrams and ADRs |
| `ast` | Parsing, validating and editing Jerry markdown and work-item frontmatter through `jerry ast` |
| `nasa-se` | Systems engineering per NASA NPR 7123.1D: requirements, V&V, risk, reviews, trade studies |
| `orchestration` | Multi-agent workflows with parallel pipelines, gates and checkpoints that resume across sessions |
| `problem-solving` | Research, analysis, root-cause investigation and reviews by specialist agents that write reports |
| `worktracker` | Work items in `WORKTRACKER.md`: epics, features, stories, tasks and bugs, with verify and audit agents |
| `/architect` | Command: write a `PLAN.md` into `{project_dir}` before implementation starts |

## What changed from upstream

| Area | Upstream v0.31.9 | This derivative |
|---|---|---|
| Projects in scope | One, from `JERRY_PROJECT` | A per-session focus set of one or more projects |
| Project discovery | `projects/` under the Claude Code project directory | Enclosing root, `./projects`, `../projects`, then configured roots |
| Project structure | Flat `PROJ-NNN-slug` folders | Nested sub-projects, `project.toml` metadata, typed links, a generated registry |
| Hooks | SessionStart, UserPromptSubmit, PreToolUse, PreCompact, Stop, SubagentStop | SessionStart and SubagentStart only, standard library only, no shell |
| Context monitoring | Context-fill tiers, checkpoints, resumption | Removed; Claude Code compaction plus each project's `RESUME.md` |
| Skills | 30 skills, 89 agents | The 7 skills above, 28 agents, and `/architect`; `/release` removed |
| Platforms | macOS first, Windows in progress | macOS, Linux and Windows, all tested in CI |

[CHANGELOG.md](CHANGELOG.md) lists every change.

## Attribution and licence

- Derived from geekatron/jerry at tag `v0.31.9`, commit
  `4aff242854ebb1bc74208991901b88c559be5a19`. [UPSTREAM.md](UPSTREAM.md) records the import.
- Licensed under the [Apache License 2.0](LICENSE). [NOTICE](NOTICE) keeps upstream's
  attribution and adds this derivative's. Every file modified from upstream carries a notice
  saying so, and [upstream-manifest.txt](upstream-manifest.txt) records the upstream version of
  each imported file.
- "Jerry" is the upstream project's name. This repository uses it to identify where the work
  comes from.

<!-- Modified from geekatron/jerry v0.31.9; see NOTICE. -->
