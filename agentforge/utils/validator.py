"""
Configuration validator - Validate skill, agent, and team configurations.

Provides validation utilities for all AgentForge entity types
with detailed error reporting.
"""

import re
from typing import Any, Dict, List, Tuple


class ConfigValidator:
    """Validator for AgentForge configuration entities.

    Validates skills, agents, and teams against defined rules
    and returns structured error reports.
    """

    # Valid parameter types
    VALID_PARAM_TYPES = {"string", "integer", "number", "boolean", "array", "object"}

    # Valid IO types (extends param types with file)
    VALID_IO_TYPES = {"string", "integer", "number", "boolean", "array", "object", "file"}

    # Name pattern (alphanumeric, hyphens, underscores)
    NAME_PATTERN = re.compile(r"^[a-zA-Z0-9][a-zA-Z0-9_-]*$")

    @classmethod
    def validate_skill(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a skill configuration dictionary.

        Args:
            data: Skill configuration dictionary.

        Returns:
            Tuple of (is_valid, list_of_errors).
        """
        errors = []

        # Required fields
        name = data.get("name", "")
        if not name:
            errors.append("Skill 'name' is required")
        elif not cls.NAME_PATTERN.match(name):
            errors.append(
                f"Skill name '{name}' must match pattern: alphanumeric, hyphens, underscores"
            )

        description = data.get("description", "")
        if not description:
            errors.append("Skill 'description' is required")

        instructions = data.get("instructions", "")
        if not instructions:
            errors.append("Skill 'instructions' is required")

        # Version format
        version = data.get("version", "1.0.0")
        if not cls._validate_version(version):
            errors.append(f"Invalid version format: '{version}' (expected: X.Y.Z)")

        # Parameters
        for i, param in enumerate(data.get("parameters", [])):
            param_errors = cls._validate_parameter(param, i)
            errors.extend(param_errors)

        # Check for duplicate parameter names
        param_names = [p.get("name", "") for p in data.get("parameters", [])]
        duplicates = [n for n in param_names if param_names.count(n) > 1]
        if duplicates:
            errors.append(f"Duplicate parameter names: {', '.join(set(duplicates))}")

        # Inputs
        for i, inp in enumerate(data.get("inputs", [])):
            io_errors = cls._validate_io(inp, "input", i)
            errors.extend(io_errors)

        # Outputs
        for i, out in enumerate(data.get("outputs", [])):
            io_errors = cls._validate_io(out, "output", i)
            errors.extend(io_errors)

        return (len(errors) == 0, errors)

    @classmethod
    def validate_agent(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate an agent configuration dictionary.

        Args:
            data: Agent configuration dictionary.

        Returns:
            Tuple of (is_valid, list_of_errors).
        """
        errors = []

        name = data.get("name", "")
        if not name:
            errors.append("Agent 'name' is required")
        elif not cls.NAME_PATTERN.match(name):
            errors.append(
                f"Agent name '{name}' must match pattern: alphanumeric, hyphens, underscores"
            )

        role = data.get("role", "")
        if not role:
            errors.append("Agent 'role' is required")

        # Temperature validation
        temperature = data.get("temperature", 0.7)
        if not isinstance(temperature, (int, float)):
            errors.append("Temperature must be a number")
        elif not (0.0 <= temperature <= 2.0):
            errors.append("Temperature must be between 0.0 and 2.0")

        # Skills validation
        skills = data.get("skills", [])
        if not isinstance(skills, list):
            errors.append("Skills must be a list")
        else:
            for skill_name in skills:
                if not isinstance(skill_name, str):
                    errors.append(f"Skill name must be a string, got: {type(skill_name).__name__}")

        return (len(errors) == 0, errors)

    @classmethod
    def validate_team(cls, data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate a team configuration dictionary.

        Args:
            data: Team configuration dictionary.

        Returns:
            Tuple of (is_valid, list_of_errors).
        """
        errors = []

        name = data.get("name", "")
        if not name:
            errors.append("Team 'name' is required")
        elif not cls.NAME_PATTERN.match(name):
            errors.append(
                f"Team name '{name}' must match pattern: alphanumeric, hyphens, underscores"
            )

        # Nodes validation
        nodes = data.get("nodes", [])
        if not isinstance(nodes, list):
            errors.append("Nodes must be a list")
        else:
            agent_names = set()
            for i, node in enumerate(nodes):
                node_errors = cls._validate_team_node(node, i)
                errors.extend(node_errors)

                agent_name = node.get("agent_name", "")
                if agent_name in agent_names:
                    errors.append(f"Duplicate agent '{agent_name}' in team nodes")
                agent_names.add(agent_name)

            # Check dependency references
            for node in nodes:
                for dep in node.get("depends_on", []):
                    if dep not in agent_names:
                        errors.append(
                            f"Agent '{node.get('agent_name')}' depends on "
                            f"non-existent agent '{dep}'"
                        )

        return (len(errors) == 0, errors)

    @classmethod
    def _validate_parameter(cls, param: Dict[str, Any], index: int) -> List[str]:
        """Validate a single parameter definition."""
        errors = []
        prefix = f"Parameter #{index}"

        name = param.get("name", "")
        if not name:
            errors.append(f"{prefix}: 'name' is required")
        elif not cls.NAME_PATTERN.match(name):
            errors.append(f"{prefix}: name '{name}' has invalid format")

        ptype = param.get("type", "")
        if ptype not in cls.VALID_PARAM_TYPES:
            errors.append(
                f"{prefix}: type '{ptype}' is not valid. "
                f"Valid types: {', '.join(sorted(cls.VALID_PARAM_TYPES))}"
            )

        if "required" not in param:
            errors.append(f"{prefix}: 'required' field is missing")

        return errors

    @classmethod
    def _validate_io(cls, io: Dict[str, Any], io_type: str, index: int) -> List[str]:
        """Validate a single input/output definition."""
        errors = []
        prefix = f"{io_type.capitalize()} #{index}"

        name = io.get("name", "")
        if not name:
            errors.append(f"{prefix}: 'name' is required")

        itype = io.get("type", "")
        if itype not in cls.VALID_IO_TYPES:
            errors.append(
                f"{prefix}: type '{itype}' is not valid. "
                f"Valid types: {', '.join(sorted(cls.VALID_IO_TYPES))}"
            )

        return errors

    @classmethod
    def _validate_team_node(cls, node: Dict[str, Any], index: int) -> List[str]:
        """Validate a single team node definition."""
        errors = []
        prefix = f"Node #{index}"

        agent_name = node.get("agent_name", "")
        if not agent_name:
            errors.append(f"{prefix}: 'agent_name' is required")

        depends_on = node.get("depends_on", [])
        if not isinstance(depends_on, list):
            errors.append(f"{prefix}: 'depends_on' must be a list")

        return errors

    @classmethod
    def _validate_version(cls, version: str) -> bool:
        """Validate semantic version format (X.Y.Z)."""
        parts = version.split(".")
        if len(parts) != 3:
            return False
        for part in parts:
            try:
                int(part)
            except ValueError:
                return False
        return True
