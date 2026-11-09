# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import subprocess
from pathlib import Path

import pytest
from conftest import make_project

from jerry import cli, save

START = "<!-- jerry:index:start -->"
END = "<!-- jerry:index:end -->"
PICK_UP = "# Resume\n\n## Pick up here\n\n- Next step.\n"


def git(cwd: Path, *args: str) -> str:
    return subprocess.run(["git", "-C", str(cwd), *args], check=True, capture_output=True, text=True).stdout


def tracked(parent: Path, folder: str, **fields: object) -> Path:
    path = make_project(parent, folder, **fields)
    (path / "RESUME.md").write_text(PICK_UP, encoding="utf-8")
    return path


def configure(repo: Path) -> None:
    for key, value in (("user.name", "Goku"), ("user.email", "goku@example.com"), ("commit.gpgsign", "false")):
        git(repo, "config", key, value)


def run_save(capsys: pytest.CaptureFixture[str], root: Path, *args: str) -> tuple[int, str, str]:
    code = cli.main(["projects", "save", *args, "--root", str(root)])
    captured = capsys.readouterr()
    return code, captured.out, captured.err


def committed(repo: Path) -> list[str]:
    return git(repo, "show", "--name-only", "--format=", "HEAD").split()


@pytest.fixture
def remote(tmp_path: Path, home: Path) -> Path:
    remote = tmp_path / "remote.git"
    root = tmp_path / "seed"
    tracked(root, "PROJ-001-goku", title="Goku", summary="")
    tracked(root, "PROJ-002-vegeta", title="Vegeta", summary="")
    (root / "README.md").write_text(f"# Registry\n\n{START}\n{END}\n", encoding="utf-8")
    assert cli.main(["projects", "index", "--write", "--root", str(root)]) == 0
    git(tmp_path, "init", "-q", "-b", "main", str(root))
    configure(root)
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "Seed")
    git(tmp_path, "init", "-q", "--bare", str(remote))
    git(root, "push", "-q", str(remote), "main")
    git(remote, "symbolic-ref", "HEAD", "refs/heads/main")
    return remote


def clone(remote: Path, path: Path) -> Path:
    git(remote.parent, "clone", "-q", str(remote), str(path))
    configure(path)
    return path


@pytest.fixture
def root(remote: Path, tmp_path: Path) -> Path:
    return clone(remote, tmp_path / "projects")


def test_should_commit_only_the_named_projects_folder_and_the_refreshed_registry(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    goku = root / "PROJ-001-goku"
    (goku / "project.toml").write_text('title = "Goku"\nstatus = "done"\nsummary = ""\n', encoding="utf-8")
    (goku / "work").mkdir()
    (goku / "work" / "notes.md").write_text("Kamehameha.\n", encoding="utf-8")
    (root / "PROJ-002-vegeta" / "RESUME.md").write_text(PICK_UP + "- Final Flash.\n", encoding="utf-8")

    code, out, err = run_save(capsys, root, "PROJ-001", "-m", "Close PROJ-001")

    assert (code, err) == (0, "")
    assert out.startswith(f"{root.resolve().as_posix()}: committed ") and out.endswith(" (3 files)\n")
    assert sorted(committed(root)) == ["PROJ-001-goku/project.toml", "PROJ-001-goku/work/notes.md", "README.md"]
    assert git(root, "log", "-1", "--format=%s") == "Close PROJ-001\n"
    assert git(root, "status", "--porcelain") == " M PROJ-002-vegeta/RESUME.md\n"


def test_should_leave_other_staged_changes_staged(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (root / "PROJ-001-goku" / "RESUME.md").write_text(PICK_UP + "- Spirit Bomb.\n", encoding="utf-8")
    (root / "notes.md").write_text("Not a project.\n", encoding="utf-8")
    git(root, "add", "notes.md")

    code, _, _ = run_save(capsys, root, "PROJ-001", "-m", "Update PROJ-001")

    assert code == 0
    assert committed(root) == ["PROJ-001-goku/RESUME.md"]
    assert git(root, "status", "--porcelain") == "A  notes.md\n"


def test_should_save_the_session_focus_when_no_ids_are_given(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["focus", "set", "PROJ-002", "--session", "s1", "--root", str(root)]) == 0
    (root / "PROJ-001-goku" / "RESUME.md").write_text(PICK_UP + "- Not this one.\n", encoding="utf-8")
    (root / "PROJ-002-vegeta" / "RESUME.md").write_text(PICK_UP + "- Final Flash.\n", encoding="utf-8")
    capsys.readouterr()

    code, _, _ = run_save(capsys, root, "-m", "Update PROJ-002", "--session", "s1")

    assert code == 0
    assert committed(root) == ["PROJ-002-vegeta/RESUME.md"]


def test_should_save_a_sub_projects_whole_top_level_folder(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    assert cli.main(["projects", "new", "gohan", "--parent", "PROJ-001", "--root", str(root)]) == 0
    capsys.readouterr()

    code, out, _ = run_save(capsys, root, "PROJ-001.1", "-m", "Add PROJ-001.1")

    assert code == 0, out
    assert sorted(committed(root)) == [
        "PROJ-001-goku/PROJ-001.1-gohan/RESUME.md",
        "PROJ-001-goku/PROJ-001.1-gohan/project.toml",
        "PROJ-001-goku/RESUME.md",
        "README.md",
    ]


def test_should_report_nothing_to_commit(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    head = git(root, "rev-parse", "HEAD")

    code, out, _ = run_save(capsys, root, "PROJ-001", "-m", "Nothing")

    assert code == 0
    assert out == f"{root.resolve().as_posix()}: nothing to commit\n"
    assert git(root, "rev-parse", "HEAD") == head


def test_should_refuse_to_save_when_check_reports_errors(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    (root / "PROJ-001-goku" / "RESUME.md").write_text("# Resume\n\nNo section.\n", encoding="utf-8")
    head = git(root, "rev-parse", "HEAD")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Break it")

    assert code == 1
    assert "jerry projects check reports 1 error" in err and "Pick up here" in err
    assert git(root, "rev-parse", "HEAD") == head


def test_should_refuse_to_save_when_the_registry_markers_are_misplaced(
    root: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (root / "README.md").write_text(f"{START}\n{START}\n{END}\n", encoding="utf-8")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Markers")

    assert code == 1
    assert "README.md: expected one" in err


@pytest.mark.parametrize(
    ("text", "kind"),
    [
        ("{home}/Documents/x", "home path"),
        ("{home_backslashed}", "home path"),
        ("/private/tmp/claude-501/-x-/scratchpad/out.txt", "scratchpad path"),
        ("token " + "gh" + "p_" + "A1" * 18, "secret"),
        ("-----BEGIN OPENSSH " + "PRIVATE KEY-----", "secret"),
        ("AK" + "IA" + "ABCDEFGHIJKLMNOP", "secret"),
        ("xo" + "xb-" + "1234567890-abc", "secret"),
        ("sk" + "-ant-" + "a" * 24, "secret"),
        ("ey" + "J" + "a" * 12 + ".ey" + "J" + "b" * 12 + "." + "c" * 12, "secret"),
    ],
    ids=["home", "home-json", "scratchpad", "github", "private-key", "aws", "slack", "anthropic", "jwt"],
)
def test_should_refuse_files_that_hold_a_home_path_scratchpad_path_or_secret(
    root: Path, home: Path, capsys: pytest.CaptureFixture[str], text: str, kind: str
) -> None:
    line = text.format(home=home.as_posix(), home_backslashed=str(home).replace("/", "\\").replace("\\", "\\\\"))
    evidence = root / "PROJ-001-goku" / "evidence"
    evidence.mkdir()
    (evidence / "log.txt").write_text(f"first\n{line}\n", encoding="utf-8")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Leak")

    assert code == 1
    assert f"PROJ-001-goku/evidence/log.txt:2: {kind}" in err
    assert line not in err
    assert git(root, "status", "--porcelain") == "?? PROJ-001-goku/evidence/\n"


def test_should_scrub_a_file_that_was_staged_before_the_save(
    root: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    (root / "PROJ-001-goku" / "log.txt").write_text(f"{home.as_posix()}/x\n", encoding="utf-8")
    git(root, "add", "-A")
    head = git(root, "rev-parse", "HEAD")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Leak")

    assert code == 1
    assert "PROJ-001-goku/log.txt:1: home path" in err
    assert git(root, "rev-parse", "HEAD") == head


def test_should_skip_ignored_deleted_and_binary_files_when_scrubbing(
    root: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    goku = root / "PROJ-001-goku"
    (goku / "old.md").write_text("Old.\n", encoding="utf-8")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "Old")
    (goku / "old.md").unlink()
    (root / ".gitignore").write_text("*.local\n", encoding="utf-8")
    (goku / "paths.local").write_text(home.as_posix(), encoding="utf-8")
    (goku / "image.bin").write_bytes(b"\0" + home.as_posix().encode())

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Add binary")

    assert (code, err) == (0, "")
    assert sorted(committed(root)) == ["PROJ-001-goku/image.bin", "PROJ-001-goku/old.md"]


def test_should_refuse_a_root_outside_git(tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "loose"
    tracked(root, "PROJ-001-goku")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Nowhere")

    assert code == 1
    assert f"{root.resolve().as_posix()}: not in a git repository" in err


@pytest.mark.parametrize(("ids", "message"), [(["PROJ-404"], "unknown project: PROJ-404"), ([], "no projects to save")])
def test_should_refuse_unknown_ids_and_an_empty_focus(
    root: Path, capsys: pytest.CaptureFixture[str], ids: list[str], message: str
) -> None:
    code, _, err = run_save(capsys, root, *ids, "-m", "Who")

    assert code == 1
    assert message in err


def test_should_rebase_onto_the_remote_then_push(
    remote: Path, root: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    other = clone(remote, tmp_path / "other")
    (other / "PROJ-002-vegeta" / "RESUME.md").write_text(PICK_UP + "- Final Flash.\n", encoding="utf-8")
    git(other, "commit", "-q", "-am", "Vegeta")
    git(other, "push", "-q")
    (root / "PROJ-001-goku" / "RESUME.md").write_text(PICK_UP + "- Spirit Bomb.\n", encoding="utf-8")
    (root / "scratch.md").write_text("draft\n", encoding="utf-8")
    git(root, "add", "scratch.md")
    git(root, "commit", "-q", "-m", "Local draft")
    (root / "scratch.md").write_text("dirty\n", encoding="utf-8")

    code, out, err = run_save(capsys, root, "PROJ-001", "-m", "Goku", "--push")

    assert (code, err) == (0, ""), err
    assert out.endswith("(1 file); pushed\n")
    assert git(remote, "log", "--format=%s", "main") == "Goku\nLocal draft\nVegeta\nSeed\n"
    assert (root / "scratch.md").read_text(encoding="utf-8") == "dirty\n"


def test_should_abort_the_rebase_and_keep_the_commit_when_the_pull_conflicts(
    remote: Path, root: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    other = clone(remote, tmp_path / "other")
    (other / "PROJ-001-goku" / "RESUME.md").write_text(PICK_UP + "- Theirs.\n", encoding="utf-8")
    git(other, "commit", "-q", "-am", "Theirs")
    git(other, "push", "-q")
    (root / "PROJ-001-goku" / "RESUME.md").write_text(PICK_UP + "- Ours.\n", encoding="utf-8")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Ours", "--push")

    assert code == 1
    assert "pull failed, nothing pushed; any rebase was aborted" in err
    assert git(root, "log", "-1", "--format=%s") == "Ours\n"
    assert git(root, "status", "--porcelain") == ""
    assert git(remote, "log", "-1", "--format=%s", "main") == "Theirs\n"


def test_should_refuse_to_push_a_branch_without_an_upstream(root: Path, capsys: pytest.CaptureFixture[str]) -> None:
    git(root, "switch", "-q", "-c", "local")
    (root / "PROJ-001-goku" / "RESUME.md").write_text(PICK_UP + "- Ours.\n", encoding="utf-8")

    code, _, err = run_save(capsys, root, "PROJ-001", "-m", "Ours", "--push")

    assert code == 1
    assert "pull failed" in err
    assert git(root, "log", "-1", "--format=%s") == "Ours\n"


def test_should_skip_the_home_check_when_home_is_the_filesystem_root() -> None:
    assert save.scrub("/etc/hosts\n", "/") == []


def test_should_not_flag_placeholders_or_a_longer_name_that_extends_home() -> None:
    assert save.scrub("/Users/<name>/ and /home/goku2/x\n", "/home/goku") == []
