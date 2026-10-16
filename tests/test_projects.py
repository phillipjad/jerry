# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import os
from pathlib import Path

import pytest

from jerry import cli, projects


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
    return home


def write_config(home: Path, text: str) -> None:
    (home / ".jerry").mkdir(exist_ok=True)
    (home / ".jerry" / "config.toml").write_text(text, encoding="utf-8")


def same(a: Path, b: Path) -> bool:
    return os.path.samefile(a, b)


@pytest.mark.parametrize(
    ("name", "expected"),
    [
        ("PROJ-009-over-nine-thousand", ("PROJ-009", (9,), "over-nine-thousand")),
        ("PROJ-004.1.2-x", ("PROJ-004.1.2", (4, 1, 2), "x")),
        ("PROJ-013-a1-b2", ("PROJ-013", (13,), "a1-b2")),
    ],
)
def test_should_parse_valid_folder_names(name: str, expected: tuple[str, tuple[int, ...], str]) -> None:
    parsed = projects.parse_folder(name)

    assert parsed is not None
    assert (parsed.id, parsed.number, parsed.slug) == expected


@pytest.mark.parametrize(
    "name",
    ["PROJ-04-x", "PROJ-004-Upper", "PROJ-004", "PROJ-004-", "PROJ-004--x", "proj-004-x", "PROJ-004-" + "a" * 41],
)
def test_should_reject_invalid_folder_names(name: str) -> None:
    assert projects.parse_folder(name) is None


def test_should_find_projects_in_the_start_directorys_projects_folder(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-001-sample")

    found = projects.discover(tmp_path)

    assert list(found.projects) == ["PROJ-001"]
    assert same(found.roots[0], tmp_path / "projects")


def test_should_find_projects_one_level_up(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-001-sample")
    repo = tmp_path / "repo"
    repo.mkdir()

    found = projects.discover(repo)

    assert list(found.projects) == ["PROJ-001"]


def test_should_find_the_enclosing_root_from_inside_a_project(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "anywhere" / "store"
    project = make_project(root, "PROJ-001-sample")
    deep = project / "work" / "notes"
    deep.mkdir(parents=True)

    found = projects.discover(deep)

    assert same(found.roots[0], root)
    assert list(found.projects) == ["PROJ-001"]


def test_should_never_treat_a_parent_project_as_a_root(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "store"
    parent = make_project(root, "PROJ-004-parent")
    make_project(parent, "PROJ-004.1-child")
    work = parent / "work"
    work.mkdir()

    found = projects.discover(work)

    assert same(found.roots[0], root)
    assert list(found.projects) == ["PROJ-004", "PROJ-004.1"]


def test_should_add_configured_roots_after_the_local_ones(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-001-local")
    shared = tmp_path / "shared"
    make_project(shared, "PROJ-002-shared")
    write_config(home, f"roots = [{json.dumps(str(shared))}]\n")

    found = projects.discover(tmp_path)

    assert list(found.projects) == ["PROJ-001", "PROJ-002"]
    assert same(found.roots[-1], shared)


def test_should_expand_home_in_configured_roots(tmp_path: Path, home: Path) -> None:
    make_project(home / "store", "PROJ-003-home")
    write_config(home, "roots = ['~/store']\n")
    start = tmp_path / "empty"
    start.mkdir()

    found = projects.discover(start)

    assert list(found.projects) == ["PROJ-003"]


def test_should_warn_and_skip_relative_configured_roots(tmp_path: Path, home: Path) -> None:
    write_config(home, "roots = ['relative/store']\n")

    found = projects.discover(tmp_path)

    assert found.roots == []
    assert any("relative/store" in w and "absolute" in w for w in found.warnings)


def test_should_warn_about_configured_roots_that_do_not_exist(tmp_path: Path, home: Path) -> None:
    missing = tmp_path / "gone"
    write_config(home, f"roots = [{json.dumps(str(missing))}]\n")

    found = projects.discover(tmp_path)

    assert any("not found" in w for w in found.warnings)


@pytest.mark.parametrize("text", ["roots = [", "roots = 'not-a-list'\n", "roots = [1]\n"])
def test_should_warn_instead_of_failing_on_a_bad_config(tmp_path: Path, home: Path, text: str) -> None:
    write_config(home, text)

    found = projects.discover(tmp_path)

    assert found.roots == []
    assert any("config.toml" in w for w in found.warnings)


def test_should_keep_backslashes_in_single_quoted_windows_paths() -> None:
    roots, warnings = projects.parse_config("roots = ['C:\\Users\\me\\projects']\n", "config.toml")

    assert warnings == []
    assert roots == ["C:\\Users\\me\\projects"]


def test_should_deduplicate_roots_that_are_the_same_directory(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-sample")
    write_config(home, f"roots = [{json.dumps(str(root))}]\n")

    found = projects.discover(root)

    assert len(found.roots) == 1
    assert found.warnings == []


def test_should_deduplicate_a_symlinked_alias_of_a_root(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-sample")
    alias = tmp_path / "alias"
    try:
        alias.symlink_to(root, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks are not permitted here")
    write_config(home, f"roots = [{json.dumps(str(alias))}]\n")

    found = projects.discover(tmp_path)

    assert len(found.roots) == 1
    assert found.warnings == []


def test_should_keep_the_nearest_project_for_a_duplicate_id_and_warn_once_per_root(
    tmp_path: Path, home: Path
) -> None:
    make_project(tmp_path / "projects", "PROJ-001-near", title="Near")
    make_project(tmp_path / "projects", "PROJ-002-near")
    far = tmp_path / "far"
    make_project(far, "PROJ-001-far", title="Far")
    make_project(far, "PROJ-002-far")
    write_config(home, f"roots = [{json.dumps(str(far))}]\n")

    found = projects.discover(tmp_path)

    assert found.projects["PROJ-001"].title == "Near"
    shadow = [w for w in found.warnings if "shadow" in w]
    assert len(shadow) == 1
    assert "PROJ-001" in shadow[0] and "PROJ-002" in shadow[0]


def test_should_report_a_duplicate_id_within_one_root_as_an_error(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-013-first")
    make_project(root, "PROJ-013-second")

    found = projects.discover(tmp_path)

    assert any("PROJ-013" in e and "PROJ-013-first" in e and "PROJ-013-second" in e for e in found.errors)


def test_should_load_project_toml_with_a_bom_and_crlf_line_endings(tmp_path: Path, home: Path) -> None:
    path = tmp_path / "projects" / "PROJ-001-sample"
    path.mkdir(parents=True)
    text = 'title = "Sample"\r\nstatus = "paused"\r\nsummary = "S."\r\n'
    (path / "project.toml").write_bytes(b"\xef\xbb\xbf" + text.encode("utf-8"))

    found = projects.discover(tmp_path)

    assert found.projects["PROJ-001"].status == "paused"


def test_should_ignore_folders_without_project_toml(tmp_path: Path, home: Path) -> None:
    (tmp_path / "projects" / "PROJ-001-not-a-project").mkdir(parents=True)

    found = projects.discover(tmp_path)

    assert found.projects == {}


def test_should_warn_about_a_badly_named_folder_that_has_project_toml(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-01-short-number")

    found = projects.discover(tmp_path)

    assert found.projects == {}
    assert any("PROJ-01-short-number" in w for w in found.warnings)


@pytest.mark.parametrize(
    ("toml", "fragment"),
    [
        ("title = ", "cannot parse"),
        ('title = "T"\nsummary = "S"\n', "status"),
        ('title = "T"\nstatus = "finished"\nsummary = "S"\n', "status"),
        ('status = "active"\nsummary = "S"\n', "title"),
        ('title = "T"\nstatus = "active"\nsummary = "S"\nrelated = "PROJ-002"\n', "related"),
        ('title = "T"\nstatus = "active"\nsummary = "S"\nuses = ["proj-2"]\n', "uses"),
        ('title = "T"\nstatus = "active"\nsummary = "S"\ndepend_on = []\n', "depend_on"),
    ],
)
def test_should_report_an_invalid_project_toml_and_skip_the_project(
    tmp_path: Path, home: Path, toml: str, fragment: str
) -> None:
    path = tmp_path / "projects" / "PROJ-001-sample"
    path.mkdir(parents=True)
    (path / "project.toml").write_text(toml, encoding="utf-8")

    found = projects.discover(tmp_path)

    assert found.projects == {}
    assert any("PROJ-001-sample" in e and fragment in e for e in found.errors)


def test_should_nest_sub_projects_under_their_parent(tmp_path: Path, home: Path) -> None:
    parent = make_project(tmp_path / "projects", "PROJ-004-parent")
    make_project(parent, "PROJ-004.2-second")
    make_project(parent, "PROJ-004.10-tenth")
    make_project(parent, "PROJ-004.1-first")

    found = projects.discover(tmp_path)

    assert [p.id for p in found.children("PROJ-004")] == ["PROJ-004.1", "PROJ-004.2", "PROJ-004.10"]
    assert found.projects["PROJ-004.1"].parent == "PROJ-004"
    assert found.projects["PROJ-004.1"].depth == 1
    assert "parent: PROJ-004\n" in projects.render_show(found, "PROJ-004.1")


def test_should_report_a_child_whose_number_does_not_extend_its_parent(tmp_path: Path, home: Path) -> None:
    parent = make_project(tmp_path / "projects", "PROJ-004-parent")
    make_project(parent, "PROJ-005.1-stray")

    found = projects.discover(tmp_path)

    assert any("PROJ-005.1" in e and "PROJ-004" in e for e in found.errors)


def test_should_report_a_sub_project_number_at_the_top_of_a_root(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-004.1-orphan")

    found = projects.discover(tmp_path)

    assert any("PROJ-004.1" in e and "top of" in e for e in found.errors)


def test_should_report_a_missing_summary(tmp_path: Path, home: Path) -> None:
    path = tmp_path / "projects" / "PROJ-001-sample"
    path.mkdir(parents=True)
    (path / "project.toml").write_text('title = "T"\nstatus = "active"\n', encoding="utf-8")

    found = projects.discover(tmp_path)

    assert any("summary" in e for e in found.errors)


def test_should_warn_about_an_explicit_root_that_does_not_exist(tmp_path: Path, home: Path) -> None:
    found = projects.discover(tmp_path, roots=[tmp_path / "missing"])

    assert found.roots == []
    assert any("missing" in w and "not found" in w for w in found.warnings)


def test_should_not_scan_below_folders_that_are_not_projects(tmp_path: Path, home: Path) -> None:
    project = make_project(tmp_path / "projects", "PROJ-001-sample")
    make_project(project / "evidence" / "deep", "PROJ-001.9-hidden")

    found = projects.discover(tmp_path)

    assert list(found.projects) == ["PROJ-001"]


def test_should_compute_inverse_links(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-base")
    make_project(root, "PROJ-002-user", depends_on=["PROJ-001"], uses=["PROJ-001"], related=["PROJ-003"])
    make_project(root, "PROJ-003-new", supersedes=["PROJ-001"])

    found = projects.discover(tmp_path)

    assert found.inverse_links("PROJ-001") == {
        "blocks": ["PROJ-002"],
        "used_by": ["PROJ-002"],
        "superseded_by": ["PROJ-003"],
    }
    assert found.inverse_links("PROJ-003") == {"related": ["PROJ-002"]}


def test_should_report_unknown_and_self_links_as_errors(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-001-sample", related=["PROJ-001", "PROJ-099"])

    found = projects.discover(tmp_path)

    assert any("PROJ-001" in e and "itself" in e for e in found.errors)
    assert any("PROJ-099" in e and "not a known project" in e for e in found.errors)


def test_should_resolve_links_within_the_same_root_first(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-002-near")
    far = tmp_path / "far"
    make_project(far, "PROJ-001-far", related=["PROJ-002"])
    make_project(far, "PROJ-002-far-sibling")
    write_config(home, f"roots = [{json.dumps(str(far))}]\n")

    found = projects.discover(tmp_path)
    linker = next(p for p in found.all_projects if p.id == "PROJ-001")

    assert found.resolve("PROJ-002", linker.root).slug == "far-sibling"


def test_should_use_only_explicit_roots_when_given(tmp_path: Path, home: Path) -> None:
    make_project(tmp_path / "projects", "PROJ-001-local")
    other = tmp_path / "other"
    make_project(other, "PROJ-002-other")

    found = projects.discover(tmp_path, roots=[other])

    assert list(found.projects) == ["PROJ-002"]


def test_should_list_projects_grouped_by_root_and_indented_by_depth(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    parent = make_project(tmp_path / "projects", "PROJ-004-parent", title="Parent")
    make_project(parent, "PROJ-004.1-child", title="Child", status="done")
    monkeypatch.chdir(tmp_path)

    code = cli.main(["projects", "list"])

    lines = capsys.readouterr().out.splitlines()
    assert code == 0
    assert lines[0].endswith("/projects")
    assert lines[1:] == ["  PROJ-004  [active]  Parent", "    PROJ-004.1  [done]  Child"]


def test_should_say_when_no_projects_are_found(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    code = cli.main(["projects", "list"])

    assert code == 0
    assert "No projects found" in capsys.readouterr().out


def test_should_show_a_project_with_links_inverses_and_files(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    base = make_project(root, "PROJ-001-base", title="Base", related=["PROJ-003"])
    (base / "RESUME.md").write_text("## Pick up here\n", encoding="utf-8")
    make_project(base, "PROJ-001.1-part")
    make_project(root, "PROJ-002-user", depends_on=["PROJ-001"])
    make_project(root, "PROJ-003-peer", related=["PROJ-001"])
    monkeypatch.chdir(tmp_path)

    code = cli.main(["projects", "show", "PROJ-001"])

    out = capsys.readouterr().out
    assert code == 0
    assert out.splitlines()[0] == "PROJ-001  Base"
    assert "status: active" in out
    assert f"path: {base.resolve().as_posix()}" in out
    assert "children: PROJ-001.1" in out
    assert "related: PROJ-003" in out
    assert "blocks: PROJ-002" in out
    assert "files: RESUME.md" in out
    assert "parent:" not in out


def test_should_exit_1_for_an_unknown_project(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    code = cli.main(["projects", "show", "PROJ-404"])

    assert code == 1
    assert "PROJ-404" in capsys.readouterr().err


def test_should_print_problems_to_stderr_and_use_the_given_root(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    other = tmp_path / "other"
    make_project(other, "PROJ-001-sample", related=["PROJ-099"])

    code = cli.main(["projects", "list", "--root", str(other)])

    captured = capsys.readouterr()
    assert code == 0
    assert "PROJ-001" in captured.out
    assert "error: " in captured.err and "PROJ-099" in captured.err
