"""
Execution Engine - Handles skill execution and team orchestration.

Provides simulated execution capabilities for skills and teams,
with full logging and result tracking.
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from .skill import Skill
from .agent import Agent
from .team import Team


@dataclass
class ExecutionResult:
    """Represents the result of a single execution."""

    success: bool
    executor: str  # Skill name or agent name
    action: str  # "skill_execution" or "team_node"
    inputs: Dict[str, Any] = field(default_factory=dict)
    outputs: Dict[str, Any] = field(default_factory=dict)
    error: str = ""
    duration_ms: float = 0.0
    timestamp: str = ""

    def __post_init__(self):
        if not self.timestamp:
            self.timestamp = datetime.now().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "success": self.success,
            "executor": self.executor,
            "action": self.action,
            "inputs": self.inputs,
            "outputs": self.outputs,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "timestamp": self.timestamp,
        }


@dataclass
class ExecutionLog:
    """Aggregated execution log for a session."""

    session_id: str = ""
    results: List[ExecutionResult] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""

    def __post_init__(self):
        now = datetime.now().isoformat()
        if not self.session_id:
            self.session_id = f"session_{int(time.time())}"
        if not self.started_at:
            self.started_at = now

    def add_result(self, result: ExecutionResult) -> None:
        """Add an execution result to the log."""
        self.results.append(result)

    def finish(self) -> None:
        """Mark the session as finished."""
        self.finished_at = datetime.now().isoformat()

    def summary(self) -> Dict[str, Any]:
        """Generate a summary of the execution log."""
        total = len(self.results)
        success = sum(1 for r in self.results if r.success)
        failed = total - success
        total_duration = sum(r.duration_ms for r in self.results)
        return {
            "session_id": self.session_id,
            "total_executions": total,
            "successful": success,
            "failed": failed,
            "total_duration_ms": round(total_duration, 2),
            "started_at": self.started_at,
            "finished_at": self.finished_at,
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON."""
        data = {
            "session_id": self.session_id,
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "results": [r.to_dict() for r in self.results],
        }
        return json.dumps(data, indent=indent, ensure_ascii=False)


class SkillExecutor:
    """Executes individual skills with simulated execution.

    In a real environment, this would connect to an LLM API.
    For now, it simulates execution and records inputs/outputs.
    """

    def __init__(self):
        """Initialize the skill executor."""
        self._log = ExecutionLog()

    @property
    def log(self) -> ExecutionLog:
        """Get the execution log."""
        return self._log

    def execute(self, skill: Skill, inputs: Optional[Dict[str, Any]] = None) -> ExecutionResult:
        """Execute a skill with given inputs.

        Args:
            skill: The Skill to execute.
            inputs: Dictionary of input values keyed by parameter name.

        Returns:
            ExecutionResult with outputs and metadata.
        """
        inputs = inputs or {}
        start_time = time.time()

        # Validate required parameters
        missing = []
        for param in skill.parameters:
            if param.required and param.name not in inputs:
                if param.default is None:
                    missing.append(param.name)

        if missing:
            result = ExecutionResult(
                success=False,
                executor=skill.name,
                action="skill_execution",
                inputs=inputs,
                error=f"Missing required parameters: {', '.join(missing)}",
            )
            result.duration_ms = (time.time() - start_time) * 1000
            self._log.add_result(result)
            return result

        # Simulate execution
        try:
            # Build simulated outputs based on skill output definitions
            outputs = {}
            for out_def in skill.outputs:
                outputs[out_def.name] = self._simulate_output(out_def, skill, inputs)

            # Add a generic result
            outputs["result"] = f"[Simulated] Executed skill '{skill.name}' with inputs: {list(inputs.keys())}"

            elapsed = (time.time() - start_time) * 1000
            result = ExecutionResult(
                success=True,
                executor=skill.name,
                action="skill_execution",
                inputs=inputs,
                outputs=outputs,
                duration_ms=round(elapsed, 2),
            )
            self._log.add_result(result)
            return result

        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            result = ExecutionResult(
                success=False,
                executor=skill.name,
                action="skill_execution",
                inputs=inputs,
                error=str(e),
                duration_ms=round(elapsed, 2),
            )
            self._log.add_result(result)
            return result

    def _simulate_output(self, output_def, skill: Skill, inputs: Dict[str, Any]) -> Any:
        """Generate a simulated output value based on output type."""
        type_map = {
            "string": f"[Simulated output for '{output_def.name}']",
            "integer": 0,
            "number": 0.0,
            "boolean": True,
            "array": [],
            "object": {},
            "file": "simulated_output.txt",
        }
        return type_map.get(output_def.type, "")

    def reset_log(self) -> None:
        """Reset the execution log."""
        self._log = ExecutionLog()


class TeamExecutor:
    """Executes team orchestration following the DAG structure.

    Executes agents in topological order, passing context between nodes.
    """

    def __init__(self, agents: Optional[Dict[str, Agent]] = None,
                 skill_executor: Optional[SkillExecutor] = None):
        """Initialize the team executor.

        Args:
            agents: Dictionary of Agent objects keyed by name.
            skill_executor: Optional SkillExecutor for skill execution.
        """
        self._agents = agents or {}
        self._skill_executor = skill_executor or SkillExecutor()
        self._log = ExecutionLog()

    @property
    def log(self) -> ExecutionLog:
        """Get the execution log."""
        return self._log

    def register_agent(self, agent: Agent) -> None:
        """Register an agent for team execution."""
        self._agents[agent.name] = agent

    def execute(self, team: Team, initial_context: Optional[Dict[str, Any]] = None) -> ExecutionLog:
        """Execute a team orchestration.

        Args:
            team: The Team to execute.
            initial_context: Initial context data passed to all nodes.

        Returns:
            ExecutionLog with all execution results.
        """
        self._log = ExecutionLog()
        context = dict(team.global_context)
        if initial_context:
            context.update(initial_context)

        # Validate team
        errors = team.validate()
        if errors:
            result = ExecutionResult(
                success=False,
                executor=team.name,
                action="team_execution",
                error=f"Team validation failed: {'; '.join(errors)}",
            )
            self._log.add_result(result)
            self._log.finish()
            return self._log

        # Get execution order
        try:
            order = team.topological_sort()
        except ValueError as e:
            result = ExecutionResult(
                success=False,
                executor=team.name,
                action="team_execution",
                error=str(e),
            )
            self._log.add_result(result)
            self._log.finish()
            return self._log

        # Execute each node in order
        for agent_name in order:
            node = team.get_node(agent_name)
            if not node:
                continue

            # Check condition
            if node.condition and not self._evaluate_condition(node.condition, context):
                continue

            # Execute the agent's skills
            agent = self._agents.get(agent_name)
            if agent and agent.skills:
                for skill_name in agent.skills:
                    # Simulate skill execution with context
                    result = ExecutionResult(
                        success=True,
                        executor=agent_name,
                        action="team_node",
                        inputs={"context": context, "skill": skill_name},
                        outputs={
                            "message": f"[Simulated] Agent '{agent_name}' executed skill '{skill_name}'",
                            "context_update": {},
                        },
                    )
                    self._log.add_result(result)
            else:
                # Agent has no skills, just log node execution
                result = ExecutionResult(
                    success=True,
                    executor=agent_name,
                    action="team_node",
                    inputs={"context": context},
                    outputs={
                        "message": f"[Simulated] Agent '{agent_name}' executed (no skills)",
                    },
                )
                self._log.add_result(result)

        self._log.finish()
        return self._log

    def _evaluate_condition(self, condition: str, context: Dict[str, Any]) -> bool:
        """Evaluate a simple condition expression against context.

        Supports basic conditions like:
        - "status == success"
        - "count > 0"
        - "has_data"
        """
        try:
            # Simple key existence check
            if condition in context:
                return bool(context[condition])

            # Simple equality check
            if "==" in condition:
                key, value = condition.split("==", 1)
                key = key.strip()
                value = value.strip()
                return str(context.get(key, "")) == value

            # Simple comparison
            if ">" in condition:
                key, value = condition.split(">", 1)
                key = key.strip()
                value = value.strip()
                try:
                    return float(context.get(key, 0)) > float(value)
                except (ValueError, TypeError):
                    return False

            return True
        except Exception:
            return True

    def reset_log(self) -> None:
        """Reset the execution log."""
        self._log = ExecutionLog()
