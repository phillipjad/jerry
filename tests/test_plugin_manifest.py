# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import os
import re
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text(encoding="utf-8"))
HOOKS = json.loads((ROOT / "hooks" / "hooks.json").read_text(encoding="utf-8"))["hooks"]
PLUGIN_ROOT = "${CLAUDE_PLUGIN_ROOT}"
SKIPPED_DIRS = {".git", ".venv", "__pycache__", ".pytest_cache", ".ruff_cache"}
FILE_CAP = 5000
FRONTMATTER = re.compile(r"---\r?\n(.*?)\r?\n---\r?\n", re.DOTALL)


def frontmatter(path: Path) -> dict[str, str]:
    match = FRONTMATTER.match(path.read_text(encoding="utf-8-sig"))
    assert match, f"{path.relative_to(ROOT)} has no frontmatter"
    fields = {}
    for line in match.group(1).splitlines():
        key, sep, value = line.partition(":")
        if sep and not line[:1].isspace() and not line.startswith("-"):
            fields[key.strip()] = value.strip()
    return fields


def is_single_line(value: str) -> bool:
    if not value or value[0] in "|>":
        return False
    if value[0] in "\"'":
        return len(value) > 1 and value[-1] == value[0] and not value.endswith("\\" + value[0])
    return True


def skill_files() -> list[Path]:
    return sorted((ROOT / "skills").glob("*/SKILL.md"))


def agent_files() -> list[Path]:
    return sorted((ROOT / "skills").glob("*/agents/*.md"))


def test_should_find_every_agent_listed_in_manifest() -> None:
    missing = [a for a in MANIFEST["agents"] if not (ROOT / a).is_file()]

    assert missing == []


def test_should_list_every_agent_file_in_manifest() -> None:
    listed = {(ROOT / a).resolve() for a in MANIFEST["agents"]}

    orphans = [p.relative_to(ROOT).as_posix() for p in agent_files() if p.resolve() not in listed]

    assert orphans == []


def test_should_find_every_command_listed_in_manifest() -> None:
    missing = [c for c in MANIFEST["commands"] if not (ROOT / c).is_file()]

    assert missing == []


def test_should_give_every_command_a_single_line_description() -> None:
    bad = [c for c in MANIFEST["commands"] if not is_single_line(frontmatter(ROOT / c).get("description", ""))]

    assert bad == []


def test_should_keep_developer_context_out_of_the_plugin_root() -> None:
    assert not (ROOT / "CLAUDE.md").exists(), "Claude Code does not load CLAUDE.md from a plugin root"
    assert (ROOT / ".claude" / "CLAUDE.md").is_file()


def test_should_give_every_skill_a_single_line_name_and_description() -> None:
    bad = [
        f"{p.relative_to(ROOT).as_posix()}: {key}"
        for p in skill_files()
        for key in ("name", "description")
        if not is_single_line(frontmatter(p).get(key, ""))
    ]

    assert bad == []


def test_should_say_when_to_use_each_skill_within_1024_characters() -> None:
    descriptions = {p.parent.name: frontmatter(p)["description"].strip("\"'") for p in skill_files()}

    bad = [name for name, text in descriptions.items() if "Use when" not in text or len(text) > 1024]

    assert descriptions
    assert bad == []


def test_should_give_skills_unique_names() -> None:
    names = [frontmatter(p)["name"] for p in skill_files()]

    assert len(names) == len(set(names))


def test_should_give_agents_unique_names() -> None:
    names = [frontmatter(p)["name"] for p in agent_files()]

    assert len(names) == len(set(names))


def test_should_register_only_the_session_start_and_subagent_start_hooks() -> None:
    assert set(HOOKS) == {"SessionStart", "SubagentStart"}


@pytest.mark.parametrize(("event", "name"), [("SessionStart", "session-start"), ("SubagentStart", "subagent-start")])
def test_should_run_each_hook_through_uv_in_exec_form(event: str, name: str) -> None:
    args = ["run", "--no-project", "--python", ">=3.11", f"{PLUGIN_ROOT}/hooks/run.py", name]

    assert HOOKS[event] == [{"hooks": [{"type": "command", "command": "uv", "args": args, "timeout": 20}]}]


def test_should_find_every_plugin_file_a_hook_references() -> None:
    files = [
        arg.removeprefix(f"{PLUGIN_ROOT}/")
        for groups in HOOKS.values()
        for group in groups
        for hook in group["hooks"]
        for arg in hook["args"]
        if arg.startswith(f"{PLUGIN_ROOT}/")
    ]

    assert files
    assert [path for path in files if not (ROOT / path).is_file()] == []


def test_should_stay_under_marketplace_file_cap() -> None:
    count = 0
    for _, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in SKIPPED_DIRS]
        count += len(files)

    assert count < FILE_CAP


def test_should_ship_no_top_level_bin() -> None:
    assert not (ROOT / "bin").exists()


def test_should_reject_multi_line_values() -> None:
    assert not is_single_line('"starts here,')
    assert not is_single_line("|")
    assert not is_single_line('"ends with an escaped quote\\"')
    assert is_single_line('"quoted"')
    assert is_single_line("plain words")
