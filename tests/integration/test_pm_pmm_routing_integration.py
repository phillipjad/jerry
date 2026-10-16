# SPDX-License-Identifier: Apache-2.0
# Copyright (c) 2026 Adam Nowak

"""
Integration tests for PM/PMM skill routing and cross-agent data flow.

Validates that:
    - The trigger map in mandatory-skill-usage.md correctly routes pm-pmm keywords
    - Negative keywords suppress false-positive routing
    - Non-pm-pmm prompts do NOT route to /pm-pmm
    - Cross-agent data flow paths are structurally sound
    - Plugin.json registration includes all 5 pm-pmm agents

Test naming follows BDD convention:
    test_{scenario}_when_{condition}_then_{expected}

References:
    - EN-018: PM/PMM Skill Deployment
    - agent-routing-standards.md: Layered routing architecture, anti-pattern catalog
    - mandatory-skill-usage.md: Trigger map (5-column format)
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

# Repository root
REPO_ROOT = Path(__file__).resolve().parents[2]


# ---------------------------------------------------------------------------
# Trigger Map Parser
# ---------------------------------------------------------------------------


def _parse_trigger_map(content: str) -> list[dict[str, str]]:
    """Parse the 5-column trigger map from mandatory-skill-usage.md.

    Args:
        content: Full text of mandatory-skill-usage.md.

    Returns:
        List of dicts with keys: keywords, negative, priority, compound, skill.
    """
    rows: list[dict[str, str]] = []
    in_table = False

    for line in content.splitlines():
        stripped = line.strip()

        # Detect table header row
        if (
            "Detected Keywords" in stripped
            and "Negative Keywords" in stripped
            and "Skill" in stripped
        ):
            in_table = True
            continue

        # Skip separator row
        if in_table and re.match(r"^\|[-\s|]+\|$", stripped):
            continue

        # Parse data rows
        if in_table and stripped.startswith("|") and stripped.endswith("|"):
            cells = [c.strip() for c in stripped.split("|")[1:-1]]
            if len(cells) >= 5:
                rows.append(
                    {
                        "keywords": cells[0],
                        "negative": cells[1],
                        "priority": cells[2],
                        "compound": cells[3],
                        "skill": cells[4],
                    }
                )
            else:
                # End of table (e.g., disambiguation note)
                continue

        # End of table on empty line or non-table content
        if in_table and not stripped.startswith("|") and stripped:
            if not stripped.startswith(">"):
                in_table = False

    return rows


def _keywords_match(request_text: str, keyword_str: str) -> list[str]:
    """Check which keywords from a comma-separated string match the request.

    Args:
        request_text: The user request text (lowercased).
        keyword_str: Comma-separated keywords from trigger map.

    Returns:
        List of matched keywords.
    """
    matched = []
    keywords = [k.strip().lower() for k in keyword_str.split(",")]

    for kw in keywords:
        if not kw or kw == "--":
            continue
        # Check for keyword presence in request text
        if kw in request_text:
            matched.append(kw)

    return matched


def _route_request(request_text: str, trigger_map: list[dict[str, str]]) -> list[dict[str, object]]:
    """Route a request through the trigger map using Layer 1 algorithm.

    Implements Step 1 (positive/negative filtering) and Step 3 (priority ordering)
    from agent-routing-standards.md.

    Args:
        request_text: The user request.
        trigger_map: Parsed trigger map rows.

    Returns:
        List of candidate skills sorted by priority (ascending).
    """
    request_lower = request_text.lower()
    candidates = []

    for row in trigger_map:
        positive_matches = _keywords_match(request_lower, row["keywords"])
        negative_matches = _keywords_match(request_lower, row["negative"])

        if positive_matches and not negative_matches:
            candidates.append(
                {
                    "skill": row["skill"],
                    "priority": int(row["priority"]),
                    "positive_matches": positive_matches,
                    "match_count": len(positive_matches),
                }
            )

    # Sort by priority ascending (1 = highest priority)
    candidates.sort(key=lambda c: c["priority"])
    return candidates


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture(scope="module")
def trigger_map() -> list[dict[str, str]]:
    """Parse the trigger map from mandatory-skill-usage.md."""
    path = REPO_ROOT / ".context" / "rules" / "mandatory-skill-usage.md"
    content = path.read_text(encoding="utf-8")
    rows = _parse_trigger_map(content)
    assert len(rows) >= 8, f"Expected at least 8 trigger map rows, got {len(rows)}"
    return rows


@pytest.fixture(scope="module")
def pm_pmm_row(trigger_map: list[dict[str, str]]) -> dict[str, str]:
    """Extract the /pm-pmm row from the trigger map."""
    pm_rows = [r for r in trigger_map if r["skill"].strip() == "`/pm-pmm`"]
    assert len(pm_rows) == 1, f"Expected exactly 1 /pm-pmm row, got {len(pm_rows)}"
    return pm_rows[0]


# ---------------------------------------------------------------------------
# Test: Trigger Map Structure
# ---------------------------------------------------------------------------


class TestTriggerMapStructure:
    """Verify the pm-pmm trigger map entry is correctly configured."""

    def test_pm_pmm_row_exists_in_trigger_map(self, trigger_map: list[dict[str, str]]) -> None:
        """The trigger map contains a /pm-pmm entry."""
        skills = [r["skill"].strip() for r in trigger_map]
        assert "`/pm-pmm`" in skills

    def test_pm_pmm_has_positive_keywords(self, pm_pmm_row: dict[str, str]) -> None:
        """pm-pmm has sufficient positive keywords (RT-M-002: min 3)."""
        keywords = [k.strip() for k in pm_pmm_row["keywords"].split(",") if k.strip()]
        assert len(keywords) >= 3, f"Only {len(keywords)} keywords; RT-M-002 requires >= 3"

    def test_pm_pmm_has_negative_keywords(self, pm_pmm_row: dict[str, str]) -> None:
        """pm-pmm has negative keywords (RT-M-001: required for > 5 keywords)."""
        negative = pm_pmm_row["negative"].strip()
        assert negative and negative != "--", "pm-pmm should have negative keywords"

    def test_pm_pmm_has_compound_triggers(self, pm_pmm_row: dict[str, str]) -> None:
        """pm-pmm has compound triggers for disambiguation."""
        compound = pm_pmm_row["compound"].strip()
        assert compound and compound != "--", "pm-pmm should have compound triggers"

    def test_pm_pmm_priority_is_reasonable(self, pm_pmm_row: dict[str, str]) -> None:
        """pm-pmm priority is between /ast and /eng-team."""
        priority = int(pm_pmm_row["priority"])
        assert 8 <= priority <= 10, f"Expected priority 8-10, got {priority}"


# ---------------------------------------------------------------------------
# Test: Positive Routing (pm-pmm keywords correctly match)
# ---------------------------------------------------------------------------


class TestPositiveRouting:
    """Verify pm-pmm keywords correctly route to /pm-pmm."""

    @pytest.mark.parametrize(
        "request_text",
        [
            "Create a PRD for the self-service onboarding feature",
            "Build personas for our SaaS product customers",
            "Help me with market sizing and TAM analysis",
            "Create a competitive analysis using Porter's Five Forces",
            "Design a go-to-market plan for our developer platform",
            "Write a business case with NPV analysis",
            "Create battle cards for our top competitors",
            "Create a journey map for enterprise onboarding",
            "Help me prioritize features using RICE scoring",
            "Create Dunford positioning for our product launch",
            "Analyze win/loss patterns from Q1 sales data",
            "Calculate unit economics and LTV/CAC ratios",
            "Build a product vision using Playing to Win",
            "Create an MRD for the APAC market expansion",
            "Run Van Westendorp pricing analysis for enterprise tier",
        ],
        ids=[
            "prd",
            "personas",
            "market-sizing",
            "competitive-analysis",
            "gtm-plan",
            "business-case",
            "battle-cards",
            "journey-map",
            "rice-prioritization",
            "positioning",
            "win-loss",
            "unit-economics",
            "product-vision",
            "mrd",
            "van-westendorp",
        ],
    )
    def test_positive_keyword_when_pm_request_then_routes_to_pm_pmm(
        self, request_text: str, trigger_map: list[dict[str, str]]
    ) -> None:
        """PM/PMM domain requests route to /pm-pmm."""
        candidates = _route_request(request_text, trigger_map)
        matched_skills = [c["skill"] for c in candidates]
        assert "`/pm-pmm`" in matched_skills, (
            f"Request '{request_text}' did not route to /pm-pmm. Candidates: {matched_skills}"
        )


# ---------------------------------------------------------------------------
# Test: Negative Routing (non-pm-pmm requests do NOT match)
# ---------------------------------------------------------------------------


class TestNegativeRouting:
    """Verify non-pm-pmm requests do NOT false-positive to /pm-pmm."""

    @pytest.mark.parametrize(
        "request_text",
        [
            "Debug the authentication bug in the login flow",
            "Review the code in src/handlers/auth.py",
            "Fix the deployment pipeline CI/CD configuration",
            "Run the test suite and check test coverage",
            "Create an ADR for the persistence architecture",
            "Parse this meeting transcript and extract action items",
            "Run adversarial quality review on this deliverable",
            "Set up infrastructure pricing for our cloud deployment",
            "Implement the new user registration endpoint",
            "Perform a penetration test on the API endpoints",
        ],
        ids=[
            "debug-auth",
            "code-review",
            "cicd",
            "test-coverage",
            "architecture-adr",
            "transcript",
            "adversarial",
            "infra-pricing",
            "implementation",
            "pentest",
        ],
    )
    def test_negative_keyword_when_non_pm_request_then_no_pm_pmm_route(
        self, request_text: str, trigger_map: list[dict[str, str]]
    ) -> None:
        """Non-PM/PMM domain requests do NOT route to /pm-pmm."""
        candidates = _route_request(request_text, trigger_map)
        pm_candidates = [c for c in candidates if c["skill"] == "`/pm-pmm`"]
        assert len(pm_candidates) == 0, (
            f"Request '{request_text}' false-positived to /pm-pmm. "
            f"Matched keywords: {pm_candidates[0]['positive_matches'] if pm_candidates else []}"
        )


# ---------------------------------------------------------------------------
# Test: Negative Keyword Suppression
# ---------------------------------------------------------------------------


class TestNegativeKeywordSuppression:
    """Verify negative keywords correctly suppress pm-pmm matching."""

    @pytest.mark.parametrize(
        "request_text,suppressing_keyword",
        [
            ("Review the product pricing architecture and ADR", "architecture"),
            ("Test the pricing model implementation for coverage", "testing"),
            ("Run adversarial review on the product strategy document", "adversarial"),
            ("Parse the product strategy transcript from VTT", "transcript"),
            ("Engineering implementation of the product roadmap feature", "engineering"),
        ],
        ids=[
            "architecture-suppresses",
            "testing-suppresses",
            "adversarial-suppresses",
            "transcript-suppresses",
            "engineering-suppresses",
        ],
    )
    def test_suppression_when_mixed_keywords_then_negative_wins(
        self,
        request_text: str,
        suppressing_keyword: str,
        trigger_map: list[dict[str, str]],
    ) -> None:
        """Negative keywords suppress pm-pmm even when positive keywords present."""
        candidates = _route_request(request_text, trigger_map)
        pm_candidates = [c for c in candidates if c["skill"] == "`/pm-pmm`"]
        assert len(pm_candidates) == 0, (
            f"Request '{request_text}' should be suppressed by '{suppressing_keyword}' "
            f"but matched: {pm_candidates[0]['positive_matches'] if pm_candidates else []}"
        )


# ---------------------------------------------------------------------------
# Test: Cross-Agent Data Flow
# ---------------------------------------------------------------------------


class TestCrossAgentDataFlow:
    """Verify cross-agent data flow paths are structurally sound."""

    def test_skill_md_defines_cross_agent_data_flow(self) -> None:
        """SKILL.md contains a cross-agent data flow table."""
        skill_path = REPO_ROOT / "skills" / "pm-pmm" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        assert "Cross-Agent Data Flow" in content
        assert "pm-customer-insight" in content
        assert "pm-product-strategist" in content

    def test_customer_insight_to_product_strategist_flow_defined(self) -> None:
        """The persona -> PRD data flow path is documented."""
        skill_path = REPO_ROOT / "skills" / "pm-pmm" / "SKILL.md"
        content = skill_path.read_text(encoding="utf-8")
        # Verify the from/to flow is documented
        assert "pm-customer-insight" in content
        assert "pm-product-strategist" in content
        assert "Persona" in content or "persona" in content

    def test_all_agents_are_workers_not_orchestrators(self) -> None:
        """All 5 pm-pmm agents are workers (no Task tool in frontmatter)."""
        agents_dir = REPO_ROOT / "skills" / "pm-pmm" / "agents"
        for agent_file in sorted(agents_dir.glob("*.md")):
            content = agent_file.read_text(encoding="utf-8")
            # Extract YAML frontmatter
            if content.startswith("---"):
                end = content.index("---", 3)
                frontmatter = content[3:end]
                # tools line should NOT contain Task
                for line in frontmatter.splitlines():
                    if line.strip().startswith("tools:"):
                        assert "Task" not in line, (
                            f"Agent {agent_file.name} has Task tool — "
                            f"violates P-003 (workers must not delegate)"
                        )

    def test_agent_count_is_five(self) -> None:
        """Exactly 5 pm-pmm agent definition files exist."""
        agents_dir = REPO_ROOT / "skills" / "pm-pmm" / "agents"
        agent_files = sorted(agents_dir.glob("*.md"))
        assert len(agent_files) == 5, (
            f"Expected 5 agents, found {len(agent_files)}: {[f.name for f in agent_files]}"
        )

    def test_governance_yaml_exists_for_each_agent(self) -> None:
        """Each agent has a companion .governance.yaml file."""
        agents_dir = REPO_ROOT / "skills" / "pm-pmm" / "agents"
        agent_files = sorted(agents_dir.glob("*.md"))
        for agent_file in agent_files:
            governance = agent_file.with_suffix(".governance.yaml")
            assert governance.exists(), (
                f"Missing governance YAML for {agent_file.name}: expected {governance.name}"
            )


# ---------------------------------------------------------------------------
# Test: Plugin Registration
# ---------------------------------------------------------------------------


class TestPluginRegistration:
    """Verify pm-pmm agents are registered in plugin.json."""

    def test_plugin_json_contains_all_pm_pmm_agents(self) -> None:
        """All 5 pm-pmm agents are listed in .claude-plugin/plugin.json."""
        plugin_path = REPO_ROOT / ".claude-plugin" / "plugin.json"
        if not plugin_path.exists():
            pytest.skip("plugin.json not found")

        data = json.loads(plugin_path.read_text(encoding="utf-8"))
        agents = data.get("agents", [])

        expected = [
            "./skills/pm-pmm/agents/pm-business-analyst.md",
            "./skills/pm-pmm/agents/pm-competitive-analyst.md",
            "./skills/pm-pmm/agents/pm-customer-insight.md",
            "./skills/pm-pmm/agents/pm-market-strategist.md",
            "./skills/pm-pmm/agents/pm-product-strategist.md",
        ]

        for agent_path in expected:
            assert agent_path in agents, f"Agent {agent_path} not found in plugin.json agents array"

    def test_claude_md_contains_pm_pmm_skill(self) -> None:
        """CLAUDE.md skills table includes /pm-pmm."""
        claude_md = REPO_ROOT / "CLAUDE.md"
        content = claude_md.read_text(encoding="utf-8")
        assert "/pm-pmm" in content, "CLAUDE.md missing /pm-pmm skill entry"


# ---------------------------------------------------------------------------
# Test: Template Coverage
# ---------------------------------------------------------------------------


class TestTemplateCoverage:
    """Verify templates exist for all artifact types."""

    def test_template_count_matches_artifact_count(self) -> None:
        """15 templates exist matching 15 artifacts in the ownership matrix."""
        templates_dir = REPO_ROOT / "skills" / "pm-pmm" / "templates"
        if not templates_dir.exists():
            pytest.skip("Templates directory not found")

        templates = sorted(templates_dir.glob("*.template.md"))
        assert len(templates) == 15, (
            f"Expected 15 templates, found {len(templates)}: {[t.name for t in templates]}"
        )
