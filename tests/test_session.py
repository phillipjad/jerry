# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import os
import time
from pathlib import Path

import pytest
from conftest import make_project

from jerry import cli, session

SESSION = "goku"
RESUME = "# PROJ-001 -- Resume\n\nIntro.\n\n## Pick up here\n\n1. Train with King Kai.\n\n## History\n\nOld notes.\n"


@pytest.fixture
def start(tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    start = tmp_path / "start"
    make_project(start / "projects", "PROJ-001-kame-house", title="Kame House")
    make_project(start / "projects", "PROJ-002-capsule-corp", title="Capsule Corp", status="paused")
    monkeypatch.chdir(start)
    return start


def session_file(home: Path, sid: str = SESSION) -> Path:
    return home / ".jerry" / "sessions" / f"{sid}.json"


def read_session(home: Path, sid: str = SESSION) -> dict:
    return json.loads(session_file(home, sid).read_text(encoding="utf-8"))


def focused(home: Path) -> list[str]:
    return [entry["id"] for entry in read_session(home)["focus"]]


def project_path(start: Path, folder: str) -> str:
    return (start / "projects" / folder).resolve().as_posix()


def focus(*args: str, sid: str = SESSION) -> int:
    return cli.main(["focus", *args, "--session", sid])


def test_should_refuse_focus_without_a_session_id(start: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    code = cli.main(["focus", "set", "PROJ-001"])

    assert code == 1
    assert "needs a session id: pass --session or run inside Claude Code" in capsys.readouterr().err
    assert not (home / ".jerry").exists()


def test_should_take_the_session_id_from_the_environment(
    start: Path, home: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "vegeta")

    code = cli.main(["focus", "set", "PROJ-001"])

    assert code == 0
    assert read_session(home, "vegeta")["focus"][0]["id"] == "PROJ-001"


def test_should_prefer_the_session_option_over_the_environment(home: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    assert session.session_id(None) is None

    monkeypatch.setenv("CLAUDE_CODE_SESSION_ID", "vegeta")

    assert session.session_id(None) == "vegeta"
    assert session.session_id("Goku_2-" + "a" * 121) == "Goku_2-" + "a" * 121


@pytest.mark.parametrize("sid", ["", "..", "../escape", "a/b", "a\\b", "C:evil", "a.b", "x" * 129, "goku\n"])
def test_should_reject_a_session_id_that_is_not_a_safe_file_name(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str], sid: str
) -> None:
    code = focus("set", "PROJ-001", sid=sid)

    assert code == 1
    assert "session id" in capsys.readouterr().err
    assert not (home / ".jerry").exists()


def test_should_set_the_focus_in_the_given_order_without_duplicates(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = focus("set", "PROJ-002", "PROJ-001", "PROJ-002")

    lines = capsys.readouterr().out.splitlines()
    state = read_session(home)
    primary = project_path(start, "PROJ-002-capsule-corp")
    assert code == 0
    assert state["focus"] == [
        {"id": "PROJ-002", "path": primary},
        {"id": "PROJ-001", "path": project_path(start, "PROJ-001-kame-house")},
    ]
    assert state["none"] is False
    assert "PROJ-002  [paused]  Capsule Corp  (primary)" in lines
    assert "PROJ-001  [active]  Kame House" in lines
    assert f"  path: {primary}" in lines
    assert f"{{project_dir}} = {primary}" in lines


def test_should_replace_the_focus_on_set(start: Path, home: Path) -> None:
    focus("set", "PROJ-001", "PROJ-002")

    code = focus("set", "PROJ-002")

    assert code == 0
    assert focused(home) == ["PROJ-002"]


def test_should_add_only_projects_not_already_focused(start: Path, home: Path) -> None:
    focus("set", "PROJ-001")

    code = focus("add", "PROJ-002", "PROJ-001")

    assert code == 0
    assert focused(home) == ["PROJ-001", "PROJ-002"]


def test_should_clear_the_focus_on_none_until_a_project_is_added(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    focus("set", "PROJ-001")

    assert focus("none") == 0
    assert read_session(home)["none"] is True
    assert focused(home) == []
    capsys.readouterr()
    assert focus("show") == 0
    assert "Focus: none" in capsys.readouterr().out

    assert focus("add", "PROJ-002") == 0
    assert read_session(home)["none"] is False
    assert focused(home) == ["PROJ-002"]


def test_should_show_that_nothing_is_focused_in_a_new_session(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code = focus("show")

    assert code == 0
    assert "nothing is focused" in capsys.readouterr().out
    assert not session_file(home).exists()


def test_should_print_the_pick_up_here_section_of_each_focused_project(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (start / "projects" / "PROJ-001-kame-house" / "RESUME.md").write_text(RESUME, encoding="utf-8")

    focus("set", "PROJ-001", "PROJ-002")

    out = capsys.readouterr().out
    assert "PROJ-001 RESUME.md:\n## Pick up here\n\n1. Train with King Kai.\n" in out
    assert "Old notes" not in out
    assert "PROJ-002 RESUME.md:\nNo Pick up here section; read RESUME.md.\n" in out
    assert focus("show") == 0
    assert capsys.readouterr().out == out


def test_should_refuse_an_unknown_id_and_write_nothing(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    focus("set", "PROJ-001")
    before = session_file(home).read_bytes()
    capsys.readouterr()

    code = focus("add", "PROJ-002", "PROJ-404")

    assert code == 1
    assert "PROJ-404" in capsys.readouterr().err
    assert session_file(home).read_bytes() == before
    assert focus("set", "PROJ-404", sid="trunks") == 1
    assert not session_file(home, "trunks").exists()


def test_should_refuse_an_id_found_in_two_roots_and_list_every_path(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    near = make_project(tmp_path / "near", "PROJ-007-saiyan")
    far = make_project(tmp_path / "far", "PROJ-007-namek")
    monkeypatch.chdir(tmp_path)

    code = cli.main(
        ["focus", "set", "PROJ-007", "--root", str(near.parent), "--root", str(far.parent), "--session", SESSION]
    )

    err = capsys.readouterr().err
    assert code == 1
    assert "ambiguous" in err
    assert near.resolve().as_posix() in err
    assert far.resolve().as_posix() in err
    assert not session_file(home).exists()


def test_should_let_root_override_the_session_roots(start: Path, tmp_path: Path, home: Path) -> None:
    focus("set", "PROJ-001")
    other = make_project(tmp_path / "other", "PROJ-009-other")

    code = cli.main(["focus", "add", "PROJ-009", "--root", str(other.parent), "--session", SESSION])

    state = read_session(home)
    assert code == 0
    assert state["focus"][1] == {"id": "PROJ-009", "path": other.resolve().as_posix()}
    assert state["roots"] == [(start / "projects").resolve().as_posix()]


def test_should_keep_the_session_roots_after_a_change_of_directory(
    start: Path, tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    focus("add", "PROJ-001")
    elsewhere = tmp_path / "elsewhere"
    make_project(elsewhere / "projects", "PROJ-002-impostor")
    monkeypatch.chdir(elsewhere)

    code = focus("add", "PROJ-002")

    state = read_session(home)
    assert code == 0
    assert os.path.samefile(state["cwd"], start)
    assert state["roots"] == [(start / "projects").resolve().as_posix()]
    assert state["focus"][1]["path"] == project_path(start, "PROJ-002-capsule-corp")


def test_should_list_projects_from_the_session_roots(
    start: Path, tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    focus("set", "PROJ-001")
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    monkeypatch.chdir(elsewhere)
    capsys.readouterr()

    assert cli.main(["projects", "list", "--session", SESSION]) == 0
    assert "  PROJ-002  [paused]  Capsule Corp" in capsys.readouterr().out
    assert cli.main(["projects", "show", "PROJ-002", "--session", SESSION]) == 0
    assert "PROJ-002  Capsule Corp" in capsys.readouterr().out


def test_should_re_resolve_a_focused_project_after_its_folder_moves(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    focus("set", "PROJ-001", "PROJ-002")
    (start / "projects" / "PROJ-001-kame-house").rename(start / "projects" / "PROJ-001-kame-island")
    capsys.readouterr()

    code = focus("show")

    moved = project_path(start, "PROJ-001-kame-island")
    assert code == 0
    assert read_session(home)["focus"][0] == {"id": "PROJ-001", "path": moved}
    assert f"{{project_dir}} = {moved}" in capsys.readouterr().out.splitlines()


def test_should_retry_the_replace_when_the_session_file_is_briefly_locked(
    home: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    real_replace = os.replace
    calls = []

    def flaky(source: str, target: str) -> None:
        calls.append(target)
        if len(calls) == 1:
            raise PermissionError("locked")
        real_replace(source, target)

    monkeypatch.setattr(os, "replace", flaky)

    session.save(SESSION, session.Session(cwd="/start", roots=["/start/projects"]))

    assert len(calls) == 2
    assert read_session(home) == {"cwd": "/start", "roots": ["/start/projects"], "none": False, "focus": []}


def test_should_report_a_session_file_that_stays_locked_and_leave_no_temp_file(
    start: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    def locked(*_: object) -> None:
        raise PermissionError("locked")

    monkeypatch.setattr(os, "replace", locked)
    monkeypatch.setattr(time, "sleep", lambda _: None)

    code = focus("set", "PROJ-001")

    assert code == 1
    assert "locked" in capsys.readouterr().err
    assert list(session_file(home).parent.iterdir()) == []


@pytest.mark.parametrize(
    "data",
    [
        b"{not json",
        b"\xff\xfe",
        b"[]",
        b'{"cwd": "/x", "roots": "/x", "none": false, "focus": []}',
        b'{"cwd": "/x", "roots": [], "none": false, "focus": [{"id": "PROJ-001"}]}',
    ],
)
def test_should_report_a_corrupt_session_file_without_changing_it(
    start: Path, home: Path, capsys: pytest.CaptureFixture[str], data: bytes
) -> None:
    file = session_file(home)
    file.parent.mkdir(parents=True)
    file.write_bytes(data)

    code = focus("set", "PROJ-001")

    assert code == 1
    assert "session file" in capsys.readouterr().err
    assert file.read_bytes() == data


def test_should_prune_old_session_files_but_never_the_current_one(home: Path) -> None:
    sessions = home / ".jerry" / "sessions"
    sessions.mkdir(parents=True)
    old = time.time() - 31 * 86400
    for name in ("current", "stale", "fresh"):
        (sessions / f"{name}.json").write_text("{}", encoding="utf-8")
    for name in ("current", "stale"):
        os.utime(sessions / f"{name}.json", (old, old))

    session.prune("current")

    assert sorted(p.name for p in sessions.iterdir()) == ["current.json", "fresh.json"]


def test_should_prune_nothing_when_no_session_was_ever_written(home: Path) -> None:
    session.prune("current")

    assert not (home / ".jerry").exists()


def test_should_add_a_new_project_to_the_session_focus(start: Path, home: Path) -> None:
    focus("none")

    code = cli.main(["projects", "new", "majin-buu", "--session", SESSION])

    assert code == 0
    assert read_session(home)["none"] is False
    assert read_session(home)["focus"] == [{"id": "PROJ-003", "path": project_path(start, "PROJ-003-majin-buu")}]


def test_should_append_a_new_project_after_the_primary(start: Path, home: Path) -> None:
    focus("set", "PROJ-001")

    assert cli.main(["projects", "new", "majin-buu", "--session", SESSION]) == 0

    assert focused(home) == ["PROJ-001", "PROJ-003"]


def test_should_leave_the_session_alone_when_new_fails(start: Path, home: Path) -> None:
    focus("set", "PROJ-001")
    before = session_file(home).read_text(encoding="utf-8")

    assert cli.main(["projects", "new", "Not-A-Slug", "--session", SESSION]) == 1

    assert session_file(home).read_text(encoding="utf-8") == before


def test_should_not_create_a_session_when_new_runs_without_one(start: Path, home: Path) -> None:
    assert cli.main(["projects", "new", "majin-buu"]) == 0

    assert not (home / ".jerry").exists()
