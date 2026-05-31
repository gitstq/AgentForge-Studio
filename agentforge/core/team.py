"""
Team data model - Defines multi-agent team orchestration with DAG structure.

A Team contains multiple agents organized in a Directed Acyclic Graph (DAG)
for orchestrated execution with dependency management.
"""

import json
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class TeamNode:
    """Represents a single node in the team DAG.

    Each node maps to an agent and can have dependencies on other nodes.
    """

    agent_name: str
    depends_on: List[str] = field(default_factory=list)
    condition: str = ""  # Execution condition expression

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "agent_name": self.agent_name,
            "depends_on": list(self.depends_on),
            "condition": self.condition,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "TeamNode":
        """Create a TeamNode from a dictionary."""
        return cls(
            agent_name=data.get("agent_name", ""),
            depends_on=data.get("depends_on", []),
            condition=data.get("condition", ""),
        )


@dataclass
class Team:
    """Represents a multi-agent team with DAG-based orchestration.

    A Team organizes agents in a DAG where each node is an agent
    and edges represent execution dependencies.
    """

    name: str
    description: str = ""
    nodes: List[TeamNode] = field(default_factory=list)
    global_context: Dict[str, Any] = field(default_factory=dict)
    created_at: str = ""
    updated_at: str = ""

    def __post_init__(self):
        """Set timestamps if not provided."""
        now = datetime.now().isoformat()
        if not self.created_at:
            self.created_at = now
        if not self.updated_at:
            self.updated_at = now

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return {
            "name": self.name,
            "description": self.description,
            "nodes": [n.to_dict() for n in self.nodes],
            "global_context": self.global_context,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Team":
        """Create a Team from a dictionary."""
        nodes = [TeamNode.from_dict(n) for n in data.get("nodes", [])]
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            nodes=nodes,
            global_context=data.get("global_context", {}),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "Team":
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def validate(self) -> List[str]:
        """Validate the team definition. Returns a list of errors."""
        errors = []
        if not self.name:
            errors.append("Team name is required")

        agent_names = set()
        for node in self.nodes:
            if not node.agent_name:
                errors.append("Team node agent_name is required")
            if node.agent_name in agent_names:
                errors.append(f"Duplicate agent in team: {node.agent_name}")
            agent_names.add(node.agent_name)

        # Check for circular dependencies
        cycle = self._detect_cycle()
        if cycle:
            errors.append(f"Circular dependency detected: {' -> '.join(cycle)}")

        return errors

    def _detect_cycle(self) -> Optional[List[str]]:
        """Detect circular dependencies using DFS. Returns cycle path if found."""
        # Build adjacency list
        graph: Dict[str, List[str]] = {}
        for node in self.nodes:
            graph[node.agent_name] = list(node.depends_on)

        visited = set()
        rec_stack = set()
        path = []

        def dfs(agent: str) -> Optional[List[str]]:
            visited.add(agent)
            rec_stack.add(agent)
            path.append(agent)

            for dep in graph.get(agent, []):
                if dep not in visited:
                    result = dfs(dep)
                    if result:
                        return result
                elif dep in rec_stack:
                    # Found cycle
                    cycle_start = path.index(dep)
                    return path[cycle_start:] + [dep]

            path.pop()
            rec_stack.remove(agent)
            return None

        for node in self.nodes:
            if node.agent_name not in visited:
                result = dfs(node.agent_name)
                if result:
                    return result

        return None

    def topological_sort(self) -> List[str]:
        """Return agents in topological order (execution order).

        Raises ValueError if circular dependency is detected.
        """
        # Build adjacency list and in-degree count
        in_degree: Dict[str, int] = {}
        graph: Dict[str, List[str]] = {}

        for node in self.nodes:
            if node.agent_name not in in_degree:
                in_degree[node.agent_name] = 0
            if node.agent_name not in graph:
                graph[node.agent_name] = []
            for dep in node.depends_on:
                if dep not in graph:
                    graph[dep] = []
                graph[dep].append(node.agent_name)
                in_degree[node.agent_name] = in_degree.get(node.agent_name, 0) + 1

        # Kahn's algorithm
        queue = deque()
        for agent in in_degree:
            if in_degree[agent] == 0:
                queue.append(agent)

        result = []
        while queue:
            agent = queue.popleft()
            result.append(agent)
            for neighbor in graph.get(agent, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        if len(result) != len(self.nodes):
            raise ValueError("Circular dependency detected in team DAG")

        return result

    def add_node(self, agent_name: str, depends_on: Optional[List[str]] = None,
                 condition: str = "") -> None:
        """Add a node to the team."""
        if depends_on is None:
            depends_on = []
        self.nodes.append(TeamNode(
            agent_name=agent_name,
            depends_on=depends_on,
            condition=condition,
        ))
        self.updated_at = datetime.now().isoformat()

    def remove_node(self, agent_name: str) -> bool:
        """Remove a node from the team. Returns True if removed."""
        for i, node in enumerate(self.nodes):
            if node.agent_name == agent_name:
                self.nodes.pop(i)
                # Remove this agent from other nodes' dependencies
                for other in self.nodes:
                    if agent_name in other.depends_on:
                        other.depends_on.remove(agent_name)
                self.updated_at = datetime.now().isoformat()
                return True
        return False

    def get_node(self, agent_name: str) -> Optional[TeamNode]:
        """Get a node by agent name."""
        for node in self.nodes:
            if node.agent_name == agent_name:
                return node
        return None

    def visualize_ascii(self) -> str:
        """Generate ASCII art visualization of the team DAG."""
        if not self.nodes:
            return f"Team '{self.name}' has no nodes."

        lines = []
        lines.append(f"=== Team: {self.name} ===")
        if self.description:
            lines.append(f"Description: {self.description}")
        lines.append("")

        try:
            order = self.topological_sort()
        except ValueError:
            lines.append("WARNING: Circular dependency detected!")
            order = [n.agent_name for n in self.nodes]

        for i, agent_name in enumerate(order):
            node = self.get_node(agent_name)
            prefix = "  " * i
            connector = "+" if i == 0 else "|--"
            lines.append(f"{prefix}{connector} [{agent_name}]")
            if node and node.depends_on:
                lines.append(f"{prefix}    depends_on: {', '.join(node.depends_on)}")
            if node and node.condition:
                lines.append(f"{prefix}    condition: {node.condition}")

        return "\n".join(lines)
