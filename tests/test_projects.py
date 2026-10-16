# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import os
import tomllib
from pathlib import Path

import pytest
from conftest import make_project

from jerry import cli, projects


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


START = "<!-- jerry:index:start -->"
END = "<!-- jerry:index:end -->"
PICK_UP = "# Resume\n\n## Pick up here\n\n- Next step.\n"
HEADER = "| ID | Title | Status | Summary | Links |\n|---|---|---|---|---|\n"


def make_tracked(parent: Path, folder: str, resume: str = PICK_UP, **fields: object) -> Path:
    path = make_project(parent, folder, **fields)
    (path / "RESUME.md").write_text(resume, encoding="utf-8")
    return path


def run_check(capsys: pytest.CaptureFixture[str], *roots: Path) -> tuple[int, list[str]]:
    code = cli.main(["projects", "check", *(arg for root in roots for arg in ("--root", str(root)))])
    return code, [line for line in capsys.readouterr().err.splitlines() if line.startswith("error: ")]


def test_should_return_the_pick_up_here_section_when_a_title_and_intro_come_first() -> None:
    text = "# PROJ-001 -- Resume\n\nIntro line.\n\n## Pick up here\n\n- Next.\n\n## History\n\nOld.\n"

    assert projects.pick_up_here(text) == "## Pick up here\n\n- Next."


def test_should_accept_a_heading_suffix_and_stop_at_a_level_one_heading() -> None:
    text = "## Pick up here (Cell saga) -- as of 2026-10-16\n- Train.\n### Detail\nMore.\n# Appendix\nX\n"

    assert projects.pick_up_here(text) == "## Pick up here (Cell saga) -- as of 2026-10-16\n- Train.\n### Detail\nMore."


def test_should_ignore_headings_inside_fenced_code_blocks() -> None:
    text = "````\n```\n## Fake\n```\n````\n## Pick up here\n~~~\n## Not a heading\n~~~\n- Done.\n## Next\n"

    assert projects.pick_up_here(text) == "## Pick up here\n~~~\n## Not a heading\n~~~\n- Done."
    assert projects.pick_up_here("```inline``` span\n## Pick up here\n- Next.\n") == "## Pick up here\n- Next."


def test_should_read_the_section_when_the_text_has_crlf_line_endings() -> None:
    text = "# T\r\n\r\n## Pick up here\r\n- Next.\r\n\r\n## History\r\n"

    assert projects.pick_up_here(text) == "## Pick up here\n- Next."


@pytest.mark.parametrize(
    "text",
    [
        "",
        "# Title\n\nNo sections.\n",
        "## History\n\n## Pick up here\n",
        "### Pick up here\n",
        " ## Pick up here\n",
        "```\n## Pick up here\n```\n",
    ],
)
def test_should_return_none_when_the_first_level_two_heading_is_not_pick_up_here(text: str) -> None:
    assert projects.pick_up_here(text) is None


def test_should_create_the_first_project_with_toml_and_a_resume_stub(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    root.mkdir()

    code = cli.main(["projects", "new", "sample", "--root", str(root)])

    created = root / "PROJ-001-sample"
    assert code == 0
    assert capsys.readouterr().out == f"{created.resolve().as_posix()}\n"
    toml = tomllib.loads((created / "project.toml").read_text(encoding="utf-8"))
    assert toml == {"title": "sample", "status": "active", "summary": ""}
    resume = (created / "RESUME.md").read_text(encoding="utf-8")
    assert resume == "# PROJ-001 -- Resume\n\n## Pick up here\n\n- Write the first next step here.\n"


def test_should_number_a_new_project_after_the_highest_number_in_any_root(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    near = tmp_path / "near"
    make_project(near, "PROJ-001-goku")
    far = tmp_path / "far"
    make_project(far, "PROJ-001-shadowed")
    make_project(far, "PROJ-012-vegeta")

    code = cli.main(["projects", "new", "gohan", "--root", str(near), "--root", str(far)])

    assert code == 0
    assert (near / "PROJ-013-gohan" / "project.toml").is_file()


def test_should_number_a_sub_project_after_its_highest_sibling_numerically(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    parent = make_project(root, "PROJ-004-parent")
    make_project(parent, "PROJ-004.1-first")
    make_project(parent, "PROJ-004.10-tenth")

    code = cli.main(["projects", "new", "eleventh", "--parent", "PROJ-004", "--root", str(root)])

    assert code == 0
    assert (parent / "PROJ-004.11-eleventh" / "project.toml").is_file()


def test_should_number_the_first_sub_project_of_a_nested_parent_one(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    child = make_project(make_project(root, "PROJ-004-parent"), "PROJ-004.1-child")

    code = cli.main(["projects", "new", "grandchild", "--parent", "PROJ-004.1", "--root", str(root)])

    assert code == 0
    assert (child / "PROJ-004.1.1-grandchild" / "project.toml").is_file()


@pytest.mark.parametrize("toml", [None, 'title = "Goku"\nstatus = "Active"\nsummary = ""\n'])
@pytest.mark.parametrize("nested", [False, True])
def test_should_skip_the_number_of_a_folder_whose_project_toml_is_missing_or_broken(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], toml: str | None, nested: bool
) -> None:
    root = tmp_path / "projects"
    parent = make_project(root, "PROJ-001-sample")
    container, broken, expected = (
        (parent, "PROJ-001.1-goku", "PROJ-001.2-vegeta") if nested else (root, "PROJ-002-goku", "PROJ-003-vegeta")
    )
    (container / broken).mkdir()
    if toml is not None:
        (container / broken / "project.toml").write_text(toml, encoding="utf-8")

    code = cli.main(["projects", "new", "vegeta", "--root", str(root), *(["--parent", "PROJ-001"] if nested else [])])

    assert code == 0
    assert (container / expected / "project.toml").is_file()


def test_should_exit_1_and_create_nothing_when_the_parent_is_unknown(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-sample")

    code = cli.main(["projects", "new", "child", "--parent", "PROJ-404", "--root", str(root)])

    assert code == 1
    assert "PROJ-404" in capsys.readouterr().err
    assert [p.name for p in root.iterdir()] == ["PROJ-001-sample"]


@pytest.mark.parametrize("slug", ["Upper", "1st", "two--hyphens", "trailing-", "a" * 41])
def test_should_exit_1_and_create_nothing_when_the_slug_is_invalid(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], slug: str
) -> None:
    root = tmp_path / "projects"
    root.mkdir()

    code = cli.main(["projects", "new", slug, "--root", str(root)])

    assert code == 1
    assert "slug" in capsys.readouterr().err
    assert list(root.iterdir()) == []


def test_should_exit_1_when_there_is_no_root_to_create_in(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    monkeypatch.chdir(tmp_path)

    code = cli.main(["projects", "new", "sample"])

    assert code == 1
    assert "no projects root" in capsys.readouterr().err
    assert [p.name for p in tmp_path.iterdir()] == ["home"]


def test_should_not_reuse_a_folder_created_concurrently_with_the_same_name(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    root.mkdir()
    real_subdirs = projects._subdirs
    calls: list[Path] = []

    def racing_subdirs(folder: Path) -> list[Path]:
        listed = real_subdirs(folder)
        calls.append(folder)
        if len(calls) == 2:
            (root / "PROJ-001-sample" / "notes").mkdir(parents=True)
        return listed

    monkeypatch.setattr(projects, "_subdirs", racing_subdirs)

    code = cli.main(["projects", "new", "sample", "--root", str(root)])

    assert code == 1
    assert "error: " in capsys.readouterr().err
    assert (root / "PROJ-001-sample" / "notes").is_dir()
    assert not (root / "PROJ-001-sample" / "project.toml").exists()


@pytest.mark.parametrize(
    ("rival_root", "rival"), [("near", "PROJ-002-alpha"), ("near", "PROJ-002-zulu"), ("far", "PROJ-002-rival")]
)
def test_should_roll_back_when_the_new_id_appears_twice_after_creating(
    tmp_path: Path,
    home: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
    rival_root: str,
    rival: str,
) -> None:
    near, far = tmp_path / "near", tmp_path / "far"
    make_project(near, "PROJ-001-sample")
    far.mkdir()
    real_discover = projects.discover
    calls: list[Path] = []

    def racing_discover(start: Path, roots: list[Path] | None = None) -> projects.Discovery:
        calls.append(start)
        if len(calls) == 2:
            make_project(tmp_path / rival_root, rival)
        return real_discover(start, roots)

    monkeypatch.setattr(projects, "discover", racing_discover)

    code = cli.main(["projects", "new", "mine", "--root", str(near), "--root", str(far)])

    assert code == 1
    assert "PROJ-002" in capsys.readouterr().err
    assert not (near / "PROJ-002-mine").exists()
    assert (tmp_path / rival_root / rival / "project.toml").is_file()


@pytest.mark.parametrize(
    "title",
    [
        'Say "hi"',
        "C:\\Users\\goku",
        "trailing backslash \\",
        "two\nlines\r\n",
        "tab\tbell\x07unit\x1fnul\x00",
        "rub\x7fout",
        "Kamehameha \U0001f409",
    ],
)
def test_should_round_trip_awkward_titles_through_toml(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], title: str
) -> None:
    root = tmp_path / "projects"
    root.mkdir()

    code = cli.main(["projects", "new", "sample", "--title", title, "--root", str(root)])

    text = (root / "PROJ-001-sample" / "project.toml").read_text(encoding="utf-8")
    assert code == 0
    assert tomllib.loads(text)["title"] == title
    assert projects.discover(tmp_path, roots=[root]).projects["PROJ-001"].title == title


def test_should_regenerate_the_registry_when_creating_a_project(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    root.mkdir()
    (root / "README.md").write_text(f"# Registry\n\n{START}\n{END}\n", encoding="utf-8")

    code = cli.main(["projects", "new", "sample", "--root", str(root)])

    assert code == 0
    readme = (root / "README.md").read_text(encoding="utf-8")
    assert readme == f"# Registry\n\n{START}\n{HEADER}| PROJ-001 | sample | active |  |  |\n{END}\n"


def test_should_leave_a_readme_without_markers_alone_when_creating_a_project(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    root.mkdir()
    (root / "README.md").write_bytes(b"# Registry\n\nHand-written.\n")

    code = cli.main(["projects", "new", "sample", "--root", str(root)])

    assert code == 0
    assert (root / "README.md").read_bytes() == b"# Registry\n\nHand-written.\n"


def test_should_print_the_registry_sorted_numerically_with_links_and_escaped_cells(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-010-ten", title="Ten", summary="")
    parent = make_project(
        root,
        "PROJ-004-four",
        title="Goku | Vegeta",
        summary="line one\nline two",
        uses=["PROJ-004.1"],
        depends_on=["PROJ-010"],
        related=["PROJ-010", "PROJ-004.2"],
    )
    make_project(parent, "PROJ-004.10-tenth", title="Tenth", summary="S10")
    make_project(parent, "PROJ-004.2-two", title="Two", summary="S2")
    make_project(parent, "PROJ-004.1-one", title="One", summary="S1", status="done")
    (root / "README.md").write_text("# Registry\n", encoding="utf-8")

    code = cli.main(["projects", "index", "--root", str(root)])

    assert code == 0
    assert capsys.readouterr().out == (
        HEADER
        + "| PROJ-004 | Goku \\| Vegeta | active | line one line two "
        + "| related PROJ-010, PROJ-004.2; depends_on PROJ-010; uses PROJ-004.1 |\n"
        + "| PROJ-004.1 | One | done | S1 |  |\n"
        + "| PROJ-004.2 | Two | active | S2 |  |\n"
        + "| PROJ-004.10 | Tenth | active | S10 |  |\n"
        + "| PROJ-010 | Ten | active |  |  |\n"
    )


def test_should_prefix_each_table_with_its_root_when_there_are_several(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    near, far = tmp_path / "near", tmp_path / "far"
    make_project(near, "PROJ-001-goku", title="Goku", summary="")
    make_project(far, "PROJ-002-vegeta", title="Vegeta", summary="")

    code = cli.main(["projects", "index", "--root", str(near), "--root", str(far)])

    assert code == 0
    assert capsys.readouterr().out == (
        f"{near.resolve().as_posix()}\n\n{HEADER}| PROJ-001 | Goku | active |  |  |\n\n"
        f"{far.resolve().as_posix()}\n\n{HEADER}| PROJ-002 | Vegeta | active |  |  |\n"
    )


def test_should_write_only_between_the_markers_and_be_idempotent(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-sample", title="Sample", summary="S")
    readme = root / "README.md"
    readme.write_text(f"# Registry\n\nBefore.\n\n{START}\nold row\n{END}\n\nAfter.\n", encoding="utf-8")

    first = cli.main(["projects", "index", "--write", "--root", str(root)])
    os.utime(readme, (1_000_000_000, 1_000_000_000))
    second = cli.main(["projects", "index", "--write", "--root", str(root)])

    assert (first, second) == (0, 0)
    assert readme.read_text(encoding="utf-8") == (
        f"# Registry\n\nBefore.\n\n{START}\n{HEADER}| PROJ-001 | Sample | active | S |  |\n{END}\n\nAfter.\n"
    )
    assert readme.stat().st_mtime == 1_000_000_000


def test_should_keep_crlf_line_endings_and_a_bom_when_writing_the_registry(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-sample")
    readme = root / "README.md"
    readme.write_bytes(f"\ufeff# Registry\r\n\r\n{START}\r\n{END}\r\nAfter.\r\n".encode())

    code = cli.main(["projects", "index", "--write", "--root", str(root)])

    data = readme.read_bytes()
    assert code == 0
    assert data.startswith(b"\xef\xbb\xbf# Registry\r\n")
    assert b"| PROJ-001 |" in data
    assert data.count(b"\n") == data.count(b"\r\n")
    assert data.endswith(f"{END}\r\nAfter.\r\n".encode())


@pytest.mark.parametrize(
    "readme",
    [
        None,
        "# Registry\n",
        f"{START}\n{START}\n{END}\n",
        f"{END}\n{START}\n",
        f"{START}\n",
        f"{START}\n{END}\n{END}\n",
        f"See {START} inline.\n{END}\n",
    ],
)
def test_should_refuse_to_write_without_exactly_one_start_line_then_one_end_line(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], readme: str | None
) -> None:
    root = tmp_path / "projects"
    make_project(root, "PROJ-001-sample")
    path = root / "README.md"
    if readme is not None:
        path.write_text(readme, encoding="utf-8")
    before = path.read_bytes() if readme is not None else None

    code = cli.main(["projects", "index", "--write", "--root", str(root)])

    err = capsys.readouterr().err
    assert code == 1
    assert "error: " in err and "README.md" in err
    assert (path.read_bytes() if path.exists() else None) == before


def test_should_pass_check_for_a_project_created_by_new(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    root.mkdir()
    (root / "README.md").write_text(f"{START}\n{END}\n", encoding="utf-8")
    cli.main(["projects", "new", "sample", "--root", str(root)])
    capsys.readouterr()

    code = cli.main(["projects", "check", "--root", str(root)])

    captured = capsys.readouterr()
    assert code == 0
    assert captured.err == ""
    assert "0 errors" in captured.out


def test_should_fail_check_when_no_root_is_found(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    code, errors = run_check(capsys, tmp_path / "missing")

    assert code == 1
    assert any("no projects root" in e for e in errors)


def test_should_fail_check_on_an_invalid_folder_name(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-01-short-number")

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-01-short-number" in e and "not a valid project folder name" in e for e in errors)


def test_should_fail_check_on_a_slug_longer_than_40_characters(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-" + "a" * 41)

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("slug is longer than 40 characters" in e for e in errors)


@pytest.mark.parametrize(
    ("folders", "fragment"),
    [(["PROJ-004-parent", "PROJ-005.1-stray"], "does not extend"), (["PROJ-004.1-orphan"], "top of")],
)
def test_should_fail_check_on_bad_nesting(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], folders: list[str], fragment: str
) -> None:
    parent = tmp_path / "projects"
    for folder in folders:
        parent = make_tracked(parent, folder)

    code, errors = run_check(capsys, tmp_path / "projects")

    assert code == 1
    assert any(fragment in e for e in errors)


def test_should_fail_check_on_an_invalid_project_toml(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-sample", status="finished")

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-001-sample/project.toml" in e and "status" in e for e in errors)


def test_should_fail_check_on_an_unknown_link(tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-sample", related=["PROJ-099"])

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-099" in e and "not a known project" in e for e in errors)


def test_should_fail_check_on_a_self_link(tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-sample", uses=["PROJ-001"])

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-001 lists itself under uses" in e for e in errors)


def test_should_fail_check_on_a_duplicate_id_within_one_root(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-013-first")
    make_tracked(root, "PROJ-013-second")

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-013 is defined twice" in e for e in errors)


def test_should_only_warn_in_check_about_ids_shadowed_across_roots(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    near, far = tmp_path / "near", tmp_path / "far"
    make_tracked(near, "PROJ-001-goku")
    make_tracked(far, "PROJ-001-kakarot")
    (near / "README.md").write_text("# Registry without markers\n", encoding="utf-8")

    code = cli.main(["projects", "check", "--root", str(near), "--root", str(far)])

    err = capsys.readouterr().err
    assert code == 0
    assert "warning: " in err and "shadowed" in err
    assert "error: " not in err


@pytest.mark.parametrize(
    ("table", "fragment"),
    [("| stale |\n", "stale"), (f"{START}\n", "expected one")],
)
def test_should_fail_check_on_a_stale_or_broken_registry(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], table: str, fragment: str
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-sample")
    (root / "README.md").write_text(f"# Registry\n\n{START}\n{table}{END}\n", encoding="utf-8")

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("README.md" in e and fragment in e for e in errors)


def test_should_pass_check_once_the_registry_is_rewritten(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-sample")
    (root / "README.md").write_text(f"{START}\n| stale |\n{END}\n", encoding="utf-8")
    cli.main(["projects", "index", "--write", "--root", str(root)])

    code, errors = run_check(capsys, root)

    assert (code, errors) == (0, [])


@pytest.mark.parametrize(("content", "fragment"), [(None, "missing"), (b"## Pick up here\n\xff\n", "cannot read")])
def test_should_fail_check_when_resume_is_missing_or_unreadable(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], content: bytes | None, fragment: str
) -> None:
    root = tmp_path / "projects"
    project = make_project(root, "PROJ-001-sample")
    if content is not None:
        (project / "RESUME.md").write_bytes(content)

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-001-sample/RESUME.md" in e and fragment in e for e in errors)


def test_should_fail_check_when_resume_does_not_open_with_pick_up_here(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-001-sample", resume="# Resume\n\n## History\n\n## Pick up here\n")

    code, errors = run_check(capsys, root)

    assert code == 1
    assert any("PROJ-001-sample/RESUME.md" in e and "## Pick up here" in e for e in errors)


@pytest.mark.parametrize(("length", "expected"), [(3000, 0), (3001, 1)])
def test_should_limit_pick_up_here_to_3000_characters(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], length: int, expected: int
) -> None:
    root = tmp_path / "projects"
    heading = "## Pick up here\n"
    make_tracked(root, "PROJ-001-sample", resume=heading + "x" * (length - len(heading)) + "\n\n## History\n\nOld.\n")

    code, errors = run_check(capsys, root)

    assert code == expected
    assert any("'## Pick up here' is 3,001 characters; the maximum is 3,000" in e for e in errors) == bool(expected)


@pytest.mark.parametrize(
    ("link", "expected"),
    [
        ("", 1),
        ("- [Child](PROJ-004.1-child/RESUME.md)\n", 0),
        ('- See [the child](<./PROJ-004.1-child/RESUME.md#pick-up-here> "Child").\n', 0),
        ("- [Child plan](PROJ-004.1-child/PLAN.md)\n", 1),
    ],
)
def test_should_require_a_parent_resume_to_link_each_child_resume(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str], link: str, expected: int
) -> None:
    root = tmp_path / "projects"
    parent = make_tracked(root, "PROJ-004-parent", resume=PICK_UP + link)
    make_tracked(parent, "PROJ-004.1-child")

    code, errors = run_check(capsys, root)

    assert code == expected
    assert any("PROJ-004.1" in e and "link" in e for e in errors) == bool(expected)


def test_should_fail_check_on_paths_longer_than_the_limit_relative_to_the_root(
    tmp_path: Path, home: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    assert projects.MAX_RELATIVE_PATH == 180
    monkeypatch.setattr(projects, "MAX_RELATIVE_PATH", 40)
    root = tmp_path / "projects"
    project = make_tracked(root, "PROJ-001-sample")
    (project / ("f" * 24)).write_text("fits exactly", encoding="utf-8")
    (project / ("g" * 25)).write_text("one over", encoding="utf-8")
    (project / ("d" * 30)).mkdir()
    (project / ("d" * 30) / "inner.md").write_text("inside a long folder", encoding="utf-8")

    code, errors = run_check(capsys, root)

    assert code == 1
    assert len(errors) == 2
    assert any(f"PROJ-001-sample/{'g' * 25}: path is 41 characters" in e for e in errors)
    assert any(f"PROJ-001-sample/{'d' * 30}: path is 46 characters" in e for e in errors)


LINK = "- [PROJ-004.1](PROJ-004.1-child/RESUME.md) Saiyan saga"


@pytest.mark.parametrize(
    ("before", "after"),
    [
        (
            "# Resume\n\n## Pick up here\n\n- Next step.\n\n## History\n\nOld.\n",
            f"# Resume\n\n## Pick up here\n\n- Next step.\n{LINK}\n\n## History\n\nOld.\n",
        ),
        (
            "﻿# Resume\r\n\r\n## Pick up here\r\n\r\n- Next step.\r\n",
            f"﻿# Resume\r\n\r\n## Pick up here\r\n\r\n- Next step.\r\n{LINK}\r\n",
        ),
        ("# Resume\n\nNotes.\n", f"# Resume\n\nNotes.\n\n{LINK}\n"),
    ],
)
def test_should_link_a_new_sub_project_from_its_parents_resume(
    tmp_path: Path, home: Path, before: str, after: str
) -> None:
    root = tmp_path / "projects"
    parent = make_project(root, "PROJ-004-parent")
    (parent / "RESUME.md").write_bytes(before.encode("utf-8"))

    code = cli.main(["projects", "new", "child", "--parent", "PROJ-004", "--title", "Saiyan saga", "--root", str(root)])

    assert code == 0
    assert (parent / "RESUME.md").read_bytes().decode("utf-8") == after


def test_should_pass_check_for_a_sub_project_created_by_new(
    tmp_path: Path, home: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    root = tmp_path / "projects"
    make_tracked(root, "PROJ-004-parent")
    cli.main(["projects", "new", "child", "--parent", "PROJ-004", "--root", str(root)])

    code, errors = run_check(capsys, root)

    assert (code, errors) == (0, [])


def test_should_not_create_a_parent_resume_when_linking_a_new_sub_project(tmp_path: Path, home: Path) -> None:
    root = tmp_path / "projects"
    parent = make_project(root, "PROJ-004-parent")

    assert cli.main(["projects", "new", "child", "--parent", "PROJ-004", "--root", str(root)]) == 0

    assert not (parent / "RESUME.md").exists()
