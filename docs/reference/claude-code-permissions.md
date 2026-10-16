# Claude Code Permission Syntax Reference

> Specification of Claude Code permission syntax, settings file format, evaluation semantics, and Jerry-specific configuration findings.

<!-- Quality criteria: skills/diataxis/rules/diataxis-standards.md Section 1 (R-01 through R-07) -->
<!-- Anti-patterns to avoid: RAP-01 (marketing claims), RAP-02 (instructions/recipes), RAP-03 (narrative explanation) -->
<!-- Voice: Neutral, precise, austere. No opinions, no superlatives. See Section 5. -->

## Document Sections

| Section | Purpose |
|---------|---------|
| [Overview](#overview) | Scope, rule structure, and canonical sources |
| [Settings File Format](#settings-file-format) | JSON schema, field names, and file locations |
| [Evaluation Order](#evaluation-order) | deny > ask > allow precedence and first-match semantics |
| [Settings File Scope and Precedence](#settings-file-scope-and-precedence) | Five-level hierarchy from managed to user scope |
| [MCP Tool Permissions](#mcp-tool-permissions) | `mcp__server-name__tool_name` pattern syntax |
| [Skill Permissions](#skill-permissions) | `Skill(name)` pattern syntax |
| [Bash Command Permissions](#bash-command-permissions) | `Bash(command pattern)` syntax and word-boundary behavior |
| [File Access Permissions](#file-access-permissions) | Read, Write, Edit path patterns and glob wildcards |
| [Jerry Configuration Findings](#jerry-configuration-findings) | Unverified fields and patterns in Jerry's committed settings |

---

## Overview

Claude Code enforces tool and resource access through a permission system declared in JSON settings files. Each permission entry is a string that identifies a tool or resource pattern. Permissions reside in three arrays within the `permissions` object: `allow`, `deny`, and `ask`.

The JSON schema for Claude Code settings is published at `https://json.schemastore.org/claude-code-settings.json`.

> Source: [Claude Code Settings](https://code.claude.com/docs/en/settings)

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions)

---

## Settings File Format

Claude Code settings files use JSON. The canonical `permissions` object contains three arrays: `allow`, `deny`, and `ask`. Each array contains permission strings as defined in this document.

### Documented field names

| Field | Type | Purpose |
|-------|------|---------|
| `permissions.allow` | array of strings | Tools and resources permitted without user approval |
| `permissions.deny` | array of strings | Tools and resources unconditionally blocked |
| `permissions.ask` | array of strings | Tools and resources that require user approval before each use |

**Example (canonical format):**

```json
{
  "permissions": {
    "allow": ["mcp__memory-keeper__*", "Bash(git status *)"],
    "deny": ["Bash(rm *)"],
    "ask": ["Bash(git push *)"]
  }
}
```

> Source: [Claude Code Settings](https://code.claude.com/docs/en/settings)

### FINDING-001: Undocumented field names in Jerry's committed settings

Jerry's `.claude/settings.json` uses `permissions.allowed_tools` and `permissions.require_approval`. These field names do not appear in the Claude Code official documentation. The documented field names are `permissions.allow`, `permissions.deny`, and `permissions.ask`.

| Observed field | Documented equivalent | Status |
|----------------|-----------------------|--------|
| `permissions.allowed_tools` | `permissions.allow` | UNVERIFIED — may be legacy, undocumented, or silently ignored |
| `permissions.require_approval` | `permissions.ask` | UNVERIFIED — may be legacy, undocumented, or silently ignored |

**Required action:** Validate both field names against the JSON schema at `https://json.schemastore.org/claude-code-settings.json`. Determine whether Claude Code parses, ignores, or errors on unrecognized field names.

> Source: [Claude Code Settings](https://code.claude.com/docs/en/settings) — documented fields are `allow`, `deny`, `ask`

---

## Evaluation Order

Claude Code resolves each permission check using the sequence: `deny` > `ask` > `allow`. The first matching rule in the highest-precedence array determines the outcome.

| Precedence | Array | Outcome |
|------------|-------|---------|
| 1 (highest) | `deny` | Access denied unconditionally |
| 2 | `ask` | Claude pauses and requests user approval |
| 3 (lowest) | `allow` | Access granted without interruption |

**Deny is absolute.** When a tool matches a `deny` entry, no `allow` entry at any scope overrides the denial.

**First match wins.** Within a single array, evaluation stops at the first matching entry.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "Rules are evaluated in order: deny -> ask -> allow. The first matching rule wins, so deny rules always take precedence." and "If a tool is denied at any level, no other level can allow it."

---

## Settings File Scope and Precedence

Claude Code loads settings from up to five locations. Higher-precedence scopes win on scalar field conflicts. Permission arrays (`allow`, `deny`, `ask`) are merged across all scopes; deny rules win regardless of originating scope.

| Precedence | Scope name | File path | Committed to version control |
|------------|------------|-----------|------------------------------|
| 1 (highest) | Managed | Controlled by deployment tooling | N/A |
| 2 | Command line | Flags passed to `claude` invocation | N/A (session only) |
| 3 | Local project | `.claude/settings.local.json` | No (gitignored) |
| 4 | Shared project | `.claude/settings.json` | Yes |
| 5 (lowest) | User | `~/.claude/settings.json` | No |

Both `.claude/settings.json` and `.claude/settings.local.json` use the same JSON format. The only differences between them are scope, precedence position, and whether the file is committed to version control.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — Settings precedence section

---

## MCP Tool Permissions

MCP tool permission strings identify tools provided by Model Context Protocol servers. The string format encodes the server name and, optionally, a specific tool name.

### `mcp__server-name`

**Type:** string
**Scope:** All tools from the named server

Matches all tools exposed by `server-name`. Functionally equivalent to `mcp__server-name__*`.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "mcp__puppeteer matches any tool provided by the puppeteer server"

**Example:**

```json
"allow": ["mcp__memory-keeper"]
```

### `mcp__server-name__*`

**Type:** string
**Scope:** All tools from the named server
**Wildcard:** `*` matches any tool name

Explicit wildcard form. Functionally identical to the bare `mcp__server-name` form.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "mcp__puppeteer__* wildcard syntax that also matches all tools from the puppeteer server"

**Example:**

```json
"allow": ["mcp__memory-keeper__*", "mcp__context7__*"]
```

### `mcp__server-name__tool_name`

**Type:** string
**Scope:** Single named tool from the named server

Matches exactly the tool identified by `tool_name` on `server-name`. The tool name component uses the MCP server's own tool identifier.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions)

**Example:**

```json
"allow": [
  "mcp__context7__resolve-library-id",
  "mcp__context7__query-docs"
]
```

---

## Skill Permissions

Skill permission strings control access to Claude Code skills. The `Skill()` syntax accepts a name argument identifying the target skill.

### `Skill(name)`

**Type:** string
**Scope:** Exact match against the skill's registered name
**Case-sensitive:** Yes

Matches the skill whose registered name equals `name` exactly.

> Source: [Claude Code Skills](https://code.claude.com/docs/en/skills) — direct quote: "Permission syntax: Skill(name) for exact match, Skill(name *) for prefix match with any arguments."

**Example:**

```json
"allow": ["Skill(worktracker)", "Skill(problem-solving)"]
```

### `Skill(name *)`

**Type:** string
**Scope:** Skills whose invocation begins with `name ` (name, then space, then `*`)
**Wildcard:** `*` matches any arguments passed after the prefix space

The space before `*` is required. This form matches skill invocations where the name matches and additional arguments follow.

> Source: [Claude Code Skills](https://code.claude.com/docs/en/skills) — direct quote: "Permission syntax: Skill(name) for exact match, Skill(name *) for prefix match with any arguments."

**Example:**

```json
"allow": ["Skill(jerry *)"]
```

### `Skill` (bare, in deny array)

**Type:** string
**Scope:** All skills

When placed in a `deny` array without parentheses, denies all skill invocations. No `Skill(*)` wildcard form is documented in the Claude Code permission specification.

> Source: [Claude Code Skills](https://code.claude.com/docs/en/skills)

**Example:**

```json
"deny": ["Skill"]
```

### Plugin skill namespace

Plugin skills use a `plugin-name:skill-name` namespace. This namespace prevents naming conflicts with other skill levels.

> Source: [Claude Code Skills](https://code.claude.com/docs/en/skills) — direct quote: "Plugin skills use a plugin-name:skill-name namespace, so they cannot conflict with other levels."

### FINDING-002: Colon-namespaced Skill permission form

Jerry's `.claude/settings.local.json` contains entries of the form `Skill(jerry:skill-name)`. The documented `Skill()` permission syntax specifies `Skill(name)` and `Skill(name *)`. The colon-namespaced form `Skill(jerry:name)` does not appear as a documented permission pattern.

| Observed form | Documentation basis | Status |
|---------------|---------------------|--------|
| `Skill(jerry:adversary)` | Plugin skill namespace documented for skill identity, not confirmed as permission pattern | UNVERIFIED |
| `Skill(adversary)` | Matches documented `Skill(name)` pattern | Documented |

**Required action:** Test whether `Skill(jerry:adversary)` entries in `allow` produce different behavior from `Skill(adversary)` entries alone. Determine whether removing the colon-namespaced form breaks skill invocation approval.

> Source: [Claude Code Skills](https://code.claude.com/docs/en/skills)

### FINDING-003: Skills with no permission entries

Of the 16 registered Jerry skills, 9 have no entries in the `allow` array of `.claude/settings.local.json`.

| Skills with entries | Skills without entries |
|---------------------|------------------------|
| adversary, nasa-se, problem-solving, orchestration, transcript, worktracker, prompt-engineering | architecture, ast, diataxis, eng-team, pm-pmm, red-team, saucer-boy, saucer-boy-framework-voice, user-experience |

Per the Claude Code documentation, skills operate by default unless denied. The effect of the absence of `allow` entries — whether it triggers approval prompts or auto-approves — is untested for these 9 skills.

**Required action:** Determine whether explicit `Skill()` entries in `allow` are required to suppress approval prompts for skills that have no `deny` entry.

> Source: [Claude Code Skills](https://code.claude.com/docs/en/skills)

---

## Bash Command Permissions

Bash permission strings control which shell commands Claude Code may execute. The `Bash()` syntax accepts a pattern argument matched against the full command string.

### `Bash` or `Bash(*)`

**Type:** string
**Scope:** All shell commands

Grants or denies all Bash execution. The bare `Bash` and `Bash(*)` forms are equivalent.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions)

**Example:**

```json
"allow": ["Bash"]
```

### `Bash(command *)` — prefix match with word boundary

**Type:** string
**Scope:** Commands whose text begins with the stated prefix followed by a space

The space before `*` constitutes a word boundary. The pattern matches only when the literal prefix is followed by at least one space before additional characters.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "The space before * matters: Bash(ls *) matches ls -la but not lsof, while Bash(ls*) matches both."

**Example:**

```json
"allow": ["Bash(npm run *)"]
```

`Bash(ls *)` matches `ls -la` but does not match `lsof` or `lsblk`.

### `Bash(command*)` — prefix match without word boundary

**Type:** string
**Scope:** Commands whose text begins with the stated prefix as a bare substring

Without a space before `*`, the pattern matches any command text starting with the literal prefix, including commands whose names extend the prefix without a separator.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "The space before * matters: Bash(ls *) matches ls -la but not lsof, while Bash(ls*) matches both."

**Example:**

```json
"allow": ["Bash(ls*)"]
```

`Bash(ls*)` matches `ls -la`, `lsof`, and `lsblk`.

### Argument-constraining patterns

The Claude Code documentation warns that Bash permission patterns intended to constrain which arguments are accepted are fragile and may not behave as expected across all invocation forms.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "Bash permission patterns that try to constrain command arguments are fragile"

### Deprecated `:*` suffix syntax

The `:*` suffix (e.g., `Bash(echo:*)`) is a legacy form. The documented replacement is a space before `*` (e.g., `Bash(echo *)`).

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — direct quote: "The legacy :* suffix syntax is equivalent to * but is deprecated."

### FINDING-004: Deprecated `:*` syntax in Jerry settings

Jerry's `.claude/settings.local.json` contains multiple entries using the deprecated `:*` form, for example `Bash(echo:*)`, `Bash(ls:*)`, `Bash(find:*)`, and all `Bash(git ...:*)` entries.

| Status | Description |
|--------|-------------|
| DEPRECATED | All `Bash(command:*)` entries use the deprecated `:*` suffix form |

**Required action:** Migrate all `Bash(command:*)` entries to `Bash(command *)` (space before `*`) per the documented replacement syntax.

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions)

---

## File Access Permissions

File access permission strings apply to the `Read`, `Write`, and `Edit` tool permissions. They accept gitignore-style glob patterns.

### Path type prefixes

| Prefix | Interpretation |
|--------|----------------|
| `//` | Absolute path from the filesystem root |
| `~/` | Path relative to the user's home directory |
| `/` | Path relative to the project root |
| `./` or bare name | Path relative to the current working directory |

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions) — Read and Edit section

### Glob wildcards

| Pattern | Matches |
|---------|---------|
| `*` | Any filename characters within a single directory level; does not cross directory boundaries |
| `**` | Any path segment including directory separators; crosses directory boundaries recursively |

> Source: [Claude Code Permissions](https://code.claude.com/docs/en/permissions)

**Example:**

```json
"allow": [
  "Read(/src/**/*.py)",
  "Write(./.claude/settings.local.json)"
]
```

`Read(/src/**/*.py)` matches any `.py` file at any depth under `src/`. `Read(/src/*.py)` matches only `.py` files directly inside `src/`.

---

## Jerry Configuration Findings

This section consolidates all FINDING entries from the sections above, cross-referenced for navigation.

| ID | Location | Issue | Status | Action |
|----|----------|-------|--------|--------|
| FINDING-001 | `.claude/settings.json` | `permissions.allowed_tools` and `permissions.require_approval` are not documented field names; documented names are `allow`, `deny`, `ask` | UNVERIFIED | Validate against JSON schema at `https://json.schemastore.org/claude-code-settings.json` |
| FINDING-002 | `.claude/settings.local.json` | `Skill(jerry:name)` colon-namespaced form is not documented as a permission pattern | UNVERIFIED | Test whether removing colon-namespaced entries changes approval behavior |
| FINDING-003 | `.claude/settings.local.json` | 9 of 16 registered skills have no `allow` entries; approval behavior for these skills is untested | UNTESTED | Determine whether absent `allow` entries trigger approval prompts |
| FINDING-004 | `.claude/settings.local.json` | All `Bash(command:*)` entries use the deprecated `:*` suffix form | DEPRECATED | Migrate to `Bash(command *)` (space before `*`) |

---

## Related

- **Explanation:** [About Claude Code permission scopes and merge behavior](../design/) — Design rationale and architectural context
- **How-To Guide:** [How to add a new skill permission to Jerry settings](../../.context/) — Task-oriented configuration instructions
