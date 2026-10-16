# Upstream

This repository is an independent derivative of the Jerry Framework
(https://github.com/geekatron/jerry), licensed under the Apache License, Version 2.0. It is not
affiliated with or endorsed by the upstream project.

- Imported from tag `v0.31.9`, commit `4aff242854ebb1bc74208991901b88c559be5a19`.
- Not imported: `projects/` and `skills/.graveyard/`.
- `upstream-manifest.txt` lists every imported upstream file with its git blob SHA at that tag.
  A file whose content no longer matches its entry has been modified in this repository and
  carries a notice saying so, as section 4(b) of the licence requires.

## Modified files without comment syntax

These files cannot carry an in-file notice, so this list is their notice: each has been
modified from geekatron/jerry v0.31.9.

- `.claude-plugin/plugin.json`
- `hooks/hooks.json`
- `uv.lock`

## Moved files

These upstream files now live at a new path. Each one that changed carries the in-file notice.

- `src/domain/markdown_ast/__init__.py` -> `src/jerry/markdown_ast/__init__.py`
- `src/domain/markdown_ast/jerry_document.py` -> `src/jerry/markdown_ast/jerry_document.py`
- `src/domain/markdown_ast/frontmatter.py` -> `src/jerry/markdown_ast/frontmatter.py`
- `src/domain/markdown_ast/nav_table.py` -> `src/jerry/markdown_ast/nav_table.py`
- `src/domain/markdown_ast/schema.py` -> `src/jerry/markdown_ast/schema.py`
- `src/domain/markdown_ast/schema_definitions.py` -> `src/jerry/markdown_ast/schema_definitions.py`
- `src/domain/markdown_ast/schema_registry.py` -> `src/jerry/markdown_ast/schema_registry.py`
- `src/interface/cli/ast_commands.py` -> `src/jerry/ast_cli.py`
- `tests/unit/domain/markdown_ast/test_jerry_document.py` -> `tests/markdown_ast/test_jerry_document.py`
- `tests/unit/domain/markdown_ast/test_frontmatter.py` -> `tests/markdown_ast/test_frontmatter.py`
- `tests/unit/domain/markdown_ast/test_nav_table.py` -> `tests/markdown_ast/test_nav_table.py`
- `tests/unit/domain/markdown_ast/test_schema.py` -> `tests/markdown_ast/test_schema.py`
- `tests/unit/domain/markdown_ast/test_schema_registry.py` -> `tests/markdown_ast/test_schema_registry.py`
- `tests/unit/interface/cli/test_ast_commands.py` -> `tests/test_ast_cli.py`
