# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Phillip Miavelstuck

"""Command-line entry point: `jerry <namespace> <command> ...`."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from jerry import ast_cli, projects, session


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

    project_parser = namespaces.add_parser("projects", help="Discover and inspect projects.")
    project_commands = project_parser.add_subparsers(dest="command", required=True)

    listing = project_commands.add_parser("list", help="List discovered projects by root.")
    _add_scope(listing)

    show = project_commands.add_parser("show", help="Show one project with its links and files.")
    show.add_argument("project_id")
    _add_scope(show)

    new = project_commands.add_parser("new", help="Create the next-numbered project with a RESUME.md stub.")
    new.add_argument("slug")
    new.add_argument("--parent", help="Create a sub-project inside this project ID.")
    new.add_argument("--title", help="Project title (default: the slug).")
    _add_scope(new)

    index = project_commands.add_parser("index", help="Print each root's registry table, or update its README.md.")
    index.add_argument("--write", action="store_true", help="Rewrite the table between the README.md markers.")
    _add_scope(index)

    check = project_commands.add_parser("check", help="Validate projects, RESUME.md files and registries.")
    _add_scope(check)

    focus_parser = namespaces.add_parser("focus", help="Show or change the projects this session works on.")
    focus_commands = focus_parser.add_subparsers(dest="command", required=True)
    _add_scope(focus_commands.add_parser("show", help="Show the focus and each project's Pick up here."))
    for name, help_text in (
        ("set", "Focus on these projects; the first is primary."),
        ("add", "Add these projects to the focus."),
    ):
        command = focus_commands.add_parser(name, help=help_text)
        command.add_argument("project_ids", nargs="+", metavar="id")
        _add_scope(command)
    _add_scope(focus_commands.add_parser("none", help="Work without a project in this session."))

    return parser


def _add_scope(parser: argparse.ArgumentParser) -> None:
    parser.add_argument(
        "--root", action="append", type=Path, help="Use only this projects root (repeatable) instead of discovery."
    )
    parser.add_argument("--session", help=f"Session id (default: ${session.ENV}); its stored roots apply.")


def _discover(args: argparse.Namespace, sid: str | None) -> tuple[session.Session | None, projects.Discovery]:
    state = None if sid is None else session.load(sid) or session.start(Path.cwd())
    roots = args.root
    if roots is None and state is not None:
        roots = [Path(root) for root in state.roots]
    found = projects.discover(Path.cwd(), roots=roots)
    if args.command != "check":
        for warning in found.warnings:
            print(f"warning: {warning}", file=sys.stderr)
        for error in found.errors:
            print(f"error: {error}", file=sys.stderr)
    return state, found


def _new(found: projects.Discovery, args: argparse.Namespace) -> int:
    try:
        path = projects.new_project(found, args.slug, parent_id=args.parent, title=args.title)
    except (OSError, ValueError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(path.as_posix())
    return 0


def _index(found: projects.Discovery, write: bool) -> int:
    if not write:
        tables = [projects.render_index(found, root) for root in found.roots]
        if len(tables) > 1:
            tables = [f"{root.as_posix()}\n\n{table}" for root, table in zip(found.roots, tables)]
        print("\n".join(tables), end="")
        return 0
    code = 0
    for root in found.roots:
        readme = (root / projects.REGISTRY).as_posix()
        try:
            changed = projects.sync_registry(found, root, write=True)
            if changed is None:
                raise ValueError(f"no '{projects.INDEX_START}' and '{projects.INDEX_END}' lines")
        except (OSError, ValueError) as exc:
            print(f"error: {readme}: {exc}", file=sys.stderr)
            code = 1
            continue
        print(f"{readme}: {'updated' if changed else 'up to date'}")
    return code


def _projects(args: argparse.Namespace) -> int:
    _, found = _discover(args, session.session_id(args.session))
    if args.command == "check":
        errors, warnings = projects.check(found)
        for warning in warnings:
            print(f"warning: {warning}", file=sys.stderr)
        for error in errors:
            print(f"error: {error}", file=sys.stderr)
        print(f"{len(errors)} errors, {len(warnings)} warnings, {len(found.all_projects)} projects checked")
        return 1 if errors else 0
    if args.command == "new":
        return _new(found, args)
    if args.command == "index":
        return _index(found, args.write)
    if args.command == "list":
        print(projects.render_list(found), end="")
        return 0
    shown = projects.render_show(found, args.project_id)
    if shown is None:
        print(f"Unknown project: {args.project_id}", file=sys.stderr)
        return 1
    print(shown, end="")
    return 0


def _focus(args: argparse.Namespace) -> int:
    sid = session.session_id(args.session)
    if sid is None:
        print("error: needs a session id: pass --session or run inside Claude Code", file=sys.stderr)
        return 1
    state, found = _discover(args, sid)
    changed = session.refresh(state, found)
    if args.command in ("set", "add"):
        entries = session.focus_entries(found, args.project_ids)
        if args.command == "set":
            state.focus = entries
        else:
            focused = {entry["id"] for entry in state.focus}
            state.focus += [entry for entry in entries if entry["id"] not in focused]
        state.none = False
    elif args.command == "none":
        state.focus, state.none = [], True
    if changed or args.command != "show":
        session.save(sid, state)
    print(session.render(state, found), end="")
    return 0


def main(argv: list[str] | None = None) -> int:
    """Run one command and return its exit code."""
    for stream in (sys.stdout, sys.stderr):
        reconfigure = getattr(stream, "reconfigure", None)
        if reconfigure is not None:
            reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args(argv)
    if args.namespace in ("projects", "focus"):
        try:
            return _projects(args) if args.namespace == "projects" else _focus(args)
        except (session.SessionError, OSError) as exc:
            print(f"error: {exc}", file=sys.stderr)
            return 1
    if args.command == "parse":
        return ast_cli.ast_parse(args.file)
    if args.command == "frontmatter":
        return ast_cli.ast_frontmatter(args.file)
    if args.command == "validate":
        return ast_cli.ast_validate(args.file, schema=args.schema, nav=args.nav)
    return ast_cli.ast_modify(args.file, args.key, args.value)
