"""
Tests for the Agent data model.

Tests agent creation, serialization, validation, and skill management.
"""

import json
import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agentforge.core.agent import Agent


class TestAgent:
    """Tests for Agent class."""

    def _make_agent(self, **kwargs) -> Agent:
        """Helper to create a basic agent with defaults."""
        defaults = {
            "name": "test-agent",
            "role": "Software Developer",
            "system_prompt": "You are an expert developer.",
        }
        defaults.update(kwargs)
        return Agent(**defaults)

    def test_create_agent(self):
        """Test basic agent creation."""
        agent = self._make_agent()
        assert agent.name == "test-agent"
        assert agent.role == "Software Developer"
        assert agent.system_prompt == "You are an expert developer."
        assert agent.model == "default"
        assert agent.temperature == 0.7
        assert agent.skills == []
        assert agent.created_at != ""

    def test_agent_to_dict(self):
        """Test agent serialization to dictionary."""
        agent = self._make_agent()
        agent.assign_skill("code-review")
        d = agent.to_dict()
        assert d["name"] == "test-agent"
        assert d["role"] == "Software Developer"
        assert "code-review" in d["skills"]

    def test_agent_from_dict(self):
        """Test agent deserialization from dictionary."""
        data = {
            "name": "from-dict",
            "role": "Data Analyst",
            "system_prompt": "Analyze data.",
            "skills": ["data-analyst", "summarizer"],
            "model": "gpt-4",
            "temperature": 0.5,
            "tags": ["analytics"],
        }
        agent = Agent.from_dict(data)
        assert agent.name == "from-dict"
        assert agent.role == "Data Analyst"
        assert agent.skills == ["data-analyst", "summarizer"]
        assert agent.model == "gpt-4"
        assert agent.temperature == 0.5
        assert agent.tags == ["analytics"]

    def test_agent_to_json(self):
        """Test JSON serialization."""
        agent = self._make_agent()
        json_str = agent.to_json()
        parsed = json.loads(json_str)
        assert parsed["name"] == "test-agent"

    def test_agent_from_json(self):
        """Test JSON deserialization."""
        agent = self._make_agent()
        json_str = agent.to_json()
        restored = Agent.from_json(json_str)
        assert restored.name == agent.name
        assert restored.role == agent.role

    def test_agent_validate_valid(self):
        """Test validation of a valid agent."""
        agent = self._make_agent()
        errors = agent.validate()
        assert errors == []

    def test_agent_validate_missing_name(self):
        """Test validation detects missing name."""
        agent = Agent(name="", role="Developer")
        errors = agent.validate()
        assert any("name" in e for e in errors)

    def test_agent_validate_missing_role(self):
        """Test validation detects missing role."""
        agent = Agent(name="x", role="")
        errors = agent.validate()
        assert any("role" in e for e in errors)

    def test_agent_validate_temperature_out_of_range(self):
        """Test validation rejects out-of-range temperature."""
        agent = Agent(name="x", role="Dev", temperature=3.0)
        errors = agent.validate()
        assert any("Temperature" in e for e in errors)

    def test_assign_skill(self):
        """Test assigning a skill to agent."""
        agent = self._make_agent()
        agent.assign_skill("code-review")
        assert "code-review" in agent.skills

    def test_assign_duplicate_skill(self):
        """Test that duplicate skill assignment is ignored."""
        agent = self._make_agent()
        agent.assign_skill("code-review")
        agent.assign_skill("code-review")
        assert agent.skills.count("code-review") == 1

    def test_remove_skill(self):
        """Test removing a skill from agent."""
        agent = self._make_agent()
        agent.assign_skill("code-review")
        result = agent.remove_skill("code-review")
        assert result is True
        assert "code-review" not in agent.skills

    def test_remove_nonexistent_skill(self):
        """Test removing a non-existent skill returns False."""
        agent = self._make_agent()
        result = agent.remove_skill("nonexistent")
        assert result is False

    def test_has_skill(self):
        """Test checking if agent has a skill."""
        agent = self._make_agent()
        agent.assign_skill("code-review")
        assert agent.has_skill("code-review") is True
        assert agent.has_skill("nonexistent") is False

    def test_json_roundtrip(self):
        """Test full JSON roundtrip."""
        agent = self._make_agent()
        agent.assign_skill("skill-a")
        agent.assign_skill("skill-b")
        agent.tags = ["dev", "review"]

        json_str = agent.to_json()
        restored = Agent.from_json(json_str)

        assert restored.name == agent.name
        assert restored.role == agent.role
        assert restored.skills == ["skill-a", "skill-b"]
        assert restored.model == agent.model
        assert restored.temperature == agent.temperature
        assert restored.tags == ["dev", "review"]
