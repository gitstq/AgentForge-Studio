"""
File I/O utilities - Read and write skill, agent, and team data.

Handles persistence of AgentForge entities to/from the filesystem
using JSON format with proper directory management.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

from ..core.skill import Skill
from ..core.agent import Agent
from ..core.team import Team


class FileIO:
    """File I/O manager for AgentForge Studio entities.

    Manages reading and writing Skills, Agents, and Teams to the
    filesystem using a structured directory layout.
    """

    # Default directory names
    SKILLS_DIR = "skills"
    AGENTS_DIR = "agents"
    TEAMS_DIR = "teams"

    def __init__(self, base_dir: Optional[str] = None):
        """Initialize FileIO with a base directory.

        Args:
            base_dir: Base directory for all data. Defaults to current directory.
        """
        self._base_dir = Path(base_dir) if base_dir else Path.cwd()

    @property
    def base_dir(self) -> Path:
        """Get the base directory path."""
        return self._base_dir

    @property
    def skills_dir(self) -> Path:
        """Get the skills directory path."""
        return self._base_dir / self.SKILLS_DIR

    @property
    def agents_dir(self) -> Path:
        """Get the agents directory path."""
        return self._base_dir / self.AGENTS_DIR

    @property
    def teams_dir(self) -> Path:
        """Get the teams directory path."""
        return self._base_dir / self.TEAMS_DIR

    def init_project(self) -> Dict[str, str]:
        """Initialize the project directory structure.

        Creates skills/, agents/, and teams/ directories.

        Returns:
            Dictionary mapping directory names to their paths.
        """
        dirs = {}
        for name, dir_path in [
            ("skills", self.skills_dir),
            ("agents", self.agents_dir),
            ("teams", self.teams_dir),
        ]:
            dir_path.mkdir(parents=True, exist_ok=True)
            dirs[name] = str(dir_path)
        return dirs

    # --- Skill I/O ---

    def save_skill(self, skill: Skill) -> str:
        """Save a skill to a JSON file.

        Args:
            skill: The Skill to save.

        Returns:
            Path to the saved file.
        """
        self.skills_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.skills_dir / f"{skill.name}.json"
        filepath.write_text(skill.to_json(), encoding="utf-8")
        return str(filepath)

    def load_skill(self, name: str) -> Optional[Skill]:
        """Load a skill from a JSON file.

        Args:
            name: The skill name (filename without .json).

        Returns:
            The loaded Skill, or None if not found.
        """
        filepath = self.skills_dir / f"{name}.json"
        if not filepath.exists():
            return None
        content = filepath.read_text(encoding="utf-8")
        return Skill.from_json(content)

    def list_skills(self) -> List[str]:
        """List all saved skill names.

        Returns:
            List of skill names.
        """
        if not self.skills_dir.exists():
            return []
        return [p.stem for p in self.skills_dir.glob("*.json")]

    def delete_skill(self, name: str) -> bool:
        """Delete a skill file.

        Args:
            name: The skill name.

        Returns:
            True if deleted, False if not found.
        """
        filepath = self.skills_dir / f"{name}.json"
        if filepath.exists():
            filepath.unlink()
            return True
        return False

    # --- Agent I/O ---

    def save_agent(self, agent: Agent) -> str:
        """Save an agent to a JSON file.

        Args:
            agent: The Agent to save.

        Returns:
            Path to the saved file.
        """
        self.agents_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.agents_dir / f"{agent.name}.json"
        filepath.write_text(agent.to_json(), encoding="utf-8")
        return str(filepath)

    def load_agent(self, name: str) -> Optional[Agent]:
        """Load an agent from a JSON file.

        Args:
            name: The agent name.

        Returns:
            The loaded Agent, or None if not found.
        """
        filepath = self.agents_dir / f"{name}.json"
        if not filepath.exists():
            return None
        content = filepath.read_text(encoding="utf-8")
        return Agent.from_json(content)

    def list_agents(self) -> List[str]:
        """List all saved agent names.

        Returns:
            List of agent names.
        """
        if not self.agents_dir.exists():
            return []
        return [p.stem for p in self.agents_dir.glob("*.json")]

    def delete_agent(self, name: str) -> bool:
        """Delete an agent file.

        Args:
            name: The agent name.

        Returns:
            True if deleted, False if not found.
        """
        filepath = self.agents_dir / f"{name}.json"
        if filepath.exists():
            filepath.unlink()
            return True
        return False

    # --- Team I/O ---

    def save_team(self, team: Team) -> str:
        """Save a team to a JSON file.

        Args:
            team: The Team to save.

        Returns:
            Path to the saved file.
        """
        self.teams_dir.mkdir(parents=True, exist_ok=True)
        filepath = self.teams_dir / f"{team.name}.json"
        filepath.write_text(team.to_json(), encoding="utf-8")
        return str(filepath)

    def load_team(self, name: str) -> Optional[Team]:
        """Load a team from a JSON file.

        Args:
            name: The team name.

        Returns:
            The loaded Team, or None if not found.
        """
        filepath = self.teams_dir / f"{name}.json"
        if not filepath.exists():
            return None
        content = filepath.read_text(encoding="utf-8")
        return Team.from_json(content)

    def list_teams(self) -> List[str]:
        """List all saved team names.

        Returns:
            List of team names.
        """
        if not self.teams_dir.exists():
            return []
        return [p.stem for p in self.teams_dir.glob("*.json")]

    def delete_team(self, name: str) -> bool:
        """Delete a team file.

        Args:
            name: The team name.

        Returns:
            True if deleted, False if not found.
        """
        filepath = self.teams_dir / f"{name}.json"
        if filepath.exists():
            filepath.unlink()
            return True
        return False

    # --- Generic I/O ---

    def read_json(self, filepath: str) -> Optional[Dict[str, Any]]:
        """Read a JSON file.

        Args:
            filepath: Path to the JSON file.

        Returns:
            Parsed dictionary, or None if file doesn't exist.
        """
        path = Path(filepath)
        if not path.exists():
            return None
        content = path.read_text(encoding="utf-8")
        return json.loads(content)

    def write_json(self, filepath: str, data: Dict[str, Any],
                   indent: int = 2) -> str:
        """Write data to a JSON file.

        Args:
            filepath: Path to write to.
            data: Dictionary data to write.
            indent: JSON indentation.

        Returns:
            Path to the written file.
        """
        path = Path(filepath)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, indent=indent, ensure_ascii=False), encoding="utf-8")
        return str(path)
