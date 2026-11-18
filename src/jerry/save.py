# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Commit, and optionally push, project state: ``jerry projects save``."""

from __future__ import annotations

import contextlib
import os
import re
import subprocess
from pathlib import Path

from jerry import projects

SCRATCHPAD = re.compile(r"/tmp/claude-\d+/")
SECRET = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----"
    r"|\bgh[pousr]_[A-Za-z0-9]{36,}|\bgithub_pat_\w{40,}"
    r"|\b(?:AKIA|ASIA)[0-9A-Z]{16}\b"
    r"|\bxox[abposr]-[0-9A-Za-z-]{10,}"
    r"|\bsk-ant-[\w-]{20,}"
    r"|\beyJ[\w-]{10,}\.eyJ[\w-]{10,}\.[\w-]{10,}"
)


class SaveError(Exception):
    """A save step failed; the message says which and what was left behind."""


def _plural(count: int, noun: str) -> str:
    return f"{count} {noun}{'' if count == 1 else 's'}"


def _git(top: Path, *args: str, stdin: str | None = None) -> str:
    result = subprocess.run(
        ["git", "-C", str(top), *args],
        input=stdin,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    if result.returncode:
        raise SaveError(f"git {args[0]}: {(result.stderr or result.stdout).strip()}")
    return result.stdout


def scrub(text: str, home: str) -> list[tuple[int, str]]:
    """Return ``(line, kind)`` for the first home path, scratchpad path and secret in ``text``.

    Backslashes, single or JSON-escaped, count as slashes. The matched text is never returned.
    """
    flat = text.replace("\\\\", "/").replace("\\", "/")
    checks = [("scratchpad path", SCRATCHPAD), ("secret", SECRET)]
    if Path(home).name:
        checks.insert(0, ("home path", re.compile(re.escape(home) + r"(?![\w-])", re.IGNORECASE)))
    hits = ((kind, pattern.search(flat)) for kind, pattern in checks)
    return [(flat.count("\n", 0, match.start()) + 1, kind) for kind, match in hits if match]


def _scrub_files(top: Path, paths: list[str]) -> list[str]:
    unstaged = _git(top, "ls-files", "-z", "--modified", "--others", "--exclude-standard", "--", *paths)
    staged = _git(top, "diff", "--cached", "--name-only", "-z", "--", *paths)
    home = Path.home().as_posix()
    hits = []
    for rel in sorted(set(filter(None, (unstaged + staged).split("\0")))):
        try:
            data = (top / rel).read_bytes()
        except (FileNotFoundError, IsADirectoryError):
            continue
        if b"\0" not in data:
            hits += [f"{rel}:{line}: {kind}" for line, kind in scrub(data.decode("utf-8", "replace"), home)]
    return hits


def _push(top: Path) -> None:
    try:
        _git(top, "pull", "-q", "--rebase", "--autostash")
    except SaveError as exc:
        subprocess.run(["git", "-C", str(top), "rebase", "--abort"], capture_output=True)
        raise SaveError(f"{top.as_posix()}: pull failed, nothing pushed; any rebase was aborted: {exc}") from None
    _git(top, "push", "-q")


_FROM_STDIN = ("--pathspec-from-file=-", "--pathspec-file-nul")
FOLDER_ID = re.compile(r"PROJ-\d{3}(?:\.\d+)*(?!\d|\.\d)")


def _nul_joined(paths: list[str], literal: list[str]) -> str:
    """Join pathspecs for ``--pathspec-file-nul``; each of ``literal`` is matched as exactly that file name.

    ``:(literal)`` magic is refused when the caller's environment already sets ``GIT_LITERAL_PATHSPECS``,
    and that mode makes the plain name literal anyway.
    """
    caller_is_literal = os.environ.get("GIT_LITERAL_PATHSPECS", "").lower() in {"1", "true", "yes", "on"}
    magic = "" if caller_is_literal else ":(literal)"
    return "\0".join([*paths, *(f"{magic}{name}" for name in literal)])


def _folder_id(name: str) -> str | None:
    match = FOLDER_ID.match(name)
    return match.group(0) if match else None


def _abandoned_files(top: Path, root: Path, folders: set[Path]) -> tuple[list[str], list[str]]:
    """Return the files of renamed-away project folders as ``(in HEAD, only in the index)``.

    A folder is renamed away when it is a top-level folder under ``root`` that is not saved, starts with the
    project ID of one that is, and has either lost its ``project.toml`` or lost every tracked file. A
    same-prefix folder that still holds tracked files is a different folder and is left alone. The abandoned
    files are those missing from the working tree. Comparing with HEAD and with the index together catches
    every way to rename: ``mv``, ``git mv``, ``git rm``, and files that were staged but never committed.
    """
    wanted = {_folder_id(folder.name) for folder in folders} - {None}
    saved = {folder.name for folder in folders}
    depth = len(root.relative_to(top).parts)
    scope = root.relative_to(top).as_posix()

    def listed(listing: str) -> list[str]:
        return [name for name in listing.split("\0") if name and len(name.split("/")) > depth + 1]

    tracked = listed(_git(top, "ls-files", "-z", "--", scope))
    try:
        _git(top, "rev-parse", "--verify", "--quiet", "HEAD")
    except SaveError:
        in_head = []
    else:
        in_head = listed(_git(top, "diff", "--name-only", "--no-renames", "--diff-filter=D", "-z", "HEAD", "--", scope))
        prefix = "" if scope == "." else f"{scope}/"
        try:
            names = _git(top, "ls-tree", "-r", "-z", "--name-only", "HEAD" if scope == "." else f"HEAD:{scope}")
        except SaveError:
            names = ""
        tracked += listed("\0".join(prefix + name for name in names.split("\0") if name))
    in_index = listed(_git(top, "ls-files", "-z", "--deleted", "--", scope))
    missing = set(in_head) | set(in_index)
    surviving = {name.split("/")[depth] for name in set(tracked) - missing}
    renamed_away = {
        parts[depth]
        for parts in (name.split("/") for name in tracked)
        if parts[depth] not in saved
        and _folder_id(parts[depth]) in wanted
        and "/".join(parts) in missing
        and (parts[depth] not in surviving or parts[depth + 1 :] == ["project.toml"])
    }

    def belonging(names: list[str]) -> list[str]:
        return [name for name in names if name.split("/")[depth] in renamed_away]

    return belonging(in_head), belonging([name for name in in_index if name not in in_head])


def _save_root(root: Path, folders: set[Path], message: str, push: bool) -> str:
    try:
        top = Path(_git(root, "rev-parse", "--show-toplevel").strip()).resolve()
    except SaveError:
        raise SaveError(f"{root.as_posix()}: not in a git repository; nothing to save") from None
    targets = [*folders, root / projects.REGISTRY]
    paths = sorted(p.relative_to(top).as_posix() for p in targets if p.exists())
    hits = _scrub_files(top, paths)
    if hits:
        raise SaveError(f"{root.as_posix()}: not saved; remove or redact these first:\n  " + "\n  ".join(hits))
    abandoned, staged_only = _abandoned_files(top, root, folders)
    _git(top, "add", "-A", "--", *paths)
    if abandoned or staged_only:
        _git(
            top,
            "rm",
            "--cached",
            "-q",
            "--ignore-unmatch",
            *_FROM_STDIN,
            stdin=_nul_joined([], abandoned + staged_only),
        )
    staged = _git(top, "diff", "--cached", "--name-only", "--", *paths).split("\n")
    count = len(list(filter(None, staged))) + len(abandoned)
    if count:
        _git(top, "commit", "-q", "--only", "-m", message, *_FROM_STDIN, stdin=_nul_joined(paths, abandoned))
        sha = _git(top, "rev-parse", "--short", "HEAD").strip()
        report = f"committed {sha} ({_plural(count, 'file')})"
    else:
        report = "nothing to commit"
    if push:
        _push(top)
        report += "; pushed"
    return f"{root.as_posix()}: {report}"


def save_projects(found: projects.Discovery, ids: list[str], message: str, push: bool = False) -> list[str]:
    """Commit each project's top-level folder and its root's README.md; with ``push``, pull, rebase and push.

    Each of ``ids`` is a project ID or a project folder path.
    Refreshes the registries first and refuses on any ``check`` error or scrub hit.
    Returns one report line per root. Raises SaveError; roots saved before the failure stay saved.
    """
    if not ids:
        raise SaveError("no projects to save: pass project IDs or focus a project")
    chosen = [projects.project_at(found, i) or found.projects.get(i) for i in ids]
    if None in chosen:
        raise SaveError(f"unknown project: {', '.join(i for i, p in zip(ids, chosen, strict=True) if p is None)}")
    folders: dict[Path, set[Path]] = {}
    for p in chosen:
        folders.setdefault(p.root, set()).add(p.root / p.path.relative_to(p.root).parts[0])
    for root in folders:
        with contextlib.suppress(OSError, ValueError):
            projects.sync_registry(found, root, write=True)
    errors, _ = projects.check(found)
    if errors:
        listed = "\n  ".join(errors)
        raise SaveError(f"jerry projects check reports {_plural(len(errors), 'error')}:\n  {listed}")
    return [_save_root(root, root_folders, message, push) for root, root_folders in folders.items()]
