# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Unit tests for the jerry ast command implementations."""

from __future__ import annotations

import json
from io import StringIO
from pathlib import Path
from unittest.mock import patch

import pytest

from jerry.ast_cli import (
    ast_frontmatter,
    ast_modify,
    ast_parse,
    ast_validate,
    node_to_dict,
    token_to_dict,
)


@pytest.fixture()
def tmp_md_file(tmp_path: Path) -> Path:
    """Create a temporary markdown file for testing."""
    md_content = "# Hello World\n\nThis is a paragraph.\n\n> **Key:** value\n\n## Section Two\n\nMore text.\n"
    md_file = tmp_path / "test.md"
    md_file.write_text(md_content, encoding="utf-8")
    return md_file



@pytest.fixture()
def tmp_heading_file(tmp_path: Path) -> Path:
    """Create a markdown file with multiple headings."""
    md_content = "# First\n\n## Second\n\n### Third\n\nParagraph here.\n"
    md_file = tmp_path / "headings.md"
    md_file.write_text(md_content, encoding="utf-8")
    return md_file



@pytest.fixture()
def nonexistent_file(tmp_path: Path) -> Path:
    """Return a path to a file that does not exist."""
    return tmp_path / "nonexistent.md"



class TestTokenToDict:
    """Tests for the token_to_dict serialization helper."""

    def test_converts_basic_token_fields(self) -> None:
        """token_to_dict includes type, tag, nesting, content fields."""
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark")
        tokens = md.parse("# Hello\n")
        # find the heading_open token
        heading_open = next(t for t in tokens if t.type == "heading_open")
        result = token_to_dict(heading_open)
        assert result["type"] == "heading_open"
        assert result["tag"] == "h1"
        assert "nesting" in result
        assert "map" in result
        assert "content" in result

    def test_map_is_list_or_none(self) -> None:
        """token_to_dict converts map to list or None."""
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark")
        tokens = md.parse("# Hello\n")
        for token in tokens:
            result = token_to_dict(token)
            assert result["map"] is None or isinstance(result["map"], list)

    def test_content_is_string(self) -> None:
        """token_to_dict returns content as string."""
        from markdown_it import MarkdownIt

        md = MarkdownIt("commonmark")
        tokens = md.parse("Paragraph text.\n")
        for token in tokens:
            result = token_to_dict(token)
            assert isinstance(result["content"], str)



class TestNodeToDict:
    """Tests for the node_to_dict serialization helper."""

    def test_converts_node_type(self) -> None:
        """node_to_dict includes node type."""
        from jerry.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello\n")
        headings = doc.query("heading")
        assert len(headings) > 0
        result = node_to_dict(headings[0])
        assert result["type"] == "heading"

    def test_includes_tag_field(self) -> None:
        """node_to_dict includes tag from opening token."""
        from jerry.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello\n")
        headings = doc.query("heading")
        result = node_to_dict(headings[0])
        assert "tag" in result

    def test_includes_map_field(self) -> None:
        """node_to_dict includes map (line range) from opening token."""
        from jerry.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello\n")
        headings = doc.query("heading")
        result = node_to_dict(headings[0])
        assert "map" in result

    def test_includes_content_from_inline_children(self) -> None:
        """node_to_dict extracts text content from inline children."""
        from jerry.markdown_ast.jerry_document import JerryDocument

        doc = JerryDocument.parse("# Hello World\n")
        headings = doc.query("heading")
        result = node_to_dict(headings[0])
        assert "content" in result
        assert "Hello World" in result["content"]



class TestAstParse:
    """Tests for ast_parse function."""

    def test_parse_returns_exit_code_0_on_success(self, tmp_md_file: Path) -> None:
        """ast_parse returns 0 for a valid file."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_parse(str(tmp_md_file))
        assert result == 0

    def test_parse_outputs_json_with_file_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse outputs JSON containing file key."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "file" in data
        assert str(tmp_md_file) in data["file"]

    def test_parse_outputs_json_with_tokens_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse outputs JSON containing tokens list."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "tokens" in data
        assert isinstance(data["tokens"], list)
        assert len(data["tokens"]) > 0

    def test_parse_outputs_json_with_tree_key(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse outputs JSON containing tree with root type."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "tree" in data
        assert data["tree"]["type"] == "root"

    def test_parse_token_has_required_fields(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse tokens contain type, tag, nesting, map, content fields."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        token = data["tokens"][0]
        assert "type" in token
        assert "tag" in token
        assert "nesting" in token
        assert "map" in token
        assert "content" in token

    def test_parse_file_not_found_returns_exit_code_2(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse returns exit code 2 when file does not exist."""
        result = ast_parse(str(nonexistent_file))
        assert result == 2

    def test_parse_file_not_found_prints_error(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse prints an error message to stderr (not stdout) when
        the file does not exist (GH #371: stdout must stay clean for
        JSON-consuming pipelines)."""
        ast_parse(str(nonexistent_file))
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_parse_output_is_valid_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse output is parseable as JSON."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        # Should not raise
        data = json.loads(captured.out)
        assert data is not None

    def test_parse_tree_has_children(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse tree root contains children list."""
        ast_parse(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "children" in data["tree"]
        assert isinstance(data["tree"]["children"], list)

    def test_parse_oserror_returns_exit_code_2(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_parse returns 2 when file read raises OSError."""
        from unittest.mock import patch as mock_patch

        # Mock Path.read_text at instance level to simulate OSError
        with mock_patch.object(Path, "read_text", side_effect=OSError("Permission denied")):
            result = ast_parse(str(tmp_md_file))
        assert result == 2



class TestAstValidate:
    """Tests for ast_validate function."""

    def test_validate_returns_exit_code_0_for_valid_file(self, tmp_md_file: Path) -> None:
        """ast_validate returns 0 for a parseable file."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file))
        assert result == 0

    def test_validate_no_schema_outputs_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate without --schema outputs JSON with nav table results."""
        ast_validate(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "missing_nav_entries" in data
        assert "orphaned_nav_entries" in data
        assert "schema_valid" in data
        assert data["schema_valid"] is True
        assert "schema_violations" in data
        assert data["schema_violations"] == []

    def test_validate_with_unknown_schema_returns_exit_code_2(self, tmp_md_file: Path) -> None:
        """ast_validate with an unknown --schema type returns 2 (usage error)."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema="entity")
        assert result == 2

    def test_validate_with_task_schema_returns_exit_code_1_for_invalid_doc(
        self, tmp_md_file: Path
    ) -> None:
        """ast_validate with --schema task returns 1 when document has violations."""
        # tmp_md_file does not have required 'Type', 'Status', etc. fields
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema="task")
        assert result == 1

    def test_validate_with_schema_outputs_json_report(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with --schema outputs a JSON report with nav table fields."""
        ast_validate(str(tmp_md_file), schema="task")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "is_valid" in data
        assert "nav_table_valid" in data
        assert "missing_nav_entries" in data
        assert "orphaned_nav_entries" in data
        assert "schema_valid" in data
        assert "violations" in data
        assert "entity_type" in data
        assert data["entity_type"] == "task"

    def test_validate_with_none_schema_returns_exit_code_0(self, tmp_md_file: Path) -> None:
        """ast_validate with schema=None returns 0."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_validate(str(tmp_md_file), schema=None)
        assert result == 0

    def test_validate_file_not_found_returns_exit_code_2(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate returns exit code 2 when file does not exist."""
        result = ast_validate(str(nonexistent_file))
        assert result == 2

    def test_validate_file_not_found_prints_error(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate prints an error message to stderr (not stdout) when
        the file does not exist (GH #371)."""
        ast_validate(str(nonexistent_file))
        captured = capsys.readouterr()
        assert captured.out == ""
        assert "not found" in captured.err.lower() or "error" in captured.err.lower()

    def test_validate_with_unknown_schema_prints_error_to_stderr_only(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with an unknown --schema type prints the error to
        stderr, leaving stdout empty (GH #371: unknown-schema is a
        diagnostic, not a JSON payload)."""
        result = ast_validate(str(tmp_md_file), schema="entity")
        captured = capsys.readouterr()
        assert result == 2
        assert captured.out == ""
        assert "error" in captured.err.lower()

    def test_validate_nav_flag_includes_entries(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate --nav includes detailed nav table entries."""
        md = (
            "# Title\n\n"
            "| Section | Purpose |\n"
            "|---------|----------|\n"
            "| [Details](#details) | Info |\n\n"
            "## Details\n\nSome text.\n"
        )
        md_file = tmp_path / "nav.md"
        md_file.write_text(md, encoding="utf-8")
        ast_validate(str(md_file), nav=True)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nav_entries" in data
        assert isinstance(data["nav_entries"], list)
        assert len(data["nav_entries"]) > 0
        entry = data["nav_entries"][0]
        assert "section_name" in entry
        assert "anchor" in entry
        assert "description" in entry
        assert "line_number" in entry

    def test_validate_no_nav_flag_excludes_entries(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate without --nav does not include nav_entries key."""
        ast_validate(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nav_entries" not in data

    def test_validate_with_schema_and_nav_includes_entries(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with --schema AND --nav includes nav_entries in output."""
        md = (
            "# TASK-099 Test Task\n\n"
            "> **Type:** task\n"
            "> **Status:** pending\n"
            "> **Priority:** medium\n"
            "> **Created:** 2026-02-23\n"
            "> **Parent:** FEAT-001\n\n"
            "| Section | Purpose |\n"
            "|---------|----------|\n"
            "| [Summary](#summary) | Overview |\n\n"
            "## Summary\n\nThis is a test task.\n"
        )
        md_file = tmp_path / "task.md"
        md_file.write_text(md, encoding="utf-8")
        ast_validate(str(md_file), schema="task", nav=True)
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert "nav_entries" in data
        assert isinstance(data["nav_entries"], list)
        assert len(data["nav_entries"]) > 0
        entry = data["nav_entries"][0]
        assert "section_name" in entry
        assert "anchor" in entry
        assert "description" in entry
        assert "line_number" in entry

    def test_validate_with_schema_returns_exit_code_0_for_valid_doc(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_validate with --schema returns 0 when document passes validation."""
        md = (
            "# TASK-100 Valid Task\n\n"
            "> **Type:** task\n"
            "> **Status:** pending\n"
            "> **Priority:** high\n"
            "> **Created:** 2026-02-23\n"
            "> **Parent:** FEAT-001\n\n"
            "| Section | Purpose |\n"
            "|---------|----------|\n"
            "| [Summary](#summary) | Overview |\n\n"
            "## Summary\n\nA fully valid task document.\n"
        )
        md_file = tmp_path / "valid-task.md"
        md_file.write_text(md, encoding="utf-8")
        result = ast_validate(str(md_file), schema="task")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert result == 0
        assert data["is_valid"] is True
        assert data["schema_valid"] is True
        assert data["violations"] == []



class TestAstFrontmatter:
    """Tests for ast_frontmatter function."""

    def test_frontmatter_returns_exit_code_0(self, tmp_md_file: Path) -> None:
        """ast_frontmatter returns 0 for a valid file with frontmatter."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_frontmatter(str(tmp_md_file))
        assert result == 0

    def test_frontmatter_outputs_json_dict(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter outputs a JSON object with frontmatter fields."""
        ast_frontmatter(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, dict)
        assert data.get("Key") == "value"

    def test_frontmatter_empty_for_no_frontmatter(
        self, tmp_path: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter returns {} for files without frontmatter."""
        plain_file = tmp_path / "plain.md"
        plain_file.write_text("# Just heading\n\nNo frontmatter.\n", encoding="utf-8")
        ast_frontmatter(str(plain_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data == {}

    def test_frontmatter_file_not_found(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter returns exit code 2 for missing file."""
        result = ast_frontmatter(str(nonexistent_file))
        assert result == 2

    def test_frontmatter_output_is_valid_json(
        self, tmp_md_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_frontmatter output is parseable as JSON."""
        ast_frontmatter(str(tmp_md_file))
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data is not None



class TestAstModify:
    """Tests for ast_modify function."""

    @pytest.fixture()
    def tmp_entity_file(self, tmp_path: Path) -> Path:
        """Create a temporary file with blockquote frontmatter."""
        md = "# Test Entity\n\n> **Status:** pending\n> **Type:** story\n\n## Details\n\nContent.\n"
        f = tmp_path / "entity.md"
        f.write_text(md, encoding="utf-8")
        return f

    def test_modify_returns_exit_code_0(self, tmp_entity_file: Path) -> None:
        """ast_modify returns 0 on successful modification."""
        with patch("sys.stdout", new_callable=StringIO):
            result = ast_modify(str(tmp_entity_file), "Status", "done")
        assert result == 0

    def test_modify_writes_file_back(self, tmp_entity_file: Path) -> None:
        """ast_modify writes the modified content back to disk."""
        with patch("sys.stdout", new_callable=StringIO):
            ast_modify(str(tmp_entity_file), "Status", "done")
        content = tmp_entity_file.read_text(encoding="utf-8")
        assert "done" in content

    def test_modify_outputs_json_status(
        self, tmp_entity_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify outputs JSON with file, key, value, status fields."""
        ast_modify(str(tmp_entity_file), "Status", "done")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert data["key"] == "Status"
        assert data["value"] == "done"
        assert data["status"] == "modified"

    def test_modify_preserves_other_fields(self, tmp_entity_file: Path) -> None:
        """ast_modify preserves other frontmatter fields."""
        with patch("sys.stdout", new_callable=StringIO):
            ast_modify(str(tmp_entity_file), "Status", "done")
        content = tmp_entity_file.read_text(encoding="utf-8")
        assert "story" in content

    def test_modify_missing_key_returns_exit_code_1(
        self, tmp_entity_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify returns 1 when key does not exist in frontmatter."""
        result = ast_modify(str(tmp_entity_file), "NonExistent", "value")
        assert result == 1

    def test_modify_missing_key_prints_error_to_stderr_only(
        self, tmp_entity_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify prints the key-not-found error to stderr, leaving
        stdout empty (GH #371)."""
        result = ast_modify(str(tmp_entity_file), "NonExistent", "value")
        captured = capsys.readouterr()
        assert result == 1
        assert captured.out == ""
        assert "not found" in captured.err.lower()

    def test_modify_file_not_found(
        self, nonexistent_file: Path, capsys: pytest.CaptureFixture
    ) -> None:
        """ast_modify returns exit code 2 for missing file."""
        result = ast_modify(str(nonexistent_file), "Status", "done")
        assert result == 2

# Modified from geekatron/jerry v0.31.9; see NOTICE.
