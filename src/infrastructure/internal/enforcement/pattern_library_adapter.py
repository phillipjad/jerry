# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Adapter wrapping the existing PatternLibrary for SecurityEnforcementEngine.

Thin adapter that loads patterns from scripts/patterns/ and provides
pattern validation for the SecurityEnforcementEngine. Uses yaml.safe_load()
for YAML parsing.

References:
    - #150: pre_tool_use.py consolidation
    - ADR-150-001: IPatternLibrary port protocol
    - T-06: Log rule_id only, never matched text
"""

from __future__ import annotations

import logging
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class PatternMatch:
    """A single pattern match result.

    T-06: Only rule_id and description are stored — never matched text.
    """

    rule_id: str
    description: str
    severity: str


@dataclass(frozen=True)
class PatternValidationResult:
    """Result of pattern-based validation.

    Attributes:
        decision: "approve", "block", "warn", or "ask".
        reason: Aggregated reason string.
        matches: Individual pattern matches (rule_id only, per T-06).
    """

    decision: str
    reason: str
    matches: list[PatternMatch] = field(default_factory=list)


class PatternLibraryAdapter:
    """Adapter wrapping scripts/patterns/PatternLibrary.

    Loads patterns from YAML using the existing PatternLibrary class,
    and translates its ValidationResult into our PatternValidationResult.

    Fail-open: if loading fails, validate_tool_input always returns approve.

    Args:
        patterns_path: Path to patterns.yaml. If None, auto-detects.
    """

    def __init__(self, patterns_path: Path | None = None) -> None:
        self._library: Any = None
        try:
            # Add scripts/ to sys.path temporarily for import
            scripts_dir = self._find_scripts_dir(patterns_path)
            if scripts_dir and str(scripts_dir) not in sys.path:
                sys.path.insert(0, str(scripts_dir))

            from patterns.loader import load_patterns  # type: ignore[import-not-found]

            self._library = load_patterns(patterns_path)
        except Exception as exc:
            logger.warning("[PatternLibraryAdapter] Failed to load patterns: %s", exc)

    @staticmethod
    def _find_scripts_dir(patterns_path: Path | None) -> Path | None:
        """Find the scripts/ directory for import resolution."""
        if patterns_path is not None:
            # patterns_path is like .../scripts/patterns/patterns.yaml
            # scripts_dir is .../scripts/
            return patterns_path.parent.parent

        # Try to find from cwd
        cwd = Path.cwd()
        candidates = [
            cwd / "scripts",
            cwd.parent / "scripts",
        ]
        for candidate in candidates:
            if (candidate / "patterns" / "patterns.yaml").exists():
                return candidate
        return None

    def validate_tool_input(
        self,
        tool_name: str,
        tool_input: dict[str, Any],
    ) -> PatternValidationResult:
        """Validate tool input against loaded patterns.

        Args:
            tool_name: Claude Code tool name (Write, Edit, Bash, etc.)
            tool_input: Tool input parameters dict.

        Returns:
            PatternValidationResult with decision, reason, and matches.
            T-06: matches contain rule_id only, never matched text.
        """
        if self._library is None:
            return PatternValidationResult(decision="approve", reason="", matches=[])

        try:
            result = self._library.validate_input(tool_name, tool_input)

            # T-06: Strip matched text — log rule_id and description only
            safe_matches = [
                PatternMatch(
                    rule_id=m.rule_id,
                    description=m.description,
                    severity=m.severity,
                )
                for m in result.matches
            ]

            return PatternValidationResult(
                decision=result.decision,
                reason=result.reason,
                matches=safe_matches,
            )
        except Exception as exc:
            logger.warning("[PatternLibraryAdapter] Validation failed: %s", exc)
            return PatternValidationResult(decision="approve", reason="", matches=[])
