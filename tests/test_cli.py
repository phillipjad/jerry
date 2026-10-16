# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

from jerry import cli

ROOT = Path(__file__).resolve().parents[1]
NOTE = "# Note\n\n> **Status:** open\n\nBody.\n"


def write_note(directory: Path, name: str = "note.md", text: str = NOTE) -> Path:
    path = directory / name
    path.write_text(text, encoding="utf-8")
    return path


def run_jerry(args: list[str], cwd: Path, **env: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["uv", "run", "--no-sync", "--project", str(ROOT), "jerry", *args],
        cwd=cwd,
        env=dict(os.environ, **env),
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )


def ast_subcommands() -> set[str]:
    parser = cli.build_parser()
    namespaces = next(a for a in parser._actions if a.dest == "namespace")
    ast = namespaces.choices["ast"]
    commands = next(a for a in ast._actions if a.dest == "command")
    return set(commands.choices)


def test_should_offer_exactly_the_kept_ast_subcommands() -> None:
    assert ast_subcommands() == {"parse", "frontmatter", "validate", "modify"}


def test_should_parse_validate_options() -> None:
    args = cli.build_parser().parse_args(["ast", "validate", "f.md", "--schema", "story", "--nav"])

    assert (args.file, args.schema, args.nav) == ("f.md", "story", True)


def test_should_default_validate_options() -> None:
    args = cli.build_parser().parse_args(["ast", "validate", "f.md"])

    assert (args.schema, args.nav) == (None, False)


def test_should_parse_modify_options() -> None:
    args = cli.build_parser().parse_args(["ast", "modify", "f.md", "--key", "Status", "--value", "done"])

    assert (args.file, args.key, args.value) == ("f.md", "Status", "done")


@pytest.mark.parametrize("argv", [[], ["ast"]])
def test_should_exit_2_when_a_command_is_missing(argv: list[str]) -> None:
    with pytest.raises(SystemExit) as exit_info:
        cli.main(argv)

    assert exit_info.value.code == 2


def test_should_route_frontmatter_to_its_handler(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    note = write_note(tmp_path)

    code = cli.main(["ast", "frontmatter", str(note)])

    assert code == 0
    assert json.loads(capsys.readouterr().out) == {"Status": "open"}


def test_should_route_modify_to_its_handler(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    note = write_note(tmp_path)

    code = cli.main(["ast", "modify", str(note), "--key", "Status", "--value", "done"])

    assert code == 0
    assert "**Status:** done" in note.read_text(encoding="utf-8")


def test_should_route_parse_and_validate_to_their_handlers(tmp_path: Path) -> None:
    note = write_note(tmp_path)

    assert cli.main(["ast", "parse", str(note)]) == 0
    assert cli.main(["ast", "validate", str(note)]) == 0


def test_should_read_files_outside_the_working_directory(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    elsewhere = tmp_path / "elsewhere"
    elsewhere.mkdir()
    note = write_note(elsewhere)
    monkeypatch.chdir(tmp_path)

    code = cli.main(["ast", "frontmatter", str(note)])

    assert code == 0
    assert json.loads(capsys.readouterr().out)["Status"] == "open"


def test_should_read_a_file_with_a_byte_order_mark(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    note = tmp_path / "bom.md"
    note.write_bytes(b"\xef\xbb\xbf" + NOTE.encode("utf-8"))

    code = cli.main(["ast", "frontmatter", str(note)])

    assert code == 0
    assert json.loads(capsys.readouterr().out) == {"Status": "open"}


def test_should_refuse_files_over_one_megabyte(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    big = tmp_path / "big.md"
    big.write_bytes(b"a" * (1_048_576 + 1))

    code = cli.main(["ast", "parse", str(big)])

    assert code == 2
    assert "maximum size" in capsys.readouterr().err


def test_should_resolve_relative_paths_against_the_callers_directory(tmp_path: Path) -> None:
    write_note(tmp_path)

    result = run_jerry(["ast", "frontmatter", "note.md"], cwd=tmp_path)

    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout) == {"Status": "open"}


def test_should_report_errors_cleanly_on_a_legacy_console_encoding(tmp_path: Path) -> None:
    result = run_jerry(["ast", "parse", "missing-日本.md"], cwd=tmp_path, PYTHONIOENCODING="cp1252")

    assert result.returncode == 2
    assert "Traceback" not in result.stderr
    assert "not found" in result.stderr.lower()


def test_should_keep_the_original_and_no_temp_file_when_the_write_fails(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    note = write_note(tmp_path)

    def fail(*_: object) -> None:
        raise OSError("disk full")

    monkeypatch.setattr(os, "replace", fail)

    code = cli.main(["ast", "modify", str(note), "--key", "Status", "--value", "done"])

    assert code == 2
    assert "disk full" in capsys.readouterr().err
    assert note.read_text(encoding="utf-8") == NOTE
    assert [p.name for p in tmp_path.iterdir()] == ["note.md"]


def test_should_give_empty_content_for_a_compound_node_without_inline_text() -> None:
    from jerry.ast_cli import node_to_dict
    from jerry.markdown_ast import JerryDocument

    quote = JerryDocument.parse("> - item\n").query("blockquote")[0]

    assert node_to_dict(quote)["content"] == ""


def test_should_not_import_the_upstream_src_package() -> None:
    import jerry.ast_cli  # noqa: F401
    import jerry.markdown_ast  # noqa: F401

    assert not [name for name in sys.modules if name == "src" or name.startswith("src.")]
