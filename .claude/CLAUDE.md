# CLAUDE.md

Developer context for working in this repository. Claude Code does not load this file for people who
install the plugin.

## What this is

Jerry is a Claude Code plugin for project-based work. It discovers projects (`PROJ-NNN-slug` folders
holding a `project.toml` and a `RESUME.md`), keeps a per-session focus of one or more of them, and
ships skills and agents that write their output into the focused project.

## Layout

| Path | Holds |
|------|-------|
| `src/jerry` | The `jerry` CLI (`projects`, `focus`, `ast`), project discovery, the session focus and the hook output |
| `hooks` | `hooks.json` and `run.py`, which runs the SessionStart and SubagentStart hooks |
| `skills`, `commands` | The skills with their agents, and the `/architect` command |
| `.context` | Rules and templates the skills read |
| `docs` | Governance, exemplar templates and schemas the skills read |
| `tests` | The pytest suite |

## Working here

- Test-first: write the test, watch it fail, then write the code.
- Run the tests with `uv run --group test pytest`.
- CI runs 6 cells (ubuntu, windows and macos on Python 3.11 and 3.14) with a 90% coverage floor, and a
  hook smoke job per OS (`tests/hook_smoke.py`) that runs the hooks as Claude Code starts them.
- `hooks/run.py`, `src/jerry/hooks.py`, `projects.py` and `session.py` use the standard library only:
  the hooks run without the project environment.
- Test fixtures are generic or Dragon Ball Z; no third-party names.

## Licence

This repository derives from geekatron/jerry v0.31.9 under the Apache License 2.0; `UPSTREAM.md`
records the source and `upstream-manifest.txt` the imported files. An upstream file you modify
carries the notice `Modified from geekatron/jerry v0.31.9; see NOTICE.` as a comment (an HTML
comment in markdown); one that cannot hold a comment is listed in `UPSTREAM.md` instead. New files
carry an SPDX header. `tests/test_license.py` enforces this.

<!-- Modified from geekatron/jerry v0.31.9; see NOTICE. -->
