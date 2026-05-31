"""
MCP Server format exporter - Export skills to Model Context Protocol server format.

Converts AgentForge skills into MCP-compatible tool definitions with
proper inputSchema, descriptions, and annotations.
"""

import json
from typing import Any, Dict, List, Optional

from ..core.skill import Skill


class MCPExporter:
    """Exports AgentForge Skills to MCP Server format.

    The MCP (Model Context Protocol) format defines tools that can be
    consumed by LLM clients. Each skill is converted to a tool definition
    with an inputSchema following JSON Schema conventions.
    """

    # Mapping from Skill parameter types to JSON Schema types
    _TYPE_MAP = {
        "string": {"type": "string"},
        "integer": {"type": "integer"},
        "number": {"type": "number"},
        "boolean": {"type": "boolean"},
        "array": {"type": "array", "items": {"type": "string"}},
        "object": {"type": "object"},
    }

    def export_skill(self, skill: Skill, server_name: Optional[str] = None) -> Dict[str, Any]:
        """Export a single skill to MCP tool format.

        Args:
            skill: The Skill to export.
            server_name: Optional server name for the MCP configuration.

        Returns:
            Dictionary containing the MCP tool definition.
        """
        server_name = server_name or f"agentforge-{skill.name}"

        tool_definition = {
            "name": skill.name,
            "description": skill.description,
            "inputSchema": self._build_input_schema(skill),
            "annotations": {
                "title": skill.description,
                "readOnlyHint": True,
                "destructiveHint": False,
                "idempotentHint": True,
                "openWorldHint": False,
            },
            "metadata": {
                "version": skill.version,
                "tags": skill.tags,
                "inputs": [
                    {"name": io.name, "type": io.type, "description": io.description}
                    for io in skill.inputs
                ],
                "outputs": [
                    {"name": io.name, "type": io.type, "description": io.description}
                    for io in skill.outputs
                ],
            },
        }

        return {
            "mcpServer": {
                "name": server_name,
                "version": skill.version,
                "tools": [tool_definition],
                "instructions": skill.instructions,
            }
        }

    def export_skills(self, skills: List[Skill],
                       server_name: str = "agentforge-server") -> Dict[str, Any]:
        """Export multiple skills to a single MCP server configuration.

        Args:
            skills: List of Skills to export.
            server_name: Name for the MCP server.

        Returns:
            Dictionary containing the MCP server configuration with all tools.
        """
        tools = []
        for skill in skills:
            tool_def = {
                "name": skill.name,
                "description": skill.description,
                "inputSchema": self._build_input_schema(skill),
                "annotations": {
                    "title": skill.description,
                    "readOnlyHint": True,
                    "destructiveHint": False,
                    "idempotentHint": True,
                    "openWorldHint": False,
                },
                "metadata": {
                    "version": skill.version,
                    "tags": skill.tags,
                },
            }
            tools.append(tool_def)

        return {
            "mcpServer": {
                "name": server_name,
                "version": "1.0.0",
                "tools": tools,
            }
        }

    def export_to_json(self, skill: Skill, server_name: Optional[str] = None,
                       indent: int = 2) -> str:
        """Export a skill to MCP JSON string.

        Args:
            skill: The Skill to export.
            server_name: Optional server name.
            indent: JSON indentation level.

        Returns:
            JSON string of the MCP tool definition.
        """
        data = self.export_skill(skill, server_name)
        return json.dumps(data, indent=indent, ensure_ascii=False)

    def export_to_file(self, skill: Skill, filepath: str,
                       server_name: Optional[str] = None) -> None:
        """Export a skill to an MCP JSON file.

        Args:
            skill: The Skill to export.
            filepath: Path to write the JSON file.
            server_name: Optional server name.
        """
        content = self.export_to_json(skill, server_name)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    def _build_input_schema(self, skill: Skill) -> Dict[str, Any]:
        """Build JSON Schema inputSchema from skill parameters.

        Args:
            skill: The Skill to build schema for.

        Returns:
            JSON Schema dictionary.
        """
        properties = {}
        required = []

        for param in skill.parameters:
            schema = self._TYPE_MAP.get(param.type, {"type": "string"})
            if param.description:
                schema["description"] = param.description
            if param.default is not None:
                schema["default"] = param.default
            properties[param.name] = schema

            if param.required:
                required.append(param.name)

        input_schema = {
            "type": "object",
            "properties": properties,
        }
        if required:
            input_schema["required"] = required

        return input_schema
