"""
Tests for the Team data model and DAG orchestration.

Tests team creation, DAG validation, topological sorting, and visualization.
"""

import json
import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agentforge.core.team import Team, TeamNode


class TestTeamNode:
    """Tests for TeamNode class."""

    def test_create_node(self):
        """Test basic node creation."""
        node = TeamNode(agent_name="agent-a", depends_on=["agent-b"])
        assert node.agent_name == "agent-a"
        assert node.depends_on == ["agent-b"]
        assert node.condition == ""

    def test_node_to_dict(self):
        """Test node serialization."""
        node = TeamNode(agent_name="a", depends_on=["b"], condition="status == ok")
        d = node.to_dict()
        assert d["agent_name"] == "a"
        assert d["depends_on"] == ["b"]
        assert d["condition"] == "status == ok"

    def test_node_from_dict(self):
        """Test node deserialization."""
        data = {"agent_name": "x", "depends_on": ["y", "z"], "condition": "count > 0"}
        node = TeamNode.from_dict(data)
        assert node.agent_name == "x"
        assert node.depends_on == ["y", "z"]
        assert node.condition == "count > 0"


class TestTeam:
    """Tests for Team class."""

    def _make_team(self, **kwargs) -> Team:
        """Helper to create a basic team."""
        defaults = {
            "name": "test-team",
            "description": "A test team",
        }
        defaults.update(kwargs)
        return Team(**defaults)

    def test_create_team(self):
        """Test basic team creation."""
        team = self._make_team()
        assert team.name == "test-team"
        assert team.description == "A test team"
        assert team.nodes == []
        assert team.global_context == {}
        assert team.created_at != ""

    def test_team_to_dict(self):
        """Test team serialization."""
        team = self._make_team()
        team.add_node("agent-a")
        team.add_node("agent-b", depends_on=["agent-a"])

        d = team.to_dict()
        assert d["name"] == "test-team"
        assert len(d["nodes"]) == 2

    def test_team_from_dict(self):
        """Test team deserialization."""
        data = {
            "name": "from-dict",
            "description": "Imported team",
            "nodes": [
                {"agent_name": "a", "depends_on": []},
                {"agent_name": "b", "depends_on": ["a"], "condition": "ready"},
            ],
            "global_context": {"env": "production"},
        }
        team = Team.from_dict(data)
        assert team.name == "from-dict"
        assert len(team.nodes) == 2
        assert team.nodes[1].condition == "ready"
        assert team.global_context == {"env": "production"}

    def test_team_to_json(self):
        """Test JSON serialization."""
        team = self._make_team()
        json_str = team.to_json()
        parsed = json.loads(json_str)
        assert parsed["name"] == "test-team"

    def test_team_from_json(self):
        """Test JSON deserialization."""
        team = self._make_team()
        team.add_node("a")
        json_str = team.to_json()
        restored = Team.from_json(json_str)
        assert restored.name == team.name
        assert len(restored.nodes) == 1

    def test_validate_valid_team(self):
        """Test validation of a valid team."""
        team = self._make_team()
        team.add_node("agent-a")
        team.add_node("agent-b", depends_on=["agent-a"])
        errors = team.validate()
        assert errors == []

    def test_validate_empty_name(self):
        """Test validation detects empty name."""
        team = Team(name="")
        errors = team.validate()
        assert any("name" in e for e in errors)

    def test_validate_duplicate_agent(self):
        """Test validation detects duplicate agents."""
        team = self._make_team()
        team.add_node("agent-a")
        team.add_node("agent-a")
        errors = team.validate()
        assert any("Duplicate" in e for e in errors)

    def test_detect_cycle(self):
        """Test circular dependency detection."""
        team = self._make_team()
        team.add_node("a", depends_on=["b"])
        team.add_node("b", depends_on=["c"])
        team.add_node("c", depends_on=["a"])
        errors = team.validate()
        assert any("Circular" in e for e in errors)

    def test_topological_sort_simple(self):
        """Test topological sort with simple chain."""
        team = self._make_team()
        team.add_node("a")
        team.add_node("b", depends_on=["a"])
        team.add_node("c", depends_on=["b"])

        order = team.topological_sort()
        assert order.index("a") < order.index("b")
        assert order.index("b") < order.index("c")

    def test_topological_sort_parallel(self):
        """Test topological sort with parallel nodes."""
        team = self._make_team()
        team.add_node("a")
        team.add_node("b")
        team.add_node("c", depends_on=["a", "b"])

        order = team.topological_sort()
        assert order.index("a") < order.index("c")
        assert order.index("b") < order.index("c")

    def test_topological_sort_cycle_raises(self):
        """Test topological sort raises on cycle."""
        team = self._make_team()
        team.add_node("a", depends_on=["b"])
        team.add_node("b", depends_on=["a"])

        with pytest.raises(ValueError, match="Circular"):
            team.topological_sort()

    def test_add_node(self):
        """Test adding a node to team."""
        team = self._make_team()
        team.add_node("agent-x", depends_on=["agent-y"], condition="ready")
        assert len(team.nodes) == 1
        assert team.nodes[0].agent_name == "agent-x"
        assert team.nodes[0].depends_on == ["agent-y"]
        assert team.nodes[0].condition == "ready"

    def test_remove_node(self):
        """Test removing a node from team."""
        team = self._make_team()
        team.add_node("a")
        team.add_node("b", depends_on=["a"])
        result = team.remove_node("a")
        assert result is True
        assert len(team.nodes) == 1
        assert team.nodes[0].agent_name == "b"
        assert "a" not in team.nodes[0].depends_on

    def test_remove_nonexistent_node(self):
        """Test removing non-existent node returns False."""
        team = self._make_team()
        result = team.remove_node("nonexistent")
        assert result is False

    def test_get_node(self):
        """Test getting a node by agent name."""
        team = self._make_team()
        team.add_node("agent-a")
        node = team.get_node("agent-a")
        assert node is not None
        assert node.agent_name == "agent-a"

    def test_get_node_not_found(self):
        """Test getting non-existent node returns None."""
        team = self._make_team()
        node = team.get_node("nonexistent")
        assert node is None

    def test_visualize_ascii(self):
        """Test ASCII visualization generation."""
        team = self._make_team()
        team.add_node("planner")
        team.add_node("developer", depends_on=["planner"])
        team.add_node("tester", depends_on=["developer"])

        viz = team.visualize_ascii()
        assert "test-team" in viz
        assert "planner" in viz
        assert "developer" in viz
        assert "tester" in viz

    def test_visualize_ascii_empty(self):
        """Test ASCII visualization of empty team."""
        team = self._make_team()
        viz = team.visualize_ascii()
        assert "no nodes" in viz

    def test_json_roundtrip(self):
        """Test full JSON roundtrip."""
        team = self._make_team()
        team.add_node("a")
        team.add_node("b", depends_on=["a"])
        team.global_context = {"key": "value"}
        team.tags = ["team-tag"]  # Note: Team doesn't have tags field, testing base fields

        json_str = team.to_json()
        restored = Team.from_json(json_str)

        assert restored.name == team.name
        assert restored.description == team.description
        assert len(restored.nodes) == 2
        assert restored.global_context == {"key": "value"}
