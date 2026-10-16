# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import hashlib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MARK = "Modified from geekatron/jerry v0.31.9; see NOTICE."
UPSTREAM_NOTICE = "Jerry Framework\nCopyright 2026 Adam Nowak\n"
COMMENTLESS = {".json"}
LISTED = re.compile(r"^- `([^`]+)`$", re.MULTILINE)


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


def listed_as_modified() -> set[str]:
    text = (ROOT / "UPSTREAM.md").read_text(encoding="utf-8")
    section = text.split("## Modified files without comment syntax", 1)
    return set(LISTED.findall(section[1])) if len(section) == 2 else set()


def test_should_keep_license_verbatim() -> None:
    assert blob_sha((ROOT / "LICENSE").read_bytes()) == manifest()["LICENSE"]


def test_should_keep_upstream_attribution_in_notice() -> None:
    assert UPSTREAM_NOTICE in (ROOT / "NOTICE").read_text(encoding="utf-8")


def test_should_mark_every_modified_upstream_file() -> None:
    listed = listed_as_modified()

    unmarked = [
        path
        for path in modified()
        if (path not in listed if Path(path).suffix in COMMENTLESS else MARK not in (ROOT / path).read_text(encoding="utf-8"))
    ]

    assert unmarked == []


def test_should_list_only_modified_files_as_modified() -> None:
    assert listed_as_modified() <= set(modified())


def test_should_hash_like_git() -> None:
    assert blob_sha(b"") == "e69de29bb2d1d6434b8b29ae775ad8c2e48c5391"
