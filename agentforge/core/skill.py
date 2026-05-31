"""
Skill data model - Defines the structure of an AI Agent skill.

A Skill encapsulates instructions, parameters, inputs, and outputs
that an AI Agent can execute.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List, Optional


@dataclass
class SkillParameter:
    """Represents a single parameter for a Skill."""

    name: str
    type: str  # string, integer, boolean, array, object
    required: bool
    default: Any = None
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillParameter":
        """Create a SkillParameter from a dictionary."""
        return cls(
            name=data.get("name", ""),
            type=data.get("type", "string"),
            required=data.get("required", False),
            default=data.get("default"),
            description=data.get("description", ""),
        )

    def validate(self) -> bool:
        """Validate the parameter definition."""
        valid_types = {"string", "integer", "boolean", "array", "object", "number"}
        if self.type not in valid_types:
            return False
        if not self.name or not isinstance(self.name, str):
            return False
        return True


@dataclass
class SkillIO:
    """Represents an input or output of a Skill."""

    name: str
    type: str
    description: str = ""

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary representation."""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SkillIO":
        """Create a SkillIO from a dictionary."""
        return cls(
            name=data.get("name", ""),
            type=data.get("type", "string"),
            description=data.get("description", ""),
        )

    def validate(self) -> bool:
        """Validate the IO definition."""
        valid_types = {"string", "integer", "boolean", "array", "object", "number", "file"}
        if self.type not in valid_types:
            return False
        if not self.name or not isinstance(self.name, str):
            return False
        return True


@dataclass
class Skill:
    """Represents an AI Agent Skill with full definition.

    A Skill contains instructions (prompts), parameters, inputs, and outputs
    that define what an AI Agent can do.
    """

    name: str
    description: str
    version: str = "1.0.0"
    instructions: str = ""  # Core instructions / prompt
    parameters: List[SkillParameter] = field(default_factory=list)
    inputs: List[SkillIO] = field(default_factory=list)
    outputs: List[SkillIO] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)
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
            "version": self.version,
            "instructions": self.instructions,
            "parameters": [p.to_dict() for p in self.parameters],
            "inputs": [i.to_dict() for i in self.inputs],
            "outputs": [o.to_dict() for o in self.outputs],
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Skill":
        """Create a Skill from a dictionary."""
        params = [SkillParameter.from_dict(p) for p in data.get("parameters", [])]
        inputs = [SkillIO.from_dict(i) for i in data.get("inputs", [])]
        outputs = [SkillIO.from_dict(o) for o in data.get("outputs", [])]
        return cls(
            name=data.get("name", ""),
            description=data.get("description", ""),
            version=data.get("version", "1.0.0"),
            instructions=data.get("instructions", ""),
            parameters=params,
            inputs=inputs,
            outputs=outputs,
            tags=data.get("tags", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "Skill":
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def validate(self) -> List[str]:
        """Validate the skill definition. Returns a list of errors."""
        errors = []
        if not self.name:
            errors.append("Skill name is required")
        if not self.description:
            errors.append("Skill description is required")
        if not self.instructions:
            errors.append("Skill instructions are required")
        for param in self.parameters:
            if not param.validate():
                errors.append(f"Invalid parameter: {param.name}")
        for inp in self.inputs:
            if not inp.validate():
                errors.append(f"Invalid input: {inp.name}")
        for out in self.outputs:
            if not out.validate():
                errors.append(f"Invalid output: {out.name}")
        return errors

    def add_parameter(self, name: str, type: str, required: bool,
                      default: Any = None, description: str = "") -> None:
        """Add a parameter to the skill."""
        self.parameters.append(SkillParameter(
            name=name, type=type, required=required,
            default=default, description=description,
        ))
        self.updated_at = datetime.now().isoformat()

    def add_input(self, name: str, type: str, description: str = "") -> None:
        """Add an input to the skill."""
        self.inputs.append(SkillIO(name=name, type=type, description=description))
        self.updated_at = datetime.now().isoformat()

    def add_output(self, name: str, type: str, description: str = "") -> None:
        """Add an output to the skill."""
        self.outputs.append(SkillIO(name=name, type=type, description=description))
        self.updated_at = datetime.now().isoformat()
