# /architect Command

Forces creation of a PLAN.md file before implementation begins.

---

## Usage

```
/architect <task description>
```

## Prerequisites

**Focused Project Required**: The plan is written into the session's primary focused project, `{project_dir}`.

If no project is focused, ask the user to pick one (`focus set <id>`) or create one (`projects new <slug>`, which
also focuses it). Run either through `uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry`; the SessionStart context gives
the exact command.

## Behavior

When invoked, this command:

1. **Verifies the focused project** that `{project_dir}` names
2. **Creates/updates PLAN.md** in `{project_dir}/PLAN.md`
3. **Analyzes the task** for scope, complexity, and risks
4. **Identifies alternatives** and documents trade-offs
5. **Defines implementation steps** with dependencies
6. **Sets success criteria** for validation
7. **Waits for approval** before proceeding

---

## PLAN File Template

Create the following structure:

```markdown
# PLAN: $ARGUMENTS

**ID**: PLAN-{YYYYMMDD}-{slug}
**Status**: DRAFT
**Author**: Claude (Orchestrator)
**Created**: {current date}
**Work Items**: {to be created}

## Problem Statement

{Analyze the task description and articulate:}
- What problem are we solving?
- Why does this need to be solved now?
- What constraints exist?

## Current State Analysis

{Before proposing solutions, understand:}
- What exists today?
- What are the relevant files/components?
- What are the dependencies?

## Proposed Solution

{High-level approach with rationale}

## Alternatives Considered

| Option | Pros | Cons | Decision |
|--------|------|------|----------|
| A: ... | ... | ... | ... |
| B: ... | ... | ... | **Selected** / Rejected |

## Implementation Steps

1. [ ] Step 1: {description}
   - Files: {affected files}
   - Dependencies: {what must be done first}

2. [ ] Step 2: {description}
   - Files: {affected files}
   - Dependencies: {what must be done first}

## Risks & Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| ... | Low/Med/High | Low/Med/High | ... |

## Success Criteria

- [ ] Criterion 1: {measurable outcome}
- [ ] Criterion 2: {measurable outcome}

## Open Questions

- [ ] Question 1: {needs clarification}

## References

- {Relevant documentation}
- {Prior art / examples}
```

---

## Post-Creation Actions

After creating the PLAN:

1. **Display the PLAN** to the user
2. **Ask for approval**: "Does this plan look correct? Should I proceed?"
3. **Wait for explicit approval** before implementation
4. **Create Work Items** in Work Tracker upon approval

---

## Example

```
User: /architect Add a caching layer for database queries

Claude: I'll create an architecture plan for adding a caching layer.

Focused project: PROJ-002 (projects/PROJ-002-caching)

[Creates projects/PROJ-002-caching/PLAN.md]

Here's the proposed plan:
- Problem: Database queries are slow for repeated reads
- Solution: Add in-memory LRU cache with TTL
- Steps: 1) Define cache port, 2) Implement adapter, 3) Integrate with repository
- Risks: Cache invalidation complexity, memory pressure

Does this plan look correct? Should I proceed with implementation?

User: Yes, proceed.

Claude: [Updates WORKTRACKER.md, begins implementation]
```

## Example (No Project Set)

```
User: /architect Add authentication

Claude: No project is focused, and this plan needs one.

1. Pick a project from the list in the session context
2. Or create a new one (`projects new <slug>`)

Which project should this plan belong to?
```

<!-- Modified from geekatron/jerry v0.31.9; see NOTICE. -->
