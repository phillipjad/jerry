# Jerry (derivative)

An independent derivative of [Jerry Framework](https://github.com/geekatron/jerry), a Claude Code
plugin for project-based work: work tracking, orchestration, problem-solving, systems engineering
and adversarial quality review. It is licensed under the Apache License 2.0, like upstream, and
is not affiliated with or endorsed by the upstream project.

## Why this derivative exists

Upstream Jerry ties each session to exactly one project, named by the `JERRY_PROJECT`
environment variable before Claude Code starts. That model does not fit work that spans several
related projects, or teams that keep their projects in a shared repository next to the code they
change. This derivative is built for that kind of work:

- **Several projects per session.** A session keeps a focus set of one or more projects, chosen
  during the session instead of at launch. Subagents inherit it.
- **Projects found where they live.** Jerry looks in `./projects`, then `../projects`, then in
  roots listed in `~/.jerry/config.toml`, like other tooling that searches upward for its config.
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

## What changes

| Area | Upstream v0.31.9 | This derivative (target for 1.0.0) |
|---|---|---|
| Projects in scope | One, from `JERRY_PROJECT` | A per-session focus set of one or more projects |
| Project discovery | `projects/` under the Claude Code project directory | `./projects`, `../projects`, then configured roots |
| Project structure | Flat `PROJ-NNN-slug` folders | Nested sub-projects, `project.toml` metadata, typed links, a generated registry |
| Hooks | SessionStart, UserPromptSubmit, PreToolUse, PreCompact, Stop, SubagentStop | SessionStart and SubagentStart only, standard library only, no shell |
| Context monitoring | Context-fill tiers, checkpoints, resumption | Removed; Claude Code compaction plus each project's `RESUME.md` |
| Skills | 30 skills, 89 agents | adversary, architecture, ast, nasa-se, orchestration, problem-solving, worktracker; 28 agents |
| Platforms | macOS first, Windows in progress | macOS, Linux and Windows, all tested in CI |

## Status

The changes land as a series of pull requests. Until 1.0.0 is released, `main` may still
contain upstream behaviour that is due to be removed. See the open pull requests for what is in
progress.

## Attribution and licence

- Derived from geekatron/jerry at tag `v0.31.9`, commit
  `4aff242854ebb1bc74208991901b88c559be5a19`. [UPSTREAM.md](UPSTREAM.md) records the import.
- Licensed under the [Apache License 2.0](LICENSE). Upstream's attribution is kept in
  [NOTICE](NOTICE). Every file modified from upstream carries a notice saying so, and
  [upstream-manifest.txt](upstream-manifest.txt) records the upstream version of each imported
  file.
- "Jerry" is the upstream project's name. This repository uses it to identify where the work
  comes from.

<!-- Modified from geekatron/jerry v0.31.9; see NOTICE. -->
