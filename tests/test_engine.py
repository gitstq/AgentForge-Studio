"""
Tests for the Execution Engine.

Tests SkillExecutor and TeamExecutor for simulated execution,
logging, and result tracking.
"""

import pytest

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agentforge.core.skill import Skill
from agentforge.core.agent import Agent
from agentforge.core.team import Team
from agentforge.core.engine import SkillExecutor, TeamExecutor, ExecutionResult, ExecutionLog


class TestExecutionResult:
    """Tests for ExecutionResult class."""

    def test_create_result(self):
        """Test basic result creation."""
        result = ExecutionResult(
            success=True,
            executor="test-skill",
            action="skill_execution",
            inputs={"key": "value"},
            outputs={"result": "ok"},
        )
        assert result.success is True
        assert result.executor == "test-skill"
        assert result.timestamp != ""

    def test_result_to_dict(self):
        """Test result serialization."""
        result = ExecutionResult(
            success=False,
            executor="x",
            action="test",
            error="Something went wrong",
            duration_ms=42.5,
        )
        d = result.to_dict()
        assert d["success"] is False
        assert d["error"] == "Something went wrong"
        assert d["duration_ms"] == 42.5


class TestExecutionLog:
    """Tests for ExecutionLog class."""

    def test_create_log(self):
        """Test log creation."""
        log = ExecutionLog()
        assert log.session_id != ""
        assert log.started_at != ""
        assert log.results == []

    def test_add_result(self):
        """Test adding results to log."""
        log = ExecutionLog()
        result = ExecutionResult(success=True, executor="x", action="test")
        log.add_result(result)
        assert len(log.results) == 1

    def test_summary(self):
        """Test log summary generation."""
        log = ExecutionLog()
        log.add_result(ExecutionResult(success=True, executor="a", action="test"))
        log.add_result(ExecutionResult(success=True, executor="b", action="test"))
        log.add_result(ExecutionResult(success=False, executor="c", action="test", error="fail"))
        log.finish()

        summary = log.summary()
        assert summary["total_executions"] == 3
        assert summary["successful"] == 2
        assert summary["failed"] == 1
        assert summary["finished_at"] != ""

    def test_to_json(self):
        """Test JSON serialization of log."""
        log = ExecutionLog()
        log.add_result(ExecutionResult(success=True, executor="x", action="test"))
        log.finish()
        json_str = log.to_json()
        assert "session_id" in json_str
        assert "results" in json_str


class TestSkillExecutor:
    """Tests for SkillExecutor class."""

    def _make_skill(self) -> Skill:
        """Helper to create a test skill."""
        skill = Skill(
            name="test-skill",
            description="A test skill",
            instructions="Test instructions",
        )
        skill.add_parameter("input_text", "string", True, description="Input text")
        skill.add_parameter("count", "integer", False, default=1)
        skill.add_output("result", "string", "The result")
        skill.add_output("score", "integer", "Score value")
        return skill

    def test_execute_success(self):
        """Test successful skill execution."""
        executor = SkillExecutor()
        skill = self._make_skill()

        result = executor.execute(skill, {"input_text": "hello"})
        assert result.success is True
        assert result.executor == "test-skill"
        assert "result" in result.outputs
        assert "score" in result.outputs
        assert result.duration_ms >= 0

    def test_execute_missing_required_param(self):
        """Test execution fails with missing required parameter."""
        executor = SkillExecutor()
        skill = self._make_skill()

        result = executor.execute(skill, {})
        assert result.success is False
        assert "Missing" in result.error

    def test_execute_with_optional_param(self):
        """Test execution with optional parameter."""
        executor = SkillExecutor()
        skill = self._make_skill()

        result = executor.execute(skill, {"input_text": "hello", "count": 5})
        assert result.success is True

    def test_execution_logged(self):
        """Test that execution is logged."""
        executor = SkillExecutor()
        skill = self._make_skill()

        executor.execute(skill, {"input_text": "hello"})
        assert len(executor.log.results) == 1

    def test_reset_log(self):
        """Test log reset."""
        executor = SkillExecutor()
        skill = self._make_skill()

        executor.execute(skill, {"input_text": "hello"})
        executor.reset_log()
        assert len(executor.log.results) == 0


class TestTeamExecutor:
    """Tests for TeamExecutor class."""

    def _make_team(self) -> Team:
        """Helper to create a test team."""
        team = Team(name="test-team", description="Test team")
        team.add_node("planner")
        team.add_node("developer", depends_on=["planner"])
        team.add_node("tester", depends_on=["developer"])
        return team

    def _make_agents(self) -> dict:
        """Helper to create test agents."""
        agents = {}
        planner = Agent(name="planner", role="Planner")
        planner.assign_skill("req-analyst")
        agents["planner"] = planner

        developer = Agent(name="developer", role="Developer")
        developer.assign_skill("code-generator")
        agents["developer"] = developer

        tester = Agent(name="tester", role="Tester")
        tester.assign_skill("test-generator")
        agents["tester"] = tester

        return agents

    def test_execute_team(self):
        """Test successful team execution."""
        team = self._make_team()
        agents = self._make_agents()

        executor = TeamExecutor(agents=agents)
        log = executor.execute(team)

        assert log.finished_at != ""
        assert len(log.results) == 3
        assert all(r.success for r in log.results)

    def test_execute_team_with_context(self):
        """Test team execution with initial context."""
        team = self._make_team()
        agents = self._make_agents()

        executor = TeamExecutor(agents=agents)
        log = executor.execute(team, initial_context={"project": "test-project"})

        summary = log.summary()
        assert summary["total_executions"] == 3

    def test_execute_empty_team(self):
        """Test execution of empty team."""
        team = Team(name="empty")
        executor = TeamExecutor()
        log = executor.execute(team)

        assert len(log.results) == 0

    def test_execute_team_invalid(self):
        """Test execution of invalid team."""
        team = Team(name="")  # Invalid name
        executor = TeamExecutor()
        log = executor.execute(team)

        assert any(not r.success for r in log.results)

    def test_register_agent(self):
        """Test agent registration."""
        executor = TeamExecutor()
        agent = Agent(name="test", role="Tester")
        executor.register_agent(agent)
        # Agent is now available for execution

    def test_condition_evaluation_true(self):
        """Test condition evaluation returns True for matching condition."""
        executor = TeamExecutor()
        result = executor._evaluate_condition("status", {"status": "success"})
        assert result is True

    def test_condition_evaluation_false(self):
        """Test condition evaluation returns False for non-matching."""
        executor = TeamExecutor()
        result = executor._evaluate_condition("status == failure", {"status": "success"})
        assert result is False

    def test_condition_evaluation_comparison(self):
        """Test condition evaluation with comparison."""
        executor = TeamExecutor()
        result = executor._evaluate_condition("count > 5", {"count": 10})
        assert result is True

    def test_condition_evaluation_missing_key(self):
        """Test condition evaluation with missing key returns True (pass-through)."""
        executor = TeamExecutor()
        result = executor._evaluate_condition("nonexistent", {})
        assert result is True  # Missing keys pass through

    def test_reset_log(self):
        """Test log reset."""
        executor = TeamExecutor()
        team = self._make_team()
        agents = self._make_agents()

        executor.execute(team)
        executor.reset_log()
        assert len(executor.log.results) == 0
