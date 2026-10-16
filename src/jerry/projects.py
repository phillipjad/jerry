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

import contextlib
import os
import re
import shutil
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
MAX_PICK_UP = 3000
MAX_RELATIVE_PATH = 180
REGISTRY = "README.md"
INDEX_START = "<!-- jerry:index:start -->"
INDEX_END = "<!-- jerry:index:end -->"

_FOLDER = re.compile(r"^(PROJ-(\d{3}(?:\.\d+)*))-([a-z][a-z0-9]*(?:-[a-z0-9]+)*)$")
_ID = re.compile(r"^PROJ-\d{3}(?:\.\d+)*$")
_KEYS = {"title", "status", "summary", *LINK_TYPES}
_BAD_NAME = "not a valid project folder name"
_FENCE = re.compile(r"\s*(`{3,}(?=[^`]*$)|~{3,})")
_LINK = re.compile(r"\]\(\s*<?([^)>\s]+)")
_TOML_ESCAPES = {ord('"'): '\\"', ord("\\"): "\\\\"} | {c: f"\\u{c:04X}" for c in (*range(0x20), 0x7F)}


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
                    reason = (
                        f"slug is longer than {MAX_SLUG} characters"
                        if _FOLDER.match(child.name)
                        else f"PROJ-<NNN>[.<n>...]-<slug>, lowercase slug of at most {MAX_SLUG} characters"
                    )
                    found.warnings.append(f"{child.as_posix()}: {_BAD_NAME} ({reason}); skipped")
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


def pick_up_here(text: str) -> str | None:
    """Return the ``## Pick up here`` section if it is the first level-2 heading, else None.

    The section runs to the next level-1 or level-2 heading or the end, with LF
    line endings and trailing whitespace stripped. Headings inside fenced code
    blocks do not count.
    """
    lines = text.replace("\r\n", "\n").split("\n")
    fence = ""
    start = None
    for i, line in enumerate(lines):
        match = _FENCE.match(line)
        if fence:
            if match and match.group(1)[0] == fence[0] and len(match.group(1)) >= len(fence):
                fence = ""
        elif match:
            fence = match.group(1)
        elif start is None and line.startswith("## "):
            if not line[3:].startswith("Pick up here"):
                return None
            start = i
        elif start is not None and line.startswith(("# ", "## ")):
            return "\n".join(lines[start:i]).rstrip()
    return None if start is None else "\n".join(lines[start:]).rstrip()


def _link_child(resume: Path, line: str) -> None:
    """Add ``line`` to the end of the Pick up here section of ``resume``, else to the end of the file.

    A missing file is left missing. The file's BOM and newline style are kept.
    """
    try:
        raw = resume.read_bytes().decode("utf-8")
    except FileNotFoundError:
        return
    text = raw.replace("\r\n", "\n")
    section = pick_up_here(text.lstrip("\ufeff"))
    if section is None:
        text = f"{text.rstrip()}\n\n{line}\n"
    else:
        end = text.index(section) + len(section)
        text = f"{text[:end]}\n{line}{text[end:]}"
    resume.write_bytes((text.replace("\n", "\r\n") if "\r\n" in raw else text).encode("utf-8"))


def new_project(found: Discovery, slug: str, parent_id: str | None = None, title: str | None = None) -> Path:
    """Create the next-numbered project with ``project.toml`` and a RESUME.md stub; return its path.

    A top-level project is numbered after the highest number in any root and
    created in the nearest root; a sub-project after its parent's highest child,
    and the parent's RESUME.md gains a link to the new one.
    Raises ValueError or OSError, leaving nothing behind.
    """
    parent = found.projects.get(parent_id) if parent_id else None
    if parent_id and parent is None:
        raise ValueError(f"unknown parent project: {parent_id}")
    if not found.roots:
        raise ValueError("no projects root found; create a projects/ folder or pass --root")
    base = parent.number if parent else ()
    folders = [parse_folder(d.name) for c in ([parent.path] if parent else found.roots) for d in _subdirs(c)]
    taken = [
        p.number[len(base)]
        for p in [*found.all_projects, *filter(None, folders)]
        if p.number[: len(base)] == base and p.number != base
    ]
    number = max(taken, default=0) + 1
    project_id = f"{parent.id}.{number}" if parent else f"PROJ-{number:03d}"
    name = f"{project_id}-{slug}"
    if parse_folder(name) is None:
        raise ValueError(
            f"'{name}' is not a valid project folder name: the slug needs lowercase letters, digits and "
            f"single hyphens, starting with a letter, at most {MAX_SLUG} characters"
        )
    title = title if title and title.strip() else slug
    root = parent.root if parent else found.roots[0]
    path = (parent.path if parent else root) / name
    path.mkdir()
    try:
        (path / PROJECT_FILE).write_text(
            f'title = "{title.translate(_TOML_ESCAPES)}"\nstatus = "active"\nsummary = ""\n', encoding="utf-8"
        )
        (path / "RESUME.md").write_text(
            f"# {project_id} -- Resume\n\n## Pick up here\n\n- Write the first next step here.\n", encoding="utf-8"
        )
        after = discover(path, roots=found.roots)
        if any(p.id == project_id and p.path != path.resolve() for p in after.all_projects) or any(
            e.startswith(f"{project_id} is defined twice") for e in after.errors
        ):
            raise ValueError(f"{project_id} was also created elsewhere at the same time; removed ours, run new again")
        if parent:
            _link_child(parent.path / "RESUME.md", f"- [{project_id}]({name}/RESUME.md) {' '.join(title.split())}")
    except BaseException:
        shutil.rmtree(path, ignore_errors=True)
        raise
    with contextlib.suppress(OSError, ValueError):
        sync_registry(after, root, write=True)
    return path


def render_index(found: Discovery, root: Path) -> str:
    """Render the registry table of every project in ``root``, in number order."""
    rows = ["| ID | Title | Status | Summary | Links |", "|---|---|---|---|---|"]
    for p in found.all_projects:
        if p.root == root:
            links = "; ".join(f"{link_type} {', '.join(ids)}" for link_type, ids in p.links.items())
            cells = (" ".join(c.splitlines()).replace("|", "\\|") for c in (p.id, p.title, p.status, p.summary, links))
            rows.append("| " + " | ".join(cells) + " |")
    return "\n".join(rows) + "\n"


def _splice(text: str, table: str) -> str | None:
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if line.strip() == INDEX_START]
    ends = [i for i, line in enumerate(lines) if line.strip() == INDEX_END]
    if not starts and not ends:
        return None
    if len(starts) != 1 or len(ends) != 1 or starts[0] > ends[0]:
        raise ValueError(f"expected one '{INDEX_START}' line followed by one '{INDEX_END}' line")
    newline = "\r\n" if lines[starts[0]].endswith("\r\n") else "\n"
    return "".join([*lines[: starts[0] + 1], *(row + newline for row in table.splitlines()), *lines[ends[0] :]])


def sync_registry(found: Discovery, root: Path, write: bool = False) -> bool | None:
    """Compare, and with ``write`` rewrite, the table between the markers of ``root``'s README.md.

    Returns None when there is no README.md or it has no marker lines, True when
    the table was out of date, False when it was current. Raises ValueError on
    misplaced markers. The file's BOM and newline style are kept.
    """
    readme = root / REGISTRY
    try:
        text = readme.read_bytes().decode("utf-8")
    except FileNotFoundError:
        return None
    updated = _splice(text, render_index(found, root))
    if updated is None or updated == text:
        return None if updated is None else False
    if write:
        readme.write_bytes(updated.encode("utf-8"))
    return True


def _check_resume(found: Discovery, p: Project) -> list[str]:
    resume = p.path / "RESUME.md"
    label = resume.as_posix()
    try:
        text = resume.read_text(encoding="utf-8-sig")
    except FileNotFoundError:
        return [f"{label}: missing"]
    except (OSError, UnicodeDecodeError) as exc:
        return [f"{label}: cannot read: {exc}"]
    errors = []
    section = pick_up_here(text)
    if section is None:
        errors.append(f"{label}: must open with '## Pick up here' (its first level-2 heading)")
    elif len(section) > MAX_PICK_UP:
        errors.append(f"{label}: '## Pick up here' is {len(section):,} characters; the maximum is {MAX_PICK_UP:,}")
    targets = {(p.path / target.split("#")[0]).resolve() for target in _LINK.findall(text)}
    for child in found.all_projects:
        if child.root == p.root and child.parent == p.id and (child.path / "RESUME.md").resolve() not in targets:
            errors.append(f"{label}: does not link to {child.id}'s RESUME.md")
    return errors


def _check_paths(p: Project) -> list[str]:
    errors = []
    for folder, dirs, files in os.walk(p.path):
        base = Path(p.path.name, Path(folder).relative_to(p.path))
        for name in [*dirs, *files]:
            relative = (base / name).as_posix()
            if len(relative) > MAX_RELATIVE_PATH:
                errors.append(
                    f"{p.root.as_posix()}/{relative}: path is {len(relative)} characters relative to its root; "
                    f"the maximum is {MAX_RELATIVE_PATH}"
                )
                if name in dirs:
                    dirs.remove(name)
    return errors


def check(found: Discovery) -> tuple[list[str], list[str]]:
    """Return the errors and warnings of every rule ``jerry projects check`` enforces."""
    errors = list(found.errors)
    warnings = []
    for warning in found.warnings:
        (errors if _BAD_NAME in warning else warnings).append(warning)
    if not found.roots:
        errors.append("no projects root found")
    for root in found.roots:
        label = (root / REGISTRY).as_posix()
        try:
            if sync_registry(found, root):
                errors.append(f"{label}: registry is stale; run `jerry projects index --write`")
        except (OSError, ValueError) as exc:
            errors.append(f"{label}: {exc}")
    for p in found.all_projects:
        errors += _check_resume(found, p)
        if p.parent is None:
            errors += _check_paths(p)
    return errors, warnings
