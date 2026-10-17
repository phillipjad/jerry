# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest
from conftest import make_project

from jerry import cli, hooks, projects, session

ROOT = Path(__file__).resolve().parents[1]
RUN = ROOT / "hooks" / "run.py"
SID = "goku"
CLI = f'uv run --project "{ROOT.as_posix()}" jerry'
LITERAL = "A literal ${CLAUDE_PLUGIN_ROOT} in a Jerry file opened with Read, or in a Bash command, means this path."
SKILLS = (
    "Jerry skills (H-22): when a request matches a Jerry skill's description, invoke that skill (jerry:<name>) "
    "proactively and early, without waiting for the user to name it; combine skills when the work spans several."
)
HEAD = f"Jerry plugin root: {ROOT.as_posix()}. {LITERAL}\nJerry CLI: {CLI} <command> --session {SID}\n{SKILLS}\n"
PICK_UP = "## Pick up here\n\n1. Find the seventh Dragon Ball."
ASK = "ask them to pick one of the projects below"
BUDGET = 9000
DAY = 86400
TAIL = "Use the project the task names, else the primary; never run focus commands."


@pytest.fixture
def start(tmp_path: Path, home: Path) -> Path:
    start = tmp_path / "start"
    kame = make_project(start / "projects", "PROJ-001-kame-house", title="Kame House")
    resume = f"# PROJ-001 -- Resume\n\n{PICK_UP}\n\n## History\n\nOld notes.\n"
    (kame / "RESUME.md").write_text(resume, encoding="utf-8")
    make_project(start / "projects", "PROJ-002-capsule-corp", title="Capsule Corp", status="paused")
    return start


def context(result: dict | None, event: str = "SessionStart") -> str:
    assert result is not None
    assert result["hookSpecificOutput"]["hookEventName"] == event
    return result["hookSpecificOutput"]["additionalContext"]


def session_start(cwd: Path, source: str = "startup", sid: str = SID) -> str:
    payload = {"session_id": sid, "cwd": str(cwd), "hook_event_name": "SessionStart", "source": source}
    return context(hooks.session_start(payload))


def subagent_start(sid: str = SID) -> dict | None:
    payload = {"session_id": sid, "cwd": "/elsewhere", "hook_event_name": "SubagentStart", "agent_id": "a1"}
    return hooks.subagent_start(payload)


def focus(*args: str) -> int:
    return cli.main(["focus", *args, "--session", SID])


def session_file(home: Path, sid: str = SID) -> Path:
    return home / ".jerry" / "sessions" / f"{sid}.json"


def save_focus(sid: str, focus: list[tuple[str, str]], cwd: str = "/start", none: bool = False, age: float = 0) -> None:
    entries = [{"id": project_id, "path": path} for project_id, path in focus]
    session.save(sid, session.Session(cwd=cwd, roots=[], none=none, focus=entries))
    stamp = time.time() - age
    os.utime(session.session_path(sid), (stamp, stamp))


def run_hook(event: str, stdin: bytes, home: Path) -> subprocess.CompletedProcess[bytes]:
    env = {key: value for key, value in os.environ.items() if key != "PYTHONUTF8"}
    env.update(HOME=str(home), USERPROFILE=str(home))
    return subprocess.run(
        [sys.executable, "-I", "-S", str(RUN), event], input=stdin, capture_output=True, env=env, timeout=60
    )


def test_should_write_ascii_json_from_a_bare_interpreter_in_a_non_cp1252_directory(tmp_path: Path, home: Path) -> None:
    cwd = tmp_path / "カメハウス"
    make_project(cwd / "projects", "PROJ-001-kame-house", title="亀仙人の家")
    stdin = json.dumps({"session_id": SID, "cwd": str(cwd), "source": "startup"}, ensure_ascii=False)

    result = run_hook("session-start", stdin.encode("utf-8"), home)

    assert result.returncode == 0, result.stderr
    assert result.stderr == b""
    assert result.stdout.isascii()
    text = context(json.loads(result.stdout))
    assert "- PROJ-001 [active] 亀仙人の家: Summary of PROJ-001-kame-house." in text.splitlines()
    assert json.loads(session_file(home).read_text(encoding="utf-8"))["cwd"] == cwd.as_posix()


def test_should_answer_subagent_start_through_the_runner(start: Path, home: Path) -> None:
    session_start(start)
    focus("set", "PROJ-001")

    focused = run_hook("subagent-start", json.dumps({"session_id": SID}).encode("ascii"), home)
    other = run_hook("subagent-start", json.dumps({"session_id": "vegeta"}).encode("ascii"), home)

    assert focused.returncode == 0
    assert focused.stdout.isascii()
    kame = (start / "projects" / "PROJ-001-kame-house").resolve().as_posix()
    assert f"{{project_dir}} = {kame}" in context(json.loads(focused.stdout), "SubagentStart")
    assert (other.returncode, other.stdout, other.stderr) == (0, b"", b"")


@pytest.mark.parametrize(
    ("event", "stdin", "reason"),
    [
        ("session-start", b"not json", "Expecting value"),
        ("session-start", b"\xff\xfe{}", "can't decode byte 0xff"),
        ("session-start", b"[]", "hook input has no session_id"),
        ("session-start", b'{"cwd": "/start"}', "hook input has no session_id"),
        ("session-start", b'{"session_id": "../escape", "cwd": "/start"}', "invalid session id"),
        ("session-start", b'{"session_id": "goku"}', "hook input has no cwd"),
        ("subagent-start", b'{"session_id": "a/b"}', "invalid session id"),
        ("session-end", b'{"session_id": "goku"}', "unknown event"),
    ],
)
def test_should_print_one_plain_line_and_exit_0_on_bad_input(home: Path, event: str, stdin: bytes, reason: str) -> None:
    result = run_hook(event, stdin, home)

    assert result.returncode == 0
    assert result.stdout.isascii()
    lines = result.stdout.decode("ascii").splitlines()
    assert len(lines) == 1
    assert lines[0].startswith(f"Jerry {event} hook: ")
    assert reason in lines[0]
    assert not (home / ".jerry").exists()


@pytest.mark.parametrize("event", ["session-start", "subagent-start"])
def test_should_report_a_corrupt_session_file_in_one_line_and_leave_it(home: Path, event: str) -> None:
    file = session_file(home)
    file.parent.mkdir(parents=True)
    file.write_bytes(b"{not json")

    result = run_hook(event, json.dumps({"session_id": SID, "cwd": str(home)}).encode("ascii"), home)

    lines = result.stdout.decode("ascii").splitlines()
    assert result.returncode == 0
    assert len(lines) == 1
    assert lines[0].startswith(f"Jerry {event} hook: ")
    assert "cannot read session file" in lines[0]
    assert file.read_bytes() == b"{not json"


def test_should_create_the_session_file_and_ask_for_a_project_on_startup(start: Path, home: Path) -> None:
    save_focus("trunks", [("PROJ-001", "/x")], cwd=start.as_posix())

    text = session_start(start)

    state = json.loads(session_file(home).read_text(encoding="utf-8"))
    assert state == {
        "cwd": start.as_posix(),
        "roots": [(start / "projects").resolve().as_posix()],
        "none": False,
        "focus": [],
    }
    assert text.startswith(HEAD)
    assert ASK in text
    assert "(`projects new <slug>`" in text
    assert "(`focus none`)" in text
    assert "Quick questions skip this." in text
    assert "If you cannot ask (non-interactive), use none." in text
    assert "Last focus" not in text
    assert "- PROJ-001 [active] Kame House: Summary of PROJ-001-kame-house." in text.splitlines()


@pytest.mark.parametrize("source", ["resume", "compact"])
def test_should_keep_the_stored_roots_and_focus_on_resume_and_compact(
    start: Path, tmp_path: Path, home: Path, source: str
) -> None:
    session_start(start)
    focus("set", "PROJ-001")
    before = session_file(home).read_bytes()
    elsewhere = tmp_path / "elsewhere"
    make_project(elsewhere / "projects", "PROJ-009-namek", title="Namek")

    text = session_start(elsewhere, source)

    assert session_file(home).read_bytes() == before
    assert "PROJ-009" not in text
    assert "- PROJ-002 [paused] Capsule Corp: Summary of PROJ-002-capsule-corp." in text.splitlines()
    assert "1. Find the seventh Dragon Ball." in text
    assert ASK not in text


@pytest.mark.parametrize("source", ["clear", "fork"])
def test_should_start_a_new_session_with_the_last_focus_from_this_cwd_on_clear_and_fork(
    start: Path, home: Path, source: str
) -> None:
    here = start.as_posix()
    save_focus("vegeta", [("PROJ-002", "/x")], cwd=here, age=200)
    save_focus("trunks", [("PROJ-001", "/x"), ("PROJ-002", "/y")], cwd=here, age=100)
    save_focus("gohan", [("PROJ-002", "/x")], cwd="/elsewhere")
    save_focus("piccolo", [], cwd=here, none=True)

    text = session_start(start, source)

    assert json.loads(session_file(home).read_text(encoding="utf-8"))["focus"] == []
    assert ASK in text
    hint = (
        "Last focus from this cwd: PROJ-001, PROJ-002. "
        f"Restore it with: {CLI} focus set PROJ-001 PROJ-002 --session {SID}"
    )
    assert hint in text.splitlines()


def test_should_not_hint_when_no_other_session_from_this_cwd_had_a_focus(start: Path, home: Path) -> None:
    save_focus("gohan", [("PROJ-002", "/x")], cwd="/elsewhere")
    sessions = session_file(home).parent
    (sessions / "not.a.session.json").write_text("{}", encoding="utf-8")

    assert "Last focus" not in session_start(start, "clear")


def test_should_say_the_session_works_without_a_project_when_focus_is_none(start: Path, home: Path) -> None:
    session_start(start)
    focus("none")

    text = session_start(start, "resume")

    assert "Focus: none. This session works without a project." in text.splitlines()
    assert ASK not in text
    assert "- PROJ-001 [active] Kame House: Summary of PROJ-001-kame-house." in text.splitlines()


def test_should_inject_the_focus_and_each_pick_up_here_as_focus_show_prints_them(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    session_start(start)
    focus("set", "PROJ-001", "PROJ-002")
    shown = capsys.readouterr().out

    text = session_start(start, "resume")

    assert text.startswith(HEAD + shown)
    assert PICK_UP in text
    assert "Old notes" not in text
    assert ASK not in text


def test_should_say_no_roots_were_found_and_not_ask(tmp_path: Path, home: Path) -> None:
    empty = tmp_path / "empty"
    empty.mkdir()

    text = session_start(empty)

    assert text == HEAD + f"No projects root found from {empty.as_posix()}; this session works without a project.\n"


def test_should_prune_old_session_files_but_keep_the_current_one(start: Path, home: Path) -> None:
    save_focus(SID, [("PROJ-001", "/x")], cwd=start.as_posix(), age=40 * DAY)
    save_focus("raditz", [("PROJ-002", "/x")], cwd=start.as_posix(), age=40 * DAY)

    session_start(start, "resume")

    assert sorted(p.name for p in session_file(home).parent.iterdir()) == [f"{SID}.json"]


def test_should_keep_a_resumed_session_from_being_pruned_by_another_session(start: Path, home: Path) -> None:
    save_focus(SID, [("PROJ-001", "/x")], cwd=start.as_posix(), age=40 * DAY)

    session_start(start, "resume")
    session_start(start, sid="vegeta")

    assert session_file(home).is_file()


def test_should_index_each_project_with_its_status_parent_links_and_summary(start: Path, home: Path) -> None:
    kame = start / "projects" / "PROJ-001-kame-house"
    make_project(kame, "PROJ-001.1-turtle-school", title="Turtle\nSchool", related=["PROJ-002"], summary="Run.\nSwim.")

    lines = session_start(start).splitlines()

    assert "- PROJ-001.1 [active] Turtle School (parent PROJ-001; related PROJ-002): Run. Swim." in lines
    assert lines.index("- PROJ-001 [active] Kame House: Summary of PROJ-001-kame-house.") < lines.index(
        "- PROJ-001.1 [active] Turtle School (parent PROJ-001; related PROJ-002): Run. Swim."
    )


@pytest.mark.parametrize(
    ("registry", "problem"),
    [
        (f"{projects.INDEX_START}\nold\n{projects.INDEX_END}\n", "registry is stale; run `projects index --write`"),
        (f"{projects.INDEX_END}\n{projects.INDEX_START}\n", "expected one"),
    ],
)
def test_should_warn_about_shadowed_ids_errors_config_errors_and_the_registry(
    start: Path, tmp_path: Path, home: Path, registry: str, problem: str
) -> None:
    make_project(tmp_path / "projects", "PROJ-001-impostor")
    make_project(start / "projects", "PROJ-003-broken", status="lost")
    (start / "projects" / "README.md").write_text(registry, encoding="utf-8")
    (home / ".jerry").mkdir()
    (home / ".jerry" / "config.toml").write_text("roots = 5\n", encoding="utf-8")

    text = session_start(start)

    warnings = text.split("\nWarnings:\n", 1)[1].split("\n\n", 1)[0].splitlines()
    assert any("PROJ-001 shadowed by the same ID in a nearer root" in w for w in warnings)
    assert any("PROJ-003-broken/project.toml: status must be one of" in w for w in warnings)
    assert any("config.toml: roots must be a list of strings" in w for w in warnings)
    assert any(problem in w for w in warnings)
    assert all(w.startswith("- ") for w in warnings)


def saga(start: Path, pick_up_chars: int) -> None:
    for n in range(1, 61):
        folder = make_project(
            start / "projects",
            f"PROJ-{n:03d}-saga-{n}",
            title=f"Saga {n} Kamehameha Kamehameha",
            status="done" if n % 2 else "active",
            summary=f"Summary {n}: " + "Spirit Bomb " * 10,
        )
        body = ("Charge the Spirit Bomb \U0001f409. " * 200)[:pick_up_chars]
        (folder / "RESUME.md").write_text(f"## Pick up here\n\n{body}\n", encoding="utf-8")


STEPS = {
    "done summaries": lambda text: "Summary 2:" in text and "Summary 1:" not in text,
    "all summaries": lambda text: "Summary" not in text and "- PROJ-001 [done]" in text,
    "done rows": lambda text: "- done: PROJ-001, PROJ-003," in text and "- PROJ-002 [active]" in text,
    "ids": lambda text: text.endswith(", PROJ-060\n") and "- PROJ-002 [active]" not in text,
    "truncated": lambda text: text.endswith("[truncated to fit the context budget]"),
}


@pytest.mark.parametrize(
    ("pick_up_chars", "step"),
    [(100, "done summaries"), (1000, "all summaries"), (1700, "done rows"), (2050, "ids"), (2350, "truncated")],
)
def test_should_trim_the_index_in_steps_to_stay_within_the_budget(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], pick_up_chars: int, step: str
) -> None:
    start = tmp_path / "start"
    saga(start, pick_up_chars)
    session_start(start)
    focus("set", "PROJ-002", "PROJ-004", "PROJ-006")
    focus_head = capsys.readouterr().out.split("\n\nPROJ-002 RESUME.md:")[0]

    text = session_start(start, "resume")

    assert hooks.units(text) <= BUDGET
    assert text.startswith(HEAD + focus_head + "\n")
    assert [name for name, reached in STEPS.items() if reached(text)] == [step]


def test_should_keep_the_ask_intact_while_trimming_sixty_projects(tmp_path: Path, home: Path) -> None:
    start = tmp_path / "start"
    saga(start, 0)

    text = session_start(start)

    assert hooks.units(text) <= BUDGET
    assert text.startswith(HEAD + "Focus: nothing is focused.")
    assert "If you cannot ask (non-interactive), use none." in text
    assert STEPS["done summaries"](text)


def test_should_point_later_focused_projects_to_their_resume_when_the_budget_runs_out(
    tmp_path: Path, home: Path
) -> None:
    start = tmp_path / "start"
    saga(start, 2950)
    session_start(start)
    focus("set", "PROJ-002", "PROJ-004", "PROJ-006")

    text = session_start(start, "resume")

    last = (start / "projects" / "PROJ-006-saga-6").resolve().as_posix()
    assert hooks.units(text) <= BUDGET
    assert text.count("Charge the Spirit Bomb") > 0
    assert "\nPROJ-004 RESUME.md:\n## Pick up here\n" in text
    assert f"\nPROJ-006 RESUME.md: no room for its Pick up here; read {last}/RESUME.md\n" in text


def test_should_count_an_emoji_as_two_utf16_units() -> None:
    assert hooks.units("\U0001f409") == 2
    assert hooks.units("Goku") == 4


def test_should_count_an_undecodable_file_name_byte_as_one_unit() -> None:
    assert hooks.units("caf\udce9") == 4


@pytest.mark.parametrize(
    "text",
    ["\U0001f409" * 5000, "a" + "\U0001f409" * 5000, "b" * (BUDGET + 1)],
    ids=["emoji", "ascii-then-emoji", "ascii"],
)
def test_should_cut_text_over_the_budget_without_splitting_an_emoji(text: str) -> None:
    cut = hooks.fit(text)

    assert hooks.units(cut) <= BUDGET
    assert cut.endswith("[truncated to fit the context budget]")
    cut.encode("utf-8")


def test_should_leave_text_at_the_budget_unchanged() -> None:
    text = "a" * (BUDGET - 2) + "\U0001f409"

    assert hooks.fit(text) == text


def test_should_stay_silent_for_a_subagent_without_a_focus(start: Path, home: Path) -> None:
    assert subagent_start() is None

    session_start(start)
    assert subagent_start() is None

    focus("none")
    assert subagent_start() is None


@pytest.mark.parametrize(
    ("focused", "expected"),
    [
        (
            [("PROJ-001", "/z/PROJ-001-kame-house"), ("PROJ-002", "/z/PROJ-002-capsule-corp")],
            "Jerry focus: {project_dir} = /z/PROJ-001-kame-house (PROJ-001, primary); "
            f"PROJ-002 = /z/PROJ-002-capsule-corp. {TAIL}",
        ),
        (
            [("PROJ-001", "/z/" + "a" * 80), ("PROJ-002", "/z/" + "b" * 80), ("PROJ-003", "/z/" + "c" * 80)],
            f"Jerry focus: {{project_dir}} = /z/{'a' * 80} (PROJ-001, primary); also PROJ-002, PROJ-003. {TAIL}",
        ),
        (
            [("PROJ-001", "/z/" + "a" * 120), *((f"PROJ-{n:03d}", f"/z/{n}") for n in range(2, 30))],
            f"Jerry focus: {{project_dir}} = /z/{'a' * 120} (PROJ-001, primary). {TAIL}",
        ),
    ],
)
def test_should_give_a_subagent_the_focus_within_300_characters(
    home: Path, focused: list[tuple[str, str]], expected: str
) -> None:
    save_focus(SID, focused)

    text = context(subagent_start(), "SubagentStart")

    assert text == expected
    assert len(text) <= 300


def test_should_cut_a_subagent_focus_with_a_very_long_primary_path_to_300_characters(home: Path) -> None:
    save_focus(SID, [("PROJ-001", "/z/" + "a" * 400)])

    text = context(subagent_start(), "SubagentStart")

    assert len(text) == 300
    assert text.startswith("Jerry focus: {project_dir} = /z/aaa")
