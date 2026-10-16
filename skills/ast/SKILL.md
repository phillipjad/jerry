---
name: ast
description: Structured operations on Jerry markdown through the jerry ast CLI. It parses a file to a JSON AST, reads and modifies the blockquote frontmatter of worktracker entity files, and validates navigation tables (H-23) and entity schemas. Use when the user asks to read or extract frontmatter, entity metadata or status, change one frontmatter field such as an entity's status, parse markdown structure, validate an entity file against its schema, or check a file's navigation table. Required for worktracker entity operations (H-33). Not for plain reads or free-form edits (use Read, Write or Edit), or content quality review (use adversary).
version: "1.1.0"
allowed-tools: Read, Write, Edit, Bash
activation-keywords:
  - "/ast"
  - "/jerry:ast"
  - "parse markdown"
  - "query frontmatter"
  - "modify frontmatter"
  - "validate markdown"
  - "validate nav table"

---

# AST Skill

> **Version:** 1.1.0
> **Framework:** Jerry Framework v0.9.0
> **Layer:** CLI adapter (single entry point to domain layer)

---

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | What this skill does and why |
| [When to Use This Skill](#when-to-use-this-skill) | Triggers and use cases |
| [Operations Reference](#operations-reference) | All available CLI commands |
| [Quick Reference](#quick-reference) | Copy-paste examples for common tasks |
| [Routing Disambiguation](#routing-disambiguation) | When this skill is the wrong choice |
| [Constitutional Compliance](#constitutional-compliance) | Principle mapping with consequences |
| [Architecture Notes](#architecture-notes) | Layer compliance and design |

---

## Overview

The AST skill provides structured markdown operations for Claude agents working
within the Jerry Framework. All operations are exposed via the `jerry ast` CLI
namespace, which is the single adapter between agents and the markdown AST code.

### Core Capabilities

- **Parse:** Tokenize a markdown file and return AST structure as JSON.
- **Frontmatter:** Extract `> **Key:** Value` fields as a JSON object.
- **Modify:** Change a frontmatter field value and write back to disk.
- **Validate:** Check nav table compliance (H-23/H-24) and entity schema validation.

---

## When to Use This Skill

Invoke `/ast` when you need to:

- Read frontmatter fields from a Jerry entity file (story, task, enabler, bug).
- Modify a single frontmatter field without disturbing the rest of the file.
- Validate that a markdown file complies with H-23 (nav table required) and H-24 (anchor links).

NEVER invoke this skill when:
- Reading raw file content without structural parsing -- Consequence: AST parsing overhead applied to simple file reads wastes CLI invocation cost; JSON output format adds unnecessary complexity for content retrieval; use Read tool directly
- Writing arbitrary content to files -- Consequence: AST modify is scoped to frontmatter field updates only; arbitrary content writes fail or produce incorrect results; use Write/Edit tools directly

See [Routing Disambiguation](#routing-disambiguation) for full exclusion conditions with consequences.

---

## Operations Reference

Run every operation through the plugin's project; `uv run --project` keeps your current directory:

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ast <command> [args]
```

File paths may be absolute or relative to the current directory.

### jerry ast parse

```bash
jerry ast parse <file>
```

Parse a markdown file and output the full AST as JSON (tokens + tree).

**Exit codes:** 0 success, 2 file error.

---

### jerry ast frontmatter

```bash
jerry ast frontmatter <file>
```

Extract all blockquote frontmatter fields as a JSON object.

**Output:** `{"Type": "story", "Status": "pending", ...}` or `{}` if no frontmatter.

**Exit codes:** 0 success, 2 file error.

---

### jerry ast modify

```bash
jerry ast modify <file> --key <KEY> --value <VALUE>
```

Modify one frontmatter field and write the updated content back to disk.

**Output:** `{"file": "...", "key": "...", "value": "...", "status": "modified"}`

**Exit codes:** 0 success, 1 key not found, 2 file error.

---

### jerry ast validate

```bash
jerry ast validate <file> [--schema <type>] [--nav]
```

Validate file structure against H-23/H-24 nav table rules and optionally
against an entity schema.

**Without `--schema`:** Returns JSON with nav table validation results.

**With `--schema <type>`:** Validates against entity schema (epic, feature,
story, enabler, task, bug). Returns JSON with both nav table and schema results.

**With `--nav`:** Includes detailed nav table entries in the output
(section_name, anchor, description, line_number).

**Output JSON keys:**

| Key | Type | Description |
|-----|------|-------------|
| `is_valid` | bool | True only when nav and schema are both valid |
| `nav_table_valid` | bool | True if nav table exists and covers all ## headings |
| `missing_nav_entries` | list | Heading texts absent from nav table |
| `orphaned_nav_entries` | list | Nav entries with no matching heading |
| `schema_valid` | bool | True when schema passes or no schema provided |
| `violations` | list | Violation dicts (with --schema only) |
| `nav_entries` | list | Detailed entries (with --nav only) |

**Exit codes:** 0 success, 1 validation failure (with `--schema` only), 2 file error or unknown schema type.

---

## Quick Reference

### Read frontmatter from a story file

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ast frontmatter "{project_dir}"/work/EPIC-001-example/FEAT-001-example/ST-005-example/ST-005-example.md
```

### Update story status

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ast modify "{project_dir}"/work/EPIC-001-example/FEAT-001-example/ST-005-example/ST-005-example.md --key Status --value in-progress
```

### Validate a rule file for H-23/H-24 compliance

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ast validate --nav "${CLAUDE_PLUGIN_ROOT}"/.context/rules/quality-enforcement.md
```

### Parse a file and inspect its structure

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ast parse "${CLAUDE_PLUGIN_ROOT}"/.context/rules/quality-enforcement.md
```

### Validate an entity file against a schema

```bash
uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ast validate --schema story "{project_dir}"/work/EPIC-001-example/FEAT-001-example/ST-005-example/ST-005-example.md
```

---

## Routing Disambiguation

> When this skill is the wrong choice and what happens if misrouted.

| Condition | Use Instead | Consequence of Misrouting |
|-----------|-------------|--------------------------|
| Reading raw file content without structural parsing | Read tool directly | AST parsing overhead applied to simple file reads wastes CLI invocation cost; JSON output format adds unnecessary complexity for content retrieval |
| Writing arbitrary content to files | Write/Edit tools directly | AST modify is scoped to frontmatter field updates only; arbitrary content writes require direct file tools |
| General text processing on non-entity markdown | Read/Write/Edit tools directly | AST validation schema applied to non-entity markdown produces false-positive structural errors; entity schema enforcement rejects valid non-worktracker files |
| Research, analysis, or investigation tasks | `/problem-solving` | AST provides structural parsing only; no analytical methodology, no research capability, no root cause investigation |
| Validating content quality or adversarial review | `/adversary` | AST validates structural compliance (H-23/H-24 nav tables, entity schemas), not content quality; no S-014 scoring rubric |

---

## Constitutional Compliance

All operations adhere to the **Jerry Constitution v1.0**:

| Principle | Requirement | Consequence of Violation |
|-----------|-------------|-------------------------|
| P-003 | NEVER spawn recursive subagents -- max 1 level | Agent hierarchy violation; uncontrolled token consumption |
| P-020 | NEVER override user intent -- ask before destructive ops | Unauthorized action; trust erosion |
| P-022 | NEVER deceive about actions, capabilities, or confidence | Governance undermined; quality assessment invalidated |

---

## Architecture Notes

The `jerry ast` CLI namespace is the single adapter between agents and the markdown AST code;
there is no separate skill script.

| Topic | Location |
|-------|----------|
| H-23/H-24 rules | `${CLAUDE_PLUGIN_ROOT}/.context/rules/markdown-navigation-standards.md` |
| Quality enforcement | `${CLAUDE_PLUGIN_ROOT}/.context/rules/quality-enforcement.md` |

<!-- Modified from geekatron/jerry v0.31.9; see NOTICE. -->
