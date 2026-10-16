# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Command-line entry point: `jerry <namespace> <command> ...`."""

from __future__ import annotations

import argparse
import sys

from jerry import ast_cli


def build_parser() -> argparse.ArgumentParser:
    """Build the argument parser for every namespace and command."""
    parser = argparse.ArgumentParser(prog="jerry", description="Project-based work for Claude Code.")
    namespaces = parser.add_subparsers(dest="namespace", required=True)

    ast = namespaces.add_parser("ast", help="Markdown AST operations.")
    commands = ast.add_subparsers(dest="command", required=True)

    parse = commands.add_parser("parse", help="Print the token list and AST of a markdown file as JSON.")
    parse.add_argument("file")

    frontmatter = commands.add_parser("frontmatter", help="Print blockquote frontmatter fields as JSON.")
    frontmatter.add_argument("file")

    validate = commands.add_parser("validate", help="Validate navigation and, optionally, an entity schema.")
    validate.add_argument("file")
    validate.add_argument("--schema", help="Entity type: epic, feature, story, enabler, task or bug.")
    validate.add_argument("--nav", action="store_true", help="Include the parsed navigation table entries.")

    modify = commands.add_parser("modify", help="Set a frontmatter field and write the file back.")
    modify.add_argument("file")
    modify.add_argument("--key", required=True)
    modify.add_argument("--value", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run one command and return its exit code."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    if args.command == "parse":
        return ast_cli.ast_parse(args.file)
    if args.command == "frontmatter":
        return ast_cli.ast_frontmatter(args.file)
    if args.command == "validate":
        return ast_cli.ast_validate(args.file, schema=args.schema, nav=args.nav)
    return ast_cli.ast_modify(args.file, args.key, args.value)
