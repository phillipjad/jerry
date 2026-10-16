# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Per-session state: the roots a session sees and the projects it focuses on.

Each Claude Code session has a file ``~/.jerry/sessions/<session_id>.json``
holding ``{"cwd", "roots", "none", "focus": [{"id", "path"}]}``. The stored
roots fix what the session sees, so changing directory mid-session does not
change discovery. The first focus entry is the primary project. This module
uses the standard library only, so hooks can import it without the project
environment.
"""

from __future__ import annotations

import contextlib
import json
import os
import re
import tempfile
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from jerry import projects

ENV = "CLAUDE_CODE_SESSION_ID"
REPLACE_ATTEMPTS = 5

_SESSION_ID = re.compile(r"[A-Za-z0-9_-]{1,128}")


class SessionError(Exception):
    """A session id or session file that cannot be used."""


@dataclass
class Session:
    cwd: str
    roots: list[str]
    none: bool = False
    focus: list[dict[str, str]] = field(default_factory=list)


def session_path(sid: str) -> Path:
    """Return the session file for ``sid``.

    The id becomes a file name, so anything but 1-128 letters, digits, ``_``
    or ``-`` raises SessionError instead of becoming a path.
    """
    if not _SESSION_ID.fullmatch(sid):
        raise SessionError(f"invalid session id {sid!r}: use 1-128 letters, digits, '_' or '-'")
    return Path.home() / ".jerry" / "sessions" / f"{sid}.json"


def session_id(given: str | None) -> str | None:
    """Return the checked session id: ``given``, else ``$CLAUDE_CODE_SESSION_ID``, else None."""
    value = given if given is not None else os.environ.get(ENV)
    if value is not None:
        session_path(value)
    return value


def _valid(data: object) -> bool:
    def strings(items: object) -> bool:
        return isinstance(items, list) and all(isinstance(i, str) for i in items)

    return (
        isinstance(data, dict)
        and isinstance(data.get("cwd"), str)
        and strings(data.get("roots"))
        and isinstance(data.get("none"), bool)
        and isinstance(data.get("focus"), list)
        and all(isinstance(e, dict) and strings([e.get("id"), e.get("path")]) for e in data["focus"])
    )


def load(sid: str) -> Session | None:
    """Return the stored session, or None if it has no file yet."""
    path = session_path(sid)
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        return None
    except (OSError, ValueError) as exc:
        raise SessionError(f"{path.as_posix()}: cannot read session file: {exc}") from None
    if not _valid(data):
        raise SessionError(f"{path.as_posix()}: not a valid session file")
    focus = [{"id": e["id"], "path": e["path"]} for e in data["focus"]]
    return Session(cwd=data["cwd"], roots=data["roots"], none=data["none"], focus=focus)


def save(sid: str, session: Session) -> None:
    """Write the session file atomically: a temporary file, then ``os.replace``.

    On Windows the target can be briefly locked by another reader, which
    surfaces as ``PermissionError``; the replace is retried a few times.
    """
    path = session_path(sid)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(dir=path.parent, prefix=f".{sid}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as handle:
            json.dump(asdict(session), handle, indent=2)
        for attempt in range(REPLACE_ATTEMPTS):
            try:
                os.replace(temp, path)
                break
            except PermissionError:
                if attempt == REPLACE_ATTEMPTS - 1:
                    raise
                time.sleep(0.05)
    finally:
        with contextlib.suppress(OSError):
            os.unlink(temp)


def start(cwd: Path) -> Session:
    """Return a new, unsaved session that sees the roots discovered from ``cwd``."""
    return Session(cwd=cwd.as_posix(), roots=[root.as_posix() for root in projects.discover(cwd).roots])


def prune(current_id: str, days: int = 30) -> None:
    """Delete session files untouched for ``days`` days, never the current one."""
    cutoff = time.time() - days * 86400
    for path in session_path(current_id).parent.glob("*.json"):
        with contextlib.suppress(OSError):
            if path.stem != current_id and path.stat().st_mtime < cutoff:
                path.unlink()


def _paths(found: projects.Discovery, project_id: str) -> list[str]:
    return [p.path.as_posix() for p in found.all_projects if p.id == project_id]


def focus_entries(found: projects.Discovery, ids: list[str]) -> list[dict[str, str]]:
    """Return focus entries for ``ids`` in order, without duplicates.

    Raises SessionError naming every ID that is unknown, or found in more than
    one root, before anything is changed.
    """
    entries, problems = [], []
    for project_id in dict.fromkeys(ids):
        found_at = _paths(found, project_id)
        if not found_at:
            problems.append(f"unknown project: {project_id}")
        elif len(found_at) > 1:
            problems.append(f"{project_id} is ambiguous; found at:\n  " + "\n  ".join(found_at))
        else:
            entries.append({"id": project_id, "path": found_at[0]})
    if problems:
        raise SessionError("\n".join(problems))
    return entries


def refresh(session: Session, found: projects.Discovery) -> bool:
    """Re-resolve by ID each focused project whose folder is gone; return True if any moved."""
    changed = False
    for entry in session.focus:
        if not Path(entry["path"]).is_dir():
            found_at = _paths(found, entry["id"])
            if len(found_at) == 1:
                entry["path"] = found_at[0]
                changed = True
    return changed


def _pick_up_here(project_dir: Path) -> str | None:
    try:
        return projects.pick_up_here((project_dir / "RESUME.md").read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError):
        return None


def render_head(session: Session, found: projects.Discovery) -> str:
    """Render the focus state: none, nothing, or each project with the primary marked and ``{project_dir}``."""
    if session.none:
        return "Focus: none. This session works without a project.\n"
    if not session.focus:
        return "Focus: nothing is focused.\n"
    by_path = {p.path.as_posix(): p for p in found.all_projects}
    lines = ["Focus:"]
    for index, entry in enumerate(session.focus):
        project = by_path.get(entry["path"])
        label = f"[{project.status}]  {project.title}" if project else "(not found under the session roots)"
        lines.append(f"{entry['id']}  {label}" + ("  (primary)" if index == 0 else ""))
        lines.append(f"  path: {entry['path']}")
    lines.append(f"{{project_dir}} = {session.focus[0]['path']}")
    return "\n".join(lines) + "\n"


def render_resume(entry: dict[str, str]) -> str:
    """Render one focused project's Pick up here section, after a blank line."""
    section = _pick_up_here(Path(entry["path"]))
    return f"\n{entry['id']} RESUME.md:\n{section or 'No Pick up here section; read RESUME.md.'}\n"


def render(session: Session, found: projects.Discovery) -> str:
    """Render the focus: each project with the primary marked, then each Pick up here section."""
    return render_head(session, found) + "".join(render_resume(entry) for entry in session.focus)
