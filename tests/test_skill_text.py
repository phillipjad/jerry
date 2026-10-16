# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Bans on the text the plugin ships to the model: skills, commands, .context and docs."""

import posixpath
import re
from collections.abc import Callable
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SHIPPED = ("skills", "commands", ".context", "docs")
SKIPPED_DIRS = {"__pycache__"}
DROPPED = (
    r"bootstrap|contract-design|diataxis|eng-team|pm-pmm|prompt-engineering|red-team|"
    r"saucer-boy|saucer-boy-framework-voice|test-spec|transcript|use-case|user-experience|ux-[a-z-]+"
)
DROPPED_REF = re.compile(
    rf"(?<![\w/.-])/(?:{DROPPED}|release)(?![\w-])|jerry:(?:{DROPPED})(?![\w-])|skills/(?:{DROPPED})/"
)
FENCE = re.compile(r"^\s*(`{3,}|~{3,})\s*([\w+-]*)")
SHELL_FENCES = {"bash", "sh", "shell", "console", "zsh"}
COMMANDS = {
    "uv", "ls", "cat", "grep", "mkdir", "test", "python", "python3", "jerry", "find", "head",
    "tail", "wc", "cp", "mv", "rm", "touch", "echo", "cd", "git", "sed", "awk", "diff", "rg",
}
SPAN = re.compile(r"(`+)(.+?)\1")
QUOTED = re.compile(r"\"(?:[^\"\\]|\\.)*\"|'[^']*'")
WORD = re.compile(r"[^\s|;&<>()`]+")
PLACEHOLDER = re.compile(r"\$\{[A-Za-z_]\w*\}|(?<!\{)\{[A-Za-z_][\w.-]*\}(?!\})")
PATH_NAME = re.compile(r"(?i)(path|dir|file|root)\}$")
EXTENSION = re.compile(r"\.\w+$")
BARE_REF = re.compile(r"(?<![\w.$/{}-])(?:(?:\.\./)+[\w.{}*/-]*|(?:\.context|docs)/[\w.{}*/-]*)")
LINK_TEXT = re.compile(r"\[[^\]]*\](?=\()")
ROOT_REF = re.compile(r"\$\{CLAUDE_PLUGIN_ROOT\}/([\w.{}*/<>-]*)")
ROW_OR_ITEM = re.compile(r"^\s*(?:\||[-*+]\s|\d+\.\s)")
WILDCARD = re.compile(r"[{}*?<>]|\.\.\.")
TRAILING = re.compile(r"[,:;]+$|(?<![./])\.+$")

Line = tuple[str, int, str, str]
Check = Callable[[str, str, str], bool]


def shipped() -> list[Path]:
    return sorted(
        p
        for top in SHIPPED
        for p in (ROOT / top).rglob("*")
        if p.is_file() and not SKIPPED_DIRS & set(p.parts)
    )


def contexts(rel: str, lines: list[str]) -> list[str]:
    """Return each line's context: yaml, code, frontmatter, prose, fence:<lang>, or delimiter."""
    if rel.endswith((".yaml", ".yml")):
        return ["yaml"] * len(lines)
    if not rel.endswith(".md"):
        return ["code"] * len(lines)
    out, fence, frontmatter = [], None, lines[:1] == ["---"]
    for i, line in enumerate(lines):
        if frontmatter:
            out.append("delimiter" if line == "---" else "frontmatter")
            frontmatter = i == 0 or line != "---"
            continue
        match, stripped = FENCE.match(line), line.strip()
        if fence is None and match:
            fence = (match.group(1), match.group(2).lower())
            out.append("delimiter")
        elif fence and stripped and set(stripped) == {fence[0][0]} and len(stripped) >= len(fence[0]):
            fence = None
            out.append("delimiter")
        else:
            out.append(f"fence:{fence[1]}" if fence else "prose")
    return out


def scan() -> list[Line]:
    rows = []
    for path in shipped():
        rel = path.relative_to(ROOT).as_posix()
        lines = path.read_text(encoding="utf-8").splitlines()
        rows += [(rel, n, ctx, line) for n, (ctx, line) in enumerate(zip(contexts(rel, lines), lines), 1)]
    return rows


SCAN = scan()


def offenders(check: Check) -> list[str]:
    return [f"{rel}:{n}" for rel, n, ctx, line in SCAN if check(rel, ctx, line)]


def literal(path: str) -> str:
    """Return ``path`` up to its first segment holding a placeholder or wildcard."""
    parts = []
    for part in path.split("/"):
        if WILDCARD.search(part):
            break
        parts.append(part)
    return "/".join(parts)


def plugin_path(rel: str, ref: str) -> str | None:
    """Return the existing plugin path a bare ``.context/``, ``docs/`` or ``../`` reference means."""
    path = TRAILING.sub("", ref)
    if path.startswith("../"):
        named = path.lstrip("./").split("/")[0]
        if not named or WILDCARD.search(named):
            return None
        path = posixpath.normpath(posixpath.join(posixpath.dirname(rel), path))
    top, lit = path.split("/", 1)[0], literal(path)
    if top not in (".context", "docs") or lit.rstrip("/") == "docs":
        return None
    return lit if (ROOT / lit).exists() else None


def bare_plugin_refs(rel: str, line: str) -> list[str]:
    texts = [m.span() for m in LINK_TEXT.finditer(line)]
    return [
        m.group(0)
        for m in BARE_REF.finditer(line)
        if not any(start <= m.start() < end for start, end in texts) and plugin_path(rel, m.group(0))
    ]


def shell_commands(ctx: str, line: str) -> list[str]:
    if ctx.removeprefix("fence:") in SHELL_FENCES:
        return [] if line.lstrip().startswith("#") else [line]
    if ctx != "prose" and not ctx.startswith("fence:"):
        return []
    found = [m.group(2) for m in SPAN.finditer(line)] + ([line] if ctx.startswith("fence:") else [])
    return [c for c in found if c.split() and c.split()[0] in COMMANDS]


def is_path_argument(word: str) -> bool:
    found = PLACEHOLDER.findall(word)
    return bool(found) and ("/" in word or bool(EXTENSION.search(word)) or any(PATH_NAME.search(p) for p in found))


def unquoted_path_arguments(command: str) -> list[str]:
    bare = QUOTED.sub(lambda m: " " * len(m.group(0)), command)
    return [w for w in WORD.findall(bare) if is_path_argument(w)]


def uses_directory_flag(_rel: str, _ctx: str, line: str) -> bool:
    return "--directory" in line


def uses_jerry_project_path(_rel: str, _ctx: str, line: str) -> bool:
    return bool(re.search(r"projects/\$\{?JERRY_PROJECT", line))


def uses_dead_cli(_rel: str, _ctx: str, line: str) -> bool:
    return "scripts/cli.py" in line


def has_reinject_marker(_rel: str, _ctx: str, line: str) -> bool:
    return bool(re.search(r"<!--\s*L2-REINJECT", line))


def has_bare_plugin_path(rel: str, _ctx: str, line: str) -> bool:
    return bool(bare_plugin_refs(rel, line))


def has_unquoted_path_placeholder(_rel: str, ctx: str, line: str) -> bool:
    return any(unquoted_path_arguments(c) for c in shell_commands(ctx, line))


def names_dropped_skill(_rel: str, _ctx: str, line: str) -> bool:
    return bool(ROW_OR_ITEM.match(line) and DROPPED_REF.search(line))


def test_should_scan_the_shipped_text() -> None:
    files = {rel for rel, *_ in SCAN}

    assert "skills/problem-solving/SKILL.md" in files
    assert ".context/rules/quality-enforcement.md" in files
    assert any(rel.startswith(("commands/", "docs/")) for rel in files)


def test_should_not_use_the_uv_directory_flag() -> None:
    assert offenders(uses_directory_flag) == []


def test_should_not_build_paths_from_jerry_project() -> None:
    assert offenders(uses_jerry_project_path) == []


def test_should_not_call_the_removed_cli_script() -> None:
    assert offenders(uses_dead_cli) == []


def test_should_not_carry_reinject_markers() -> None:
    assert offenders(has_reinject_marker) == []


def test_should_root_plugin_paths_at_the_plugin_root() -> None:
    assert offenders(has_bare_plugin_path) == []


def test_should_quote_path_placeholders_in_shell_commands() -> None:
    assert offenders(has_unquoted_path_placeholder) == []


def test_should_resolve_every_plugin_root_reference() -> None:
    refs = [
        (f"{rel}:{n}", TRAILING.sub("", m.group(1)))
        for rel, n, _, line in SCAN
        for m in ROOT_REF.finditer(line)
    ]

    assert refs
    assert [f"{where} {path}" for where, path in refs if not (ROOT / literal(path)).exists()] == []


def test_should_not_route_to_dropped_skills() -> None:
    assert offenders(names_dropped_skill) == []


@pytest.mark.parametrize(
    ("check", "rel", "ctx", "bad", "good"),
    [
        (uses_directory_flag, "x.md", "prose", "uv run --directory x", 'uv run --project "x"'),
        (uses_jerry_project_path, "x.md", "prose", "projects/${JERRY_PROJECT}/a", "{project_dir}/a"),
        (uses_dead_cli, "x.md", "prose", "python3 scripts/cli.py view", "jerry ast parse"),
        (has_reinject_marker, "x.md", "prose", '<!-- L2-REINJECT: rank=1, content="x" -->', "<!-- note -->"),
        (has_bare_plugin_path, "x.md", "prose", "see `.context/rules/`", "see `${CLAUDE_PLUGIN_ROOT}/.context/rules/`"),
        (has_bare_plugin_path, "s/a/B.md", "prose", "[c](../../docs/governance/)", "[docs/x](https://x/docs/)"),
        (has_bare_plugin_path, "x.md", "prose", "docs/schemas/session_context.json", "docs/{type}/x.md docs/research/"),
        (has_bare_plugin_path, ".context/templates/a/B.md", "prose", "[r](../../rules/)", "[e](../{{ID}}/e.md)"),
        (has_bare_plugin_path, ".context/templates/a/B.md", "prose", "[r](../../rules/)", "[t](../..)"),
        (has_unquoted_path_placeholder, "x.md", "fence:bash", "ls {project_dir}/a/*.md", 'ls "{project_dir}"/a/*.md'),
        (has_unquoted_path_placeholder, "x.md", "prose", "`uv run --project ${CLAUDE_PLUGIN_ROOT}`", "`uv x {t}`"),
        (has_unquoted_path_placeholder, "x.md", "fence:", "cp {a}.md b", "# ls {a}/b"),
        (names_dropped_skill, "x.md", "prose", "| Security | `/eng-team` | x |", "Use `/eng-team` instead."),
        (names_dropped_skill, "x.md", "prose", "- `/release` cuts a tag", "- `/adversary` reviews"),
    ],
    ids=[
        "directory", "jerry-project", "cli", "reinject", "bare", "relative", "docs-scope", "template-link", "dir-link",
        "fence", "inline", "plain-fence", "row", "item",
    ],
)
def test_should_flag_only_the_banned_form(check: Check, rel: str, ctx: str, bad: str, good: str) -> None:
    assert check(rel, ctx, bad)
    assert not check(rel, ctx, good)


def test_should_track_frontmatter_and_fences() -> None:
    lines = ["---", "name: x", "---", "text", "````markdown", "```bash", "```", "````", "after"]

    assert contexts("a.md", lines) == [
        "delimiter", "frontmatter", "delimiter", "prose", "delimiter", "fence:markdown", "fence:markdown",
        "delimiter", "prose",
    ]
