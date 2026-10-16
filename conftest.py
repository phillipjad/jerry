# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
from pathlib import Path

import pytest


def make_project(parent: Path, folder: str, **fields: object) -> Path:
    path = parent / folder
    path.mkdir(parents=True)
    fields.setdefault("title", folder)
    fields.setdefault("status", "active")
    fields.setdefault("summary", f"Summary of {folder}.")
    toml = "".join(f"{key} = {json.dumps(value)}\n" for key, value in fields.items())
    (path / "project.toml").write_text(toml, encoding="utf-8")
    return path


@pytest.fixture
def home(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    home = tmp_path / "home"
    home.mkdir()
    monkeypatch.setenv("HOME", str(home))
    monkeypatch.setenv("USERPROFILE", str(home))
    monkeypatch.delenv("CLAUDE_CODE_SESSION_ID", raising=False)
    return home
