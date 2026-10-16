# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Project model and discovery.

A project is a folder named ``PROJ-<NNN>[.<n>...]-<slug>`` that holds a
``project.toml``. Sub-projects sit directly inside their parent project and
extend its number (``PROJ-004/PROJ-004.1-<slug>``). Projects are found under
roots, nearest first:

1. the enclosing root: the nearest ancestor of the start directory (or the
   start directory itself) that holds a project and is not a project itself;
2. ``<start>/projects``;
3. ``<start>/../projects``;
4. the ``roots`` listed in ``~/.jerry/config.toml``.

All roots contribute; when two roots define the same ID the nearer one wins.
This module uses the standard library only, so hooks can import it without
the project environment.
"""

from __future__ import annotations

import os
import re
import tomllib
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_FILE = "project.toml"
STATUSES = ("active", "paused", "done", "abandoned")
LINK_TYPES = ("related", "depends_on", "supersedes", "uses")
INVERSES = {"related": "related", "depends_on": "blocks", "supersedes": "superseded_by", "uses": "used_by"}
SHOWN_LINKS = ("related", "depends_on", "blocks", "supersedes", "superseded_by", "uses", "used_by")
KNOWN_FILES = ("RESUME.md", "WORKTRACKER.md", "PLAN.md", "ORCHESTRATION.yaml")
MAX_SLUG = 40

_FOLDER = re.compile(r"^(PROJ-(\d{3}(?:\.\d+)*))-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")
_ID = re.compile(r"^PROJ-\d{3}(?:\.\d+)*$")
_KEYS = {"title", "status", "summary", *LINK_TYPES}


@dataclass(frozen=True)
class FolderName:
    id: str
    number: tuple[int, ...]
    slug: str


@dataclass(frozen=True, eq=False)
class Project:
    id: str
    number: tuple[int, ...]
    slug: str
    path: Path
    root: Path
    parent: str | None
    title: str
    status: str
    summary: str
    links: dict[str, tuple[str, ...]]

    @property
    def depth(self) -> int:
        return len(self.number) - 1


@dataclass
class Discovery:
    roots: list[Path]
    projects: dict[str, Project] = field(default_factory=dict)
    all_projects: list[Project] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    def children(self, project_id: str) -> list[Project]:
        return [p for p in self.projects.values() if p.parent == project_id]

    def resolve(self, project_id: str, from_root: Path) -> Project | None:
        local = next((p for p in self.all_projects if p.id == project_id and p.root == from_root), None)
        return local or self.projects.get(project_id)

    def inverse_links(self, project_id: str) -> dict[str, list[str]]:
        target = self.projects.get(project_id)
        inverse: dict[str, list[str]] = {}
        for p in self.projects.values():
            for link_type, ids in p.links.items():
                if project_id in ids and target is not None and self.resolve(project_id, p.root) is target:
                    inverse.setdefault(INVERSES[link_type], []).append(p.id)
        return {key: sorted(set(ids)) for key, ids in inverse.items()}


def parse_folder(name: str) -> FolderName | None:
    """Parse a project folder name, or return None if it is not one."""
    match = _FOLDER.match(name)
    if match is None or len(match.group(3)) > MAX_SLUG:
        return None
    return FolderName(match.group(1), tuple(int(n) for n in match.group(2).split(".")), match.group(3))


def parse_config(text: str, label: str) -> tuple[list[str], list[str]]:
    """Return the ``roots`` entries of a config file's text, and any warnings."""
    try:
        data = tomllib.loads(text)
    except tomllib.TOMLDecodeError as exc:
        return [], [f"{label}: cannot parse: {exc}"]
    roots = data.get("roots", [])
    if not isinstance(roots, list) or not all(isinstance(r, str) for r in roots):
        return [], [f"{label}: roots must be a list of strings"]
    return roots, []


def config_roots() -> tuple[list[Path], list[str]]:
    """Return the existing absolute roots from ``~/.jerry/config.toml``, and any warnings."""
    path = Path.home() / ".jerry" / "config.toml"
    if not path.is_file():
        return [], []
    label = path.as_posix()
    try:
        entries, warnings = parse_config(path.read_text(encoding="utf-8-sig"), label)
    except (OSError, UnicodeDecodeError) as exc:
        return [], [f"{label}: cannot read: {exc}"]
    roots = []
    for entry in entries:
        root = Path(entry).expanduser()
        if not root.is_absolute():
            warnings.append(f"{label}: root '{entry}' is not an absolute path; skipped")
        elif not root.is_dir():
            warnings.append(f"{label}: root '{entry}' not found; skipped")
        else:
            roots.append(root)
    return roots, warnings


def _subdirs(folder: Path) -> list[Path]:
    try:
        return sorted((p for p in folder.iterdir() if p.is_dir()), key=lambda p: p.name)
    except OSError:
        return []


def _holds_project(folder: Path) -> bool:
    return any(parse_folder(d.name) and (d / PROJECT_FILE).is_file() for d in _subdirs(folder))


def _enclosing_root(start: Path) -> Path | None:
    for folder in (start, *start.parents):
        if not (folder / PROJECT_FILE).is_file() and _holds_project(folder):
            return folder
    return None


def _candidate_roots(start: Path) -> list[Path]:
    enclosing = _enclosing_root(start)
    local = [start / "projects", start.parent / "projects"]
    return ([enclosing] if enclosing else []) + local


def _dedupe(candidates: list[Path]) -> list[Path]:
    roots: list[Path] = []
    for candidate in candidates:
        if candidate.is_dir() and not any(os.path.samefile(candidate, r) for r in roots):
            roots.append(candidate.resolve())
    return roots


def _load(path: Path) -> tuple[dict | None, str | None]:
    try:
        data = tomllib.loads(path.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, tomllib.TOMLDecodeError) as exc:
        return None, f"cannot parse: {exc}"
    unknown = sorted(set(data) - _KEYS)
    if unknown:
        return None, f"unknown key(s): {', '.join(unknown)}"
    if not isinstance(data.get("title"), str) or not data["title"].strip():
        return None, "title must be a non-empty string"
    if data.get("status") not in STATUSES:
        return None, f"status must be one of {', '.join(STATUSES)}"
    if not isinstance(data.get("summary"), str):
        return None, "summary must be a string"
    for link_type in LINK_TYPES:
        ids = data.get(link_type, [])
        if not isinstance(ids, list) or not all(isinstance(i, str) and _ID.match(i) for i in ids):
            return None, f"{link_type} must be a list of project IDs"
    return data, None


def _scan(root: Path, found: Discovery) -> list[Project]:
    in_root: dict[str, Project] = {}

    def walk(folder: Path, parent: Project | None) -> None:
        for child in _subdirs(folder):
            if not (child / PROJECT_FILE).is_file():
                continue
            name = parse_folder(child.name)
            if name is None:
                if child.name.startswith("PROJ-"):
                    found.warnings.append(
                        f"{child.as_posix()}: not a valid project folder name "
                        f"(PROJ-<NNN>[.<n>...]-<slug>, lowercase slug of at most {MAX_SLUG} characters); skipped"
                    )
                continue
            data, error = _load(child / PROJECT_FILE)
            if error:
                found.errors.append(f"{child.as_posix()}/{PROJECT_FILE}: {error}")
                continue
            if name.id in in_root:
                found.errors.append(
                    f"{name.id} is defined twice in {root.as_posix()}: "
                    f"{in_root[name.id].path.name} and {child.name}"
                )
                continue
            if parent is not None and name.number[:-1] != parent.number:
                found.errors.append(f"{name.id} sits inside {parent.id} but its number does not extend {parent.id}")
            elif parent is None and len(name.number) > 1:
                found.errors.append(f"{name.id} has a sub-project number but sits at the top of {root.as_posix()}")
            project = Project(
                id=name.id,
                number=name.number,
                slug=name.slug,
                path=child.resolve(),
                root=root,
                parent=parent.id if parent else None,
                title=data["title"],
                status=data["status"],
                summary=data["summary"],
                links={t: tuple(data.get(t, [])) for t in LINK_TYPES if data.get(t)},
            )
            in_root[name.id] = project
            walk(child, project)

    walk(root, None)
    return sorted(in_root.values(), key=lambda p: p.number)


def discover(start: Path, roots: list[Path] | None = None) -> Discovery:
    """Find every project reachable from ``start``, or under exactly ``roots`` when given."""
    warnings: list[str] = []
    if roots is None:
        configured, warnings = config_roots()
        candidates = _candidate_roots(start.resolve()) + configured
    else:
        candidates = []
        for root in roots:
            if root.is_dir():
                candidates.append(root)
            else:
                warnings.append(f"root '{root.as_posix()}' not found; skipped")
    found = Discovery(roots=_dedupe(candidates), warnings=warnings)

    for root in found.roots:
        shadowed = []
        for project in _scan(root, found):
            found.all_projects.append(project)
            if project.id in found.projects:
                shadowed.append(project.id)
            else:
                found.projects[project.id] = project
        if shadowed:
            found.warnings.append(
                f"{root.as_posix()}: {', '.join(shadowed)} shadowed by the same ID in a nearer root; ignored"
            )

    for project in found.projects.values():
        for link_type, ids in project.links.items():
            for target in ids:
                if target == project.id:
                    found.errors.append(f"{project.id} lists itself under {link_type}")
                elif found.resolve(target, project.root) is None:
                    found.errors.append(f"{project.id} {link_type} {target}, which is not a known project")
    return found


def render_list(found: Discovery) -> str:
    """Render the discovered projects grouped by root, indented by depth."""
    if not found.projects:
        return (
            "No projects found. Run from a directory next to a projects/ folder, "
            "or list roots in ~/.jerry/config.toml.\n"
        )
    lines = []
    for root in found.roots:
        rows = [p for p in found.projects.values() if p.root == root]
        if rows:
            lines.append(root.as_posix())
            lines += [f"{'  ' * (p.depth + 1)}{p.id}  [{p.status}]  {p.title}" for p in rows]
    return "\n".join(lines) + "\n"


def render_show(found: Discovery, project_id: str) -> str | None:
    """Render one project with its links, computed inverses and known files."""
    p = found.projects.get(project_id)
    if p is None:
        return None
    lines = [
        f"{p.id}  {p.title}",
        f"status: {p.status}",
        f"summary: {p.summary}",
        f"path: {p.path.as_posix()}",
        f"root: {p.root.as_posix()}",
    ]
    if p.parent:
        lines.append(f"parent: {p.parent}")
    children = found.children(p.id)
    if children:
        lines.append(f"children: {', '.join(c.id for c in children)}")
    inverse = found.inverse_links(p.id)
    for link_type in SHOWN_LINKS:
        ids = sorted(set(p.links.get(link_type, ())) | set(inverse.get(link_type, ())))
        if ids:
            lines.append(f"{link_type}: {', '.join(ids)}")
    files = [name for name in KNOWN_FILES if (p.path / name).is_file()]
    if files:
        lines.append(f"files: {', '.join(files)}")
    return "\n".join(lines) + "\n"
