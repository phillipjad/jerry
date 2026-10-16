# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "Modified from geekatron/jerry v0.31.9; see NOTICE."
UPSTREAM_NOTICE = "Jerry Framework\nCopyright 2026 Adam Nowak\n"
COMMENTLESS = {".json", ".lock"}
LISTED = re.compile(r"^- `([^`]+)`$", re.MULTILINE)
MOVED = re.compile(r"^- `([^`]+)` -> `([^`]+)`$", re.MULTILINE)


def blob_sha(data: bytes) -> str:
    return hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()


def manifest() -> dict[str, str]:
    lines = (ROOT / "upstream-manifest.txt").read_text(encoding="utf-8").splitlines()
    return {path: sha for sha, path in (line.split("  ", 1) for line in lines)}


def modified() -> list[str]:
    return [
        path
        for path, sha in sorted(manifest().items())
        if (ROOT / path).is_file() and blob_sha((ROOT / path).read_bytes()) != sha
    ]


def upstream_section(heading: str) -> str:
    text = (ROOT / "UPSTREAM.md").read_text(encoding="utf-8")
    parts = text.split(f"## {heading}", 1)
    return parts[1].split("\n## ", 1)[0] if len(parts) == 2 else ""


def listed_as_modified() -> set[str]:
    return set(LISTED.findall(upstream_section("Modified files without comment syntax")))


def moved() -> dict[str, str]:
    return dict(MOVED.findall(upstream_section("Moved files")))


def is_marked(path: str) -> bool:
    if Path(path).suffix in COMMENTLESS:
        return path in listed_as_modified()
    return MARK in (ROOT / path).read_text(encoding="utf-8")


def test_should_keep_license_verbatim() -> None:
    assert blob_sha((ROOT / "LICENSE").read_bytes()) == manifest()["LICENSE"]


def test_should_keep_upstream_attribution_in_notice() -> None:
    assert UPSTREAM_NOTICE in (ROOT / "NOTICE").read_text(encoding="utf-8")


def test_should_mark_every_modified_upstream_file() -> None:
    assert [path for path in modified() if not is_marked(path)] == []


def test_should_list_only_modified_files_as_modified() -> None:
    assert listed_as_modified() <= set(modified())


def test_should_move_only_upstream_files_to_new_paths() -> None:
    upstream = manifest()

    bad = [
        f"{old} -> {new}"
        for old, new in moved().items()
        if old not in upstream or (ROOT / old).exists() or not (ROOT / new).is_file()
    ]

    assert bad == []


def test_should_mark_every_moved_file_that_changed() -> None:
    upstream = manifest()

    unmarked = [
        new
        for old, new in moved().items()
        if blob_sha((ROOT / new).read_bytes()) != upstream[old] and not is_marked(new)
    ]

    assert unmarked == []


def test_should_hash_like_git() -> None:
    assert blob_sha(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
