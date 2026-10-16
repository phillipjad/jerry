# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""Tests for PatternLibraryAdapter (#150).

Verifies the adapter wraps the existing PatternLibrary and
strips matched text per T-06 (information disclosure prevention).

Note: Test secrets are constructed dynamically to avoid triggering
the pre_tool_use hook's own secret detection on this source file.
"""

from __future__ import annotations

import pytest

from src.infrastructure.internal.enforcement.pattern_library_adapter import (
    PatternLibraryAdapter,
)


def _make_fake_gh_pat() -> str:
    """Build a fake GitHub PAT at runtime to avoid hook detection."""
    prefix = "ghp_"
    body = "A" * 36
    return prefix + body


def _make_fake_openai_key() -> str:
    """Build a fake OpenAI key at runtime to avoid hook detection."""
    prefix = "sk-proj-"
    body = "a" * 100
    return prefix + body


class TestPatternLibraryAdapterLoading:
    """Adapter loads patterns from the real YAML file."""

    def test_loads_patterns_from_default_path(self) -> None:
        """Adapter loads the real patterns.yaml without error."""
        adapter = PatternLibraryAdapter()
        assert adapter._library is not None

    def test_missing_path_returns_approve(self) -> None:
        """Missing patterns file results in fail-open approve."""
        from pathlib import Path

        adapter = PatternLibraryAdapter(patterns_path=Path("/nonexistent/patterns.yaml"))
        result = adapter.validate_tool_input("Write", {"content": "test"})
        assert result.decision == "approve"


class TestPatternLibraryAdapterValidation:
    """Adapter validates tool inputs and strips matched text (T-06)."""

    @pytest.fixture()
    def adapter(self) -> PatternLibraryAdapter:
        """Adapter with real patterns loaded."""
        return PatternLibraryAdapter()

    def test_detects_openai_api_key(self, adapter: PatternLibraryAdapter) -> None:
        """Secrets detection catches OpenAI API key pattern."""
        fake_key = _make_fake_openai_key()
        result = adapter.validate_tool_input(
            "Write",
            {"content": fake_key},
        )
        assert result.decision == "block"
        assert any("openai" in m.rule_id for m in result.matches)

    def test_detects_github_pat(self, adapter: PatternLibraryAdapter) -> None:
        """Secrets detection catches GitHub PAT pattern."""
        fake_pat = _make_fake_gh_pat()
        result = adapter.validate_tool_input(
            "Write",
            {"content": fake_pat},
        )
        assert result.decision == "block"
        assert any("github" in m.rule_id for m in result.matches)

    def test_clean_input_approves(self, adapter: PatternLibraryAdapter) -> None:
        """Clean input with no secrets/PII is approved."""
        result = adapter.validate_tool_input(
            "Write",
            {"content": "def hello():\n    return 'world'\n"},
        )
        assert result.decision == "approve"

    def test_t06_matched_text_not_in_result(self, adapter: PatternLibraryAdapter) -> None:
        """T-06: PatternMatch objects must not contain matched text."""
        fake_pat = _make_fake_gh_pat()
        result = adapter.validate_tool_input(
            "Write",
            {"content": fake_pat},
        )
        for match in result.matches:
            # PatternMatch should only have rule_id, description, severity
            assert not hasattr(match, "matched_text")
            assert not hasattr(match, "start_pos")
            assert not hasattr(match, "end_pos")
