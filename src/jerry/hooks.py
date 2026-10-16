# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""SessionStart and SubagentStart hook output.

Each hook takes the parsed hook input and returns the JSON object Claude Code
reads, or None for no output. This module uses the standard library only:
``hooks/run.py`` imports it without the project environment.
"""

from __future__ import annotations

import contextlib
import os
from pathlib import Path

from jerry import projects, session

PLUGIN_ROOT = Path(__file__).resolve().parents[2]
BUDGET = 9000
SUBAGENT_BUDGET = 300
TRUNCATED = "\n[truncated to fit the context budget]"
ASK = (
    "Focus: nothing is focused. When tracked work starts (multi-step work, or changes to files or external "
    "systems) and the user has not named a project, ask them to pick one of the projects below, create one "
    "(`projects new <slug>`), or work without one (`focus none`), then run the focus command (`focus set <id>` "
    "for a picked or named project). Quick questions skip this. If you cannot ask (non-interactive), use none.\n"
)
SUBAGENT_TAIL = ". Use the project the task names, else the primary; never run focus commands."
LITERAL_ROOT = (
    "A literal ${CLAUDE_PLUGIN_ROOT} in a Jerry file opened with Read, or in a Bash command, means this path."
)


def units(text: str) -> int:
    """Return the length of ``text`` in UTF-16 code units, the measure of Claude Code's context cap."""
    return len(text.encode("utf-16-le", "surrogatepass")) // 2


def fit(text: str) -> str:
    """Return ``text``, or its start plus a truncation marker, within the budget of UTF-16 units."""
    if units(text) <= BUDGET:
        return text
    keep = text.encode("utf-16-le", "surrogatepass")[: 2 * (BUDGET - units(TRUNCATED))]
    return keep.decode("utf-16-le", "ignore") + TRUNCATED


def _field(payload: object, name: str) -> str:
    value = payload.get(name) if isinstance(payload, dict) else None
    if not isinstance(value, str):
        raise ValueError(f"hook input has no {name}")
    return value


def _output(event: str, text: str) -> dict:
    return {"hookSpecificOutput": {"hookEventName": event, "additionalContext": text}}


def _last_focus(sid: str, cwd: str) -> list[str]:
    newest, ids = 0.0, []
    for path in session.session_path(sid).parent.glob("*.json"):
        with contextlib.suppress(OSError, session.SessionError):
            other = session.load(path.stem) if path.stem != sid else None
            mtime = path.stat().st_mtime
            if other and other.cwd == cwd and other.focus and mtime > newest:
                newest, ids = mtime, [entry["id"] for entry in other.focus]
    return ids


def _warnings(found: projects.Discovery) -> list[str]:
    warnings = [*found.warnings, *found.errors, *projects.config_roots()[1]]
    for root in found.roots:
        label = (root / projects.REGISTRY).as_posix()
        try:
            if projects.sync_registry(found, root):
                warnings.append(f"{label}: registry is stale; run `projects index --write`")
        except (OSError, ValueError) as exc:
            warnings.append(f"{label}: {exc}")
    return warnings


def _one_line(text: str) -> str:
    return " ".join(text.split())


def _row(p: projects.Project, summary: bool) -> str:
    meta = ([f"parent {p.parent}"] if p.parent else []) + [f"{t} {', '.join(ids)}" for t, ids in p.links.items()]
    row = f"- {p.id} [{p.status}] {_one_line(p.title)}" + (f" ({'; '.join(meta)})" if meta else "")
    return row + (f": {_one_line(p.summary)}" if summary and p.summary.strip() else "")


def _indexes(found: projects.Discovery) -> list[str]:
    """Return the index from fullest to tersest: each trim step drops more."""
    rows = sorted(found.projects.values(), key=lambda p: p.number)
    done = [p.id for p in rows if p.status == "done"]
    collapsed = [_row(p, False) for p in rows if p.status != "done"] + ([f"- done: {', '.join(done)}"] if done else [])

    def table(lines: list[str]) -> str:
        return "\nProjects:\n" + "".join(f"{line}\n" for line in lines)

    return [
        table([_row(p, True) for p in rows]),
        table([_row(p, p.status != "done") for p in rows]),
        table([_row(p, False) for p in rows]),
        table(collapsed),
        f"\nProjects (IDs only; `projects list` shows more): {', '.join(p.id for p in rows)}\n",
    ]


def session_start(payload: object) -> dict:
    """Return the SessionStart context: CLI, focus, Pick up here sections, warnings and project index.

    Creates the session file from the hook's ``cwd`` when it does not exist yet;
    an existing file (resume, compact) keeps its cwd, roots and focus, and its
    modification time is refreshed so another session's prune spares it.
    """
    sid = _field(payload, "session_id")
    state = session.load(sid)
    if state is None:
        state = session.start(Path(_field(payload, "cwd")))
        session.save(sid, state)
    else:
        with contextlib.suppress(OSError):
            os.utime(session.session_path(sid))
    session.prune(sid)
    found = projects.discover(Path(state.cwd), roots=[Path(root) for root in state.roots])
    cli = f'uv run --project "{PLUGIN_ROOT.as_posix()}" jerry'
    text = f"Jerry plugin root: {PLUGIN_ROOT.as_posix()}. {LITERAL_ROOT}\nJerry CLI: {cli} <command> --session {sid}\n"

    if state.none or state.focus:
        text += session.render_head(state, found)
    elif not found.roots:
        text += f"No projects root found from {state.cwd}; this session works without a project.\n"
    else:
        text += ASK
        last = _last_focus(sid, state.cwd) if payload.get("source") in ("clear", "fork") else []
        if last:
            text += (
                f"Last focus from this cwd: {', '.join(last)}. "
                f"Restore it with: {cli} focus set {' '.join(last)} --session {sid}\n"
            )

    for entry in state.focus:
        block = session.render_resume(entry)
        if units(text + block) > BUDGET:
            block = f"\n{entry['id']} RESUME.md: no room for its Pick up here; read {entry['path']}/RESUME.md\n"
        text += block

    warnings = _warnings(found)
    if warnings:
        text += "\nWarnings:\n" + "".join(f"- {_one_line(w)}\n" for w in warnings)

    if found.projects:
        indexes = _indexes(found)
        text += next((index for index in indexes if units(text + index) <= BUDGET), indexes[-1])
    return _output("SessionStart", fit(text))


def subagent_start(payload: object) -> dict | None:
    """Return the focus for a subagent in at most 300 characters, or None when nothing is focused."""
    state = session.load(_field(payload, "session_id"))
    if state is None or state.none or not state.focus:
        return None
    primary, *others = state.focus
    lead = f"Jerry focus: {{project_dir}} = {primary['path']} ({primary['id']}, primary)"
    variants = [
        lead + "".join(f"; {e['id']} = {e['path']}" for e in others) + SUBAGENT_TAIL,
        lead + (f"; also {', '.join(e['id'] for e in others)}" if others else "") + SUBAGENT_TAIL,
        lead + SUBAGENT_TAIL,
    ]
    text = next((v for v in variants if len(v) <= SUBAGENT_BUDGET), variants[-1][: SUBAGENT_BUDGET - 3] + "...")
    return _output("SubagentStart", text)
