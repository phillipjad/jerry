# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Implementations of the `jerry ast` subcommands.

    - ast_parse: Parse a markdown file and output the AST as JSON.
    - ast_validate: Validate a markdown file against an optional entity schema.
    - ast_frontmatter: Extract blockquote frontmatter fields as JSON.
    - ast_modify: Modify a frontmatter field and write back to file.

Helper serializers:
    - token_to_dict: Convert a markdown-it-py Token to a JSON-serializable dict.
    - node_to_dict: Convert a SyntaxTreeNode to a JSON-serializable dict.

Relative paths resolve against the caller's working directory. Files of any
location are accepted; only the size limit applies.

Exit codes:
    0 -- Success
    1 -- Validation failure (schema violations found) or modify key error
    2 -- Read error (file not found, too large, unreadable, unknown schema type)
"""

from __future__ import annotations

import json
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

from markdown_it.token import Token
from markdown_it.tree import SyntaxTreeNode

from jerry.markdown_ast import (
    JerryDocument,
    extract_frontmatter,
    extract_nav_table,
    get_entity_schema,
    validate_document,
    validate_nav_table,
)

#: Maximum file size in bytes (1 MB).
_MAX_FILE_SIZE_BYTES: int = 1_048_576


def token_to_dict(token: Token) -> dict[str, Any]:
    """Convert a markdown-it-py Token to a JSON-serializable dictionary.

    Args:
        token: A Token object produced by markdown-it-py.

    Returns:
        A dictionary with keys: type, tag, nesting, map, content.
        The ``map`` value is either a list of two ints [start, end] or None.
    """
    return {
        "type": token.type,
        "tag": token.tag,
        "nesting": token.nesting,
        "map": list(token.map) if token.map is not None else None,
        "content": token.content,
    }


def _tree_to_dict(node: SyntaxTreeNode) -> dict[str, Any]:
    """Recursively convert a SyntaxTreeNode to a JSON-serializable dictionary.

    The root node's tag, map and content attributes raise AttributeError in
    markdown-it-py, so the root uses safe defaults.

    Args:
        node: A SyntaxTreeNode from the parsed AST.

    Returns:
        A nested dictionary with keys: type, tag, map, content, children.
    """
    if node.is_root:
        return {
            "type": node.type,
            "tag": "",
            "map": None,
            "content": "",
            "children": [_tree_to_dict(child) for child in node.children],
        }

    map_raw = node.map
    map_val: list[int] | None = list(map_raw) if map_raw is not None else None

    return {
        "type": node.type,
        "tag": node.tag,
        "map": map_val,
        "content": node.content or "",
        "children": [_tree_to_dict(child) for child in node.children],
    }


def node_to_dict(node: SyntaxTreeNode) -> dict[str, Any]:
    """Convert a SyntaxTreeNode to a flat JSON-serializable dictionary.

    For compound nodes (heading, blockquote) whose own content is empty, the
    content comes from the first inline child.

    Args:
        node: A SyntaxTreeNode from the parsed AST.

    Returns:
        A dictionary with keys: type, tag, map, content.
    """
    map_raw = node.map
    map_val: list[int] | None = list(map_raw) if map_raw is not None else None
    content = node.content or ""

    if not content:
        for child in node.children:
            if child.type == "inline":
                content = child.content or ""
                break

    return {
        "type": node.type,
        "tag": node.tag,
        "map": map_val,
        "content": content,
    }


def _read_file(file_path: str) -> tuple[Path | None, str | None]:
    """Resolve and read a markdown file, enforcing the size limit.

    Args:
        file_path: Absolute path, or a path relative to the working directory.

    Returns:
        A tuple of (resolved_path, content). Both are None when the file is
        missing, too large or unreadable; the reason is printed to stderr.
    """
    resolved = Path(file_path).resolve()
    if not resolved.is_file():
        print(f"Error: File not found: {file_path}", file=sys.stderr)
        return None, None
    try:
        size = resolved.stat().st_size
        if size > _MAX_FILE_SIZE_BYTES:
            print(
                f"Error: File exceeds maximum size ({size} bytes > {_MAX_FILE_SIZE_BYTES} bytes): {file_path}",
                file=sys.stderr,
            )
            return None, None
        return resolved, resolved.read_text(encoding="utf-8-sig")
    except (OSError, UnicodeDecodeError) as exc:
        print(f"Error reading file {file_path}: {exc}", file=sys.stderr)
        return None, None


def ast_parse(file_path: str) -> int:
    """Parse a markdown file and print its token list and AST as JSON.

    Args:
        file_path: Path to the markdown file to parse.

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    _, source = _read_file(file_path)
    if source is None:
        return 2

    doc = JerryDocument.parse(source)

    output = {
        "file": file_path,
        "tokens": [token_to_dict(t) for t in doc.tokens],
        "tree": _tree_to_dict(doc.tree),
    }
    print(json.dumps(output, indent=2))
    return 0


def _nav_entries(doc: JerryDocument) -> list[dict[str, Any]]:
    return [
        {
            "section_name": e.section_name,
            "anchor": e.anchor,
            "description": e.description,
            "line_number": e.line_number,
        }
        for e in extract_nav_table(doc) or []
    ]


def ast_validate(file_path: str, schema: str | None = None, nav: bool = False) -> int:
    """Validate a markdown file against an optional entity schema.

    Without ``schema``: prints a JSON report of navigation table validation.
    With ``schema`` (one of the built-in worktracker entity types: epic,
    feature, story, enabler, task, bug): also validates frontmatter fields and
    required sections, and returns 1 if any violations are found. With
    ``nav``: includes the parsed navigation table entries.

    Args:
        file_path: Path to the markdown file to validate.
        schema: Optional entity type string (e.g., "epic", "story").
        nav: When True, include detailed nav table entries in the output.

    Returns:
        0 on success, 1 if violations are found, 2 if the file cannot be read
        or the schema type is unknown.
    """
    _, source = _read_file(file_path)
    if source is None:
        return 2

    doc = JerryDocument.parse(source)
    nav_result = validate_nav_table(doc)
    nav_report: dict[str, Any] = {
        "nav_table_valid": nav_result.is_valid,
        "missing_nav_entries": nav_result.missing_entries,
        "orphaned_nav_entries": [entry.section_name for entry in nav_result.orphaned_entries],
    }

    if schema is None:
        output: dict[str, Any] = {
            "file": file_path,
            "is_valid": nav_result.is_valid,
            **nav_report,
            "schema_valid": True,
            "schema_violations": [],
        }
        if nav:
            output["nav_entries"] = _nav_entries(doc)
        print(json.dumps(output, indent=2))
        return 0

    try:
        entity_schema = get_entity_schema(schema)
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 2

    report = validate_document(doc, entity_schema)

    output = {
        "file": file_path,
        "schema": schema,
        "entity_type": report.entity_type,
        "is_valid": report.is_valid and nav_result.is_valid,
        **nav_report,
        "schema_valid": report.is_valid,
        "field_count": report.field_count,
        "section_count": report.section_count,
        "violation_count": len(report.violations),
        "violations": [
            {
                "field_path": v.field_path,
                "expected": v.expected,
                "actual": v.actual,
                "severity": v.severity,
                "message": v.message,
            }
            for v in report.violations
        ],
    }
    if nav:
        output["nav_entries"] = _nav_entries(doc)
    print(json.dumps(output, indent=2))

    return 0 if (report.is_valid and nav_result.is_valid) else 1


def ast_frontmatter(file_path: str) -> int:
    """Print the blockquote frontmatter fields of a markdown file as JSON.

    Prints ``{}`` if no frontmatter is found.

    Args:
        file_path: Path to the markdown file.

    Returns:
        0 on success, 2 if the file cannot be read.
    """
    _, source = _read_file(file_path)
    if source is None:
        return 2

    doc = JerryDocument.parse(source)
    fm = extract_frontmatter(doc)
    print(json.dumps(dict(fm.items()), indent=2))
    return 0


def ast_modify(file_path: str, key: str, value: str) -> int:
    """Set a frontmatter field and write the file back atomically.

    The new content goes to a temporary file in the same directory, which then
    replaces the original, so a failed write never leaves a partial file.

    Args:
        file_path: Path to the markdown file.
        key: The frontmatter field name to modify (case-sensitive).
        value: The new value for the field.

    Returns:
        0 on success, 1 if the key does not exist in frontmatter, 2 if the
        file cannot be read or written.
    """
    target_path, source = _read_file(file_path)
    if target_path is None or source is None:
        return 2

    doc = JerryDocument.parse(source)
    fm = extract_frontmatter(doc)

    try:
        new_doc = fm.set(key, value)
    except KeyError:
        print(f"Error: Key '{key}' not found in frontmatter", file=sys.stderr)
        return 1

    new_content = new_doc.render()

    temp_fd = None
    temp_path_str = None
    try:
        temp_fd, temp_path_str = tempfile.mkstemp(
            dir=str(target_path.parent),
            suffix=".tmp",
            prefix=".ast_modify_",
        )
        os.write(temp_fd, new_content.encode("utf-8"))
        os.close(temp_fd)
        temp_fd = None
        os.replace(temp_path_str, str(target_path))
        temp_path_str = None
    except OSError as exc:
        print(f"Error writing file {file_path}: {exc}", file=sys.stderr)
        return 2
    finally:
        if temp_fd is not None:
            try:
                os.close(temp_fd)
            except OSError:
                pass
        if temp_path_str is not None:
            try:
                os.unlink(temp_path_str)
            except OSError:
                pass

    output = {
        "file": file_path,
        "key": key,
        "value": value,
        "status": "modified",
    }
    print(json.dumps(output, indent=2))
    return 0


# Modified from geekatron/jerry v0.31.9; see NOTICE.
