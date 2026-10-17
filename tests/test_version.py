# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import re
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE = re.compile(r"^## \[(\d+\.\d+\.\d+)\]", re.MULTILINE)


def test_should_give_plugin_package_and_changelog_one_version() -> None:
    plugin = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))["version"]
    package = tomllib.loads((ROOT / "pyproject.toml").read_text(encoding="utf-8"))["project"]["version"]
    release = RELEASE.search((ROOT / "CHANGELOG.md").read_text(encoding="utf-8"))

    assert release, "CHANGELOG.md has no released version heading"
    assert (plugin, package) == (release.group(1), release.group(1))
