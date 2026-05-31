"""
Agent data model - Defines the structure of an AI Agent.

An Agent has a role, system prompt, and a list of skills it can execute.
"""

import json
from dataclasses import dataclass, field, asdict
from datetime import datetime
from typing import Any, Dict, List


@dataclass
class Agent:
    """Represents an AI Agent with role, skills, and configuration.

    An Agent is an entity that can execute skills. It has a role description,
    a system prompt, and a list of assigned skills.
    """

    name: str
    role: str  # Role description
    system_prompt: str = ""
    skills: List[str] = field(default_factory=list)  # Skill name list
    model: str = "default"
    temperature: float = 0.7
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
            "role": self.role,
            "system_prompt": self.system_prompt,
            "skills": list(self.skills),
            "model": self.model,
            "temperature": self.temperature,
            "tags": self.tags,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Agent":
        """Create an Agent from a dictionary."""
        return cls(
            name=data.get("name", ""),
            role=data.get("role", ""),
            system_prompt=data.get("system_prompt", ""),
            skills=data.get("skills", []),
            model=data.get("model", "default"),
            temperature=data.get("temperature", 0.7),
            tags=data.get("tags", []),
            created_at=data.get("created_at", ""),
            updated_at=data.get("updated_at", ""),
        )

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    @classmethod
    def from_json(cls, json_str: str) -> "Agent":
        """Deserialize from JSON string."""
        data = json.loads(json_str)
        return cls.from_dict(data)

    def validate(self) -> List[str]:
        """Validate the agent definition. Returns a list of errors."""
        errors = []
        if not self.name:
            errors.append("Agent name is required")
        if not self.role:
            errors.append("Agent role is required")
        if not isinstance(self.temperature, (int, float)) or not (0.0 <= self.temperature <= 2.0):
            errors.append("Temperature must be between 0.0 and 2.0")
        return errors

    def assign_skill(self, skill_name: str) -> None:
        """Assign a skill to this agent."""
        if skill_name not in self.skills:
            self.skills.append(skill_name)
            self.updated_at = datetime.now().isoformat()

    def remove_skill(self, skill_name: str) -> bool:
        """Remove a skill from this agent. Returns True if removed."""
        if skill_name in self.skills:
            self.skills.remove(skill_name)
            self.updated_at = datetime.now().isoformat()
            return True
        return False

    def has_skill(self, skill_name: str) -> bool:
        """Check if the agent has a specific skill."""
        return skill_name in self.skills
