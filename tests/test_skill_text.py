# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Bans on the text the plugin ships to the model (skills, commands, .context, docs) and on CLAUDE.md."""

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
    rf"(?<![\w/.-])/(?:{DROPPED}|release)(?![\w-])|jerry:(?:{DROPPED})(?![\w-])|skills/(?:{DROPPED})/|`(?:{DROPPED})`"
)
CLI = {
    "ast": {"parse", "frontmatter", "validate", "modify"},
    "projects": {"list", "show", "new", "index", "check"},
    "focus": {"show", "set", "add", "none"},
}
JERRY_CALL = re.compile(r"(?<![\w/.-])jerry\s+([a-z][\w-]*)(?:\s+([a-z][\w-]*))?")
UNROOTED_RUN = re.compile(r'\buv run (?!--project "\$\{CLAUDE_PLUGIN_ROOT\}" jerry\b)(?:[^\s`|;&]+ )*?jerry\b')
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
PLUGIN_REF = re.compile(r"(?<![\w.$/{}-])(?:(?:\.\./)+|\.context/|skills/)[\w.{}*/-]*")
REMOVED_REF = re.compile(r"(?<![\w.$/{}-])(?:scripts/\w+\.py|docs/(?:standards|governance/proposals)/)")
PROJECT_OUTPUT = re.compile(
    r"projects/[{$]|(?<![\w.$/{}-])docs/"
    r"(?:research|analysis|decisions|synthesis|reviews|investigations|reports|critiques|\{type\})/"
)
DELETED_REF = re.compile(r"\.governance\.yaml|/composition/|\.agent\.yaml|agent-(?:governance|canonical)-v1")
REMOVED_WORD = re.compile(r"project-workflow|add-entry|set-entry-type|assess-severity")
REINJECTION = re.compile(r"(?i)re-?inject|per-prompt|every prompt|L2 (?:marker|engine)|L2-protected")
UNSHIPPED = re.compile(
    r"(?i)PreToolUse|before tool calls|\bCI (?:gate|check)s?\b|L5 (?:gate|CI)|gate script|check_hard_rule_ceiling|"
    r"GitHub Actions|CI failure|L3 AST gate|Structural L2"
)
FILE_REF = re.compile(r"`([^`\s]+)`|\]\(([^)\s]+)\)")
FILE_PATH = re.compile(r"[\w.-]+(?:/[\w.-]+)+\.(?:md|ya?ml|json)")
USER_PATHS = ("docs/design/",)
WILDCARD = re.compile(r"[{}*?<>]|\.\.\.")
TRAILING = re.compile(r"[,:;]+$|(?<![./])\.+$")

Line = tuple[str, int, str, str]


def deleted_rules() -> list[str]:
    """Return the names of upstream ``.context/rules/*.md`` files this repository no longer ships."""
    lines = (ROOT / "upstream-manifest.txt").read_text(encoding="utf-8").splitlines()
    paths = [line.split("  ", 1)[1] for line in lines]
    return sorted(
        posixpath.basename(path)[:-3]
        for path in paths
        if posixpath.dirname(path) == ".context/rules" and path.endswith(".md") and not (ROOT / path).exists()
    )


DELETED_RULES = deleted_rules()
DELETED_RULE = re.compile(rf"(?<![\w-])(?:{'|'.join(map(re.escape, DELETED_RULES))})(?:\.md)?(?![\w-])")
Check = Callable[[str, str, str], bool]


def shipped() -> list[Path]:
    return sorted(
        [ROOT / "CLAUDE.md"]
        + [p for top in SHIPPED for p in (ROOT / top).rglob("*") if p.is_file() and not SKIPPED_DIRS & set(p.parts)]
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


def resolve(rel: str, ref: str) -> str | None:
    """Return the root-relative path ``ref`` means in file ``rel``, or None for a ``../`` into a placeholder."""
    path = TRAILING.sub("", ref)
    if not path.startswith("../"):
        return path
    named = path.lstrip("./").split("/")[0]
    if not named or WILDCARD.search(named):
        return None
    return posixpath.normpath(posixpath.join(posixpath.dirname(rel), path))


def plugin_path(rel: str, ref: str) -> str | None:
    """Return the existing plugin path a bare ``.context/``, ``docs/`` or ``../`` reference means."""
    path = resolve(rel, ref)
    if path is None:
        return None
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


def names_jerry_project(_rel: str, _ctx: str, line: str) -> bool:
    return "JERRY_PROJECT" in line


def claims_reinjection(_rel: str, _ctx: str, line: str) -> bool:
    return bool(REINJECTION.search(line))


def names_removed_word(_rel: str, _ctx: str, line: str) -> bool:
    return bool(REMOVED_WORD.search(line))


def names_deleted_rule_file(_rel: str, _ctx: str, line: str) -> bool:
    return bool(DELETED_RULE.search(line))


def claims_unshipped_enforcement(_rel: str, _ctx: str, line: str) -> bool:
    return bool(UNSHIPPED.search(line))


def has_unresolved_file_path(rel: str, _ctx: str, line: str) -> bool:
    """Flag a backticked or linked relative file path that exists neither at the plugin root nor beside ``rel``."""
    paths = [(m.group(1) or m.group(2)).split("#")[0] for m in FILE_REF.finditer(line)]
    return any(
        FILE_PATH.fullmatch(path)
        and "..." not in path
        and not path.startswith(USER_PATHS)
        and not (ROOT / path).exists()
        and not (ROOT / posixpath.dirname(rel) / path).exists()
        for path in paths
    )


def names_link_artifact(_rel: str, _ctx: str, line: str) -> bool:
    return "link-artifact" in line


def runs_unrooted_jerry(_rel: str, _ctx: str, line: str) -> bool:
    return bool(UNROOTED_RUN.search(line))


def calls_unknown_jerry_command(_rel: str, ctx: str, line: str) -> bool:
    calls = [m.groups() for c in shell_commands(ctx, line) for m in JERRY_CALL.finditer(c)]
    return any(ns not in CLI or (command and command not in CLI[ns]) for ns, command in calls)


def names_removed_path(_rel: str, _ctx: str, line: str) -> bool:
    return bool(REMOVED_REF.search(line))


def has_dead_plugin_path(rel: str, _ctx: str, line: str) -> bool:
    paths = [resolve(rel, m.group(0)) for m in PLUGIN_REF.finditer(line)]
    return any(path is not None and not (ROOT / literal(path)).exists() for path in paths)


def misplaces_project_output(_rel: str, _ctx: str, line: str) -> bool:
    return bool(PROJECT_OUTPUT.search(line))


def names_deleted_agent_file(_rel: str, _ctx: str, line: str) -> bool:
    return bool(DELETED_REF.search(line))


def has_bare_plugin_path(rel: str, _ctx: str, line: str) -> bool:
    return bool(bare_plugin_refs(rel, line))


def has_unquoted_path_placeholder(_rel: str, ctx: str, line: str) -> bool:
    return any(unquoted_path_arguments(c) for c in shell_commands(ctx, line))


def names_dropped_skill(_rel: str, _ctx: str, line: str) -> bool:
    return bool(DROPPED_REF.search(line))


def test_should_scan_the_shipped_text() -> None:
    files = {rel for rel, *_ in SCAN}

    assert "skills/problem-solving/SKILL.md" in files
    assert ".context/rules/quality-enforcement.md" in files
    assert any(rel.startswith(("commands/", "docs/")) for rel in files)
    assert "CLAUDE.md" in files


def test_should_not_use_the_uv_directory_flag() -> None:
    assert offenders(uses_directory_flag) == []


def test_should_not_mention_jerry_project() -> None:
    assert offenders(names_jerry_project) == []


def test_should_not_claim_per_prompt_reinjection() -> None:
    assert offenders(claims_reinjection) == []


def test_should_not_name_removed_upstream_commands_or_rules() -> None:
    assert offenders(names_removed_word) == []


def test_should_not_name_deleted_rule_files() -> None:
    assert {"coding-standards", "project-workflow"} <= set(DELETED_RULES)
    assert offenders(names_deleted_rule_file) == []


def test_should_claim_only_enforcement_the_plugin_ships() -> None:
    assert offenders(claims_unshipped_enforcement) == []


def test_should_resolve_every_relative_file_path() -> None:
    assert offenders(has_unresolved_file_path) == []


def test_should_not_mention_link_artifact() -> None:
    assert offenders(names_link_artifact) == []


def test_should_run_the_jerry_cli_from_the_plugin_project() -> None:
    assert offenders(runs_unrooted_jerry) == []


def test_should_call_only_real_jerry_commands() -> None:
    assert offenders(calls_unknown_jerry_command) == []


def test_should_not_reference_removed_upstream_paths() -> None:
    assert offenders(names_removed_path) == []


def test_should_resolve_every_relative_plugin_path() -> None:
    assert offenders(has_dead_plugin_path) == []


def test_should_put_project_files_under_project_dir() -> None:
    assert offenders(misplaces_project_output) == []


def test_should_not_reference_deleted_agent_files() -> None:
    assert offenders(names_deleted_agent_file) == []


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
        (names_jerry_project, "x.md", "prose", "export JERRY_PROJECT=PROJ-001", "{project_dir}/a"),
        (claims_reinjection, "x.md", "prose", '<!-- L2-REINJECT: rank=1 -->', "L2: architect view"),
        (claims_reinjection, "x.md", "prose", "| L2 | Every prompt | Re-inject rules |", "per prompt engineering"),
        (names_removed_word, "x.md", "prose", "| H-32 | x | project-workflow |", "workflow of the project"),
        (names_removed_word, "x.md", "prose", "`add-entry {PS_ID}` `set-entry-type`", "entry type"),
        (names_deleted_rule_file, "x.md", "prose", "| H-11 | coding-standards |", "| H-07 | architecture-standards |"),
        (names_deleted_rule_file, "x.md", "prose", "`testing-standards.md`", "coding standards"),
        (claims_unshipped_enforcement, "x.md", "prose", "| L3 | Before tool calls |", "Pre-Commit Quality Gate"),
        (claims_unshipped_enforcement, "x.md", "prose", "the L5 CI gate script", "| L5 | Execution | Task |"),
        (has_unresolved_file_path, "s/a/b/c.md", "prose", "from: `templates/research.md`", "`docs/design/a.md`"),
        (has_unresolved_file_path, "skills/ast/SKILL.md", "prose", "[x](agents/none.md)", "[x](SKILL.md) `x/.../y.md`"),
        (has_unresolved_file_path, "x.md", "prose", "`.claude/T.md`", '`"{project_dir}"/a.md` `skills/ast/SKILL.md`'),
        (names_link_artifact, "x.md", "prose", "<must>Call link-artifact</must>", "persisted to {project_dir}"),
        (runs_unrooted_jerry, "x.md", "fence:sh", "uv run jerry ast", 'uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry'),
        (runs_unrooted_jerry, "x.md", "prose", "`uv run --project . jerry`", "`uv run --group test pytest`"),
        (calls_unknown_jerry_command, "x.md", "fence:bash", "jerry ast reinject a.md", "jerry ast validate a.md --nav"),
        (calls_unknown_jerry_command, "x.md", "prose", "`jerry items list`", "`jerry focus set <id>`, jerry repo work"),
        (names_removed_path, "x.md", "prose", "python3 scripts/cli.py view", "skills/ast/scripts/x.py"),
        (names_removed_path, "x.md", "prose", "docs/standards/a docs/governance/proposals/", "docs/governance/a"),
        (has_dead_plugin_path, ".context/templates/a/B.md", "prose", "[d](../decisions/x.md)", "[e](../{{ID}}/e.md)"),
        (has_dead_plugin_path, "x.md", "prose", "`.context/patterns/` `skills/x/a.md`", "`skills/{name}/SKILL.md`"),
        (misplaces_project_output, "x.md", "prose", "`projects/{project_id}/qa/`", "`{project_dir}/qa/`"),
        (misplaces_project_output, "x.md", "prose", "Create file at: docs/research/a.md", "docs/design/a.md"),
        (names_deleted_agent_file, "x.md", "prose", "see adv-executor.governance.yaml", "composition root"),
        (has_bare_plugin_path, "x.md", "prose", "see `.context/rules/`", "see `${CLAUDE_PLUGIN_ROOT}/.context/rules/`"),
        (has_bare_plugin_path, "s/a/B.md", "prose", "[c](../../docs/governance/)", "[docs/x](https://x/docs/)"),
        (has_bare_plugin_path, "x.md", "prose", "docs/schemas/session_context.json", "docs/{type}/x.md docs/research/"),
        (has_bare_plugin_path, ".context/templates/a/B.md", "prose", "[r](../../rules/)", "[e](../{{ID}}/e.md)"),
        (has_bare_plugin_path, ".context/templates/a/B.md", "prose", "[r](../../rules/)", "[t](../..)"),
        (has_unquoted_path_placeholder, "x.md", "fence:bash", "ls {project_dir}/a/*.md", 'ls "{project_dir}"/a/*.md'),
        (has_unquoted_path_placeholder, "x.md", "prose", "`uv run --project ${CLAUDE_PLUGIN_ROOT}`", "`uv x {t}`"),
        (has_unquoted_path_placeholder, "x.md", "fence:", "cp {a}.md b", "# ls {a}/b"),
        (names_dropped_skill, "x.md", "prose", "| Security | `/eng-team` | x |", "Use the transcript."),
        (names_dropped_skill, "x.md", "prose", "- `/release` cuts a tag", "- `/adversary` reviews"),
        (names_dropped_skill, "x.md", "prose", "Use `transcript` or jerry:diataxis.", "Run bootstrap.py first."),
    ],
    ids=[
        "directory", "jerry-project", "reinject", "reinjection", "rule-file", "ps-cli", "deleted-rule-row",
        "deleted-rule-name", "pre-tool", "ci-gate", "template", "link",
        "plugin-root", "link-artifact", "uv-fence", "uv-span", "ast-command", "namespace",
        "scripts", "docs", "dead-relative", "dead-plugin", "project-id", "docs-output", "deleted", "bare", "relative",
        "docs-scope", "template-link", "dir-link", "fence", "inline", "plain-fence", "row", "item", "backticked",
    ],
)
def test_should_flag_only_the_banned_form(check: Check, rel: str, ctx: str, bad: str, good: str) -> None:
    assert check(rel, ctx, bad)
    assert not check(rel, ctx, good)


def rule_section(heading: str) -> str:
    text = (ROOT / ".context" / "rules" / "quality-enforcement.md").read_text(encoding="utf-8")
    return text.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]


def test_should_index_h22_as_a_hard_rule_and_not_retire_it() -> None:
    assert "\n| H-22 |" in rule_section("HARD Rule Index")
    assert "\n| H-22 |" not in rule_section("Retired Rule IDs")


def test_should_track_frontmatter_and_fences() -> None:
    lines = ["---", "name: x", "---", "text", "````markdown", "```bash", "```", "````", "after"]

    assert contexts("a.md", lines) == [
        "delimiter", "frontmatter", "delimiter", "prose", "delimiter", "fence:markdown", "fence:markdown",
        "delimiter", "prose",
    ]
