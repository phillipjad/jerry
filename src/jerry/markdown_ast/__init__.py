# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
markdown_ast - Markdown AST operations used by the `jerry ast` commands.

Provides the JerryDocument facade for markdown parsing, querying,
transforming and rendering, plus BlockquoteFrontmatter, navigation table
helpers and the schema validation engine.

Exports:
    JerryDocument: Unified facade for markdown AST operations
    FrontmatterField: Dataclass for a single frontmatter key-value field
    BlockquoteFrontmatter: Collection class for Jerry blockquote frontmatter
    extract_frontmatter: Convenience function to extract frontmatter
    NavEntry: Frozen dataclass for one navigation table row
    NavValidationResult: Result of nav table validation
    extract_nav_table: Parse the first navigation table
    validate_nav_table: Validate navigation table compliance
    heading_to_anchor: Convert heading text to anchor slug
    FieldRule: Rule for a single frontmatter field
    SectionRule: Rule for a required section heading
    EntitySchema: Schema definition for an entity type
    ValidationViolation: A single schema violation
    ValidationReport: Complete validation report
    validate_document: Validate a JerryDocument against an EntitySchema
    get_entity_schema: Look up a built-in schema by entity type name
    EPIC_SCHEMA through BUG_SCHEMA: Built-in worktracker schemas
    SchemaRegistry: Schema registry with freeze support
"""

from jerry.markdown_ast.frontmatter import (
    BlockquoteFrontmatter,
    FrontmatterField,
    extract_frontmatter,
)
from jerry.markdown_ast.jerry_document import JerryDocument
from jerry.markdown_ast.nav_table import (
    NavEntry,
    NavValidationResult,
    extract_nav_table,
    heading_to_anchor,
    validate_nav_table,
)
from jerry.markdown_ast.schema import (
    BUG_SCHEMA,
    ENABLER_SCHEMA,
    EPIC_SCHEMA,
    FEATURE_SCHEMA,
    STORY_SCHEMA,
    TASK_SCHEMA,
    EntitySchema,
    FieldRule,
    SectionRule,
    ValidationReport,
    ValidationViolation,
    get_entity_schema,
    validate_document,
)
from jerry.markdown_ast.schema_registry import SchemaRegistry

__all__ = [
    "JerryDocument",
    "BlockquoteFrontmatter",
    "FrontmatterField",
    "extract_frontmatter",
    "NavEntry",
    "NavValidationResult",
    "extract_nav_table",
    "heading_to_anchor",
    "validate_nav_table",
    "FieldRule",
    "SectionRule",
    "EntitySchema",
    "ValidationViolation",
    "ValidationReport",
    "validate_document",
    "get_entity_schema",
    "EPIC_SCHEMA",
    "FEATURE_SCHEMA",
    "STORY_SCHEMA",
    "ENABLER_SCHEMA",
    "TASK_SCHEMA",
    "BUG_SCHEMA",
    "SchemaRegistry",
]

# Modified from geekatron/jerry v0.31.9; see NOTICE.
