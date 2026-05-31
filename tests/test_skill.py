"""
Tests for the Skill data model.

Tests skill creation, serialization, validation, and parameter/IO management.
"""

import json
import pytest

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from agentforge.core.skill import Skill, SkillParameter, SkillIO


class TestSkillParameter:
    """Tests for SkillParameter class."""

    def test_create_parameter(self):
        """Test basic parameter creation."""
        param = SkillParameter(
            name="test_param",
            type="string",
            required=True,
            description="A test parameter",
        )
        assert param.name == "test_param"
        assert param.type == "string"
        assert param.required is True
        assert param.description == "A test parameter"

    def test_parameter_to_dict(self):
        """Test parameter serialization to dictionary."""
        param = SkillParameter(name="x", type="integer", required=False, default=42)
        d = param.to_dict()
        assert d["name"] == "x"
        assert d["type"] == "integer"
        assert d["required"] is False
        assert d["default"] == 42

    def test_parameter_from_dict(self):
        """Test parameter deserialization from dictionary."""
        data = {"name": "y", "type": "boolean", "required": True, "default": False}
        param = SkillParameter.from_dict(data)
        assert param.name == "y"
        assert param.type == "boolean"
        assert param.required is True
        assert param.default is False

    def test_parameter_validate_valid(self):
        """Test validation of a valid parameter."""
        param = SkillParameter(name="valid", type="string", required=True)
        assert param.validate() is True

    def test_parameter_validate_invalid_type(self):
        """Test validation rejects invalid type."""
        param = SkillParameter(name="x", type="invalid_type", required=True)
        assert param.validate() is False

    def test_parameter_validate_empty_name(self):
        """Test validation rejects empty name."""
        param = SkillParameter(name="", type="string", required=True)
        assert param.validate() is False

    def test_parameter_roundtrip(self):
        """Test to_dict -> from_dict roundtrip."""
        original = SkillParameter(
            name="roundtrip", type="array", required=False,
            default=["a", "b"], description="test",
        )
        restored = SkillParameter.from_dict(original.to_dict())
        assert restored.name == original.name
        assert restored.type == original.type
        assert restored.required == original.required
        assert restored.default == original.default
        assert restored.description == original.description


class TestSkillIO:
    """Tests for SkillIO class."""

    def test_create_io(self):
        """Test basic IO creation."""
        io = SkillIO(name="output_data", type="object", description="Output data")
        assert io.name == "output_data"
        assert io.type == "object"

    def test_io_to_dict(self):
        """Test IO serialization."""
        io = SkillIO(name="result", type="string", description="The result")
        d = io.to_dict()
        assert d["name"] == "result"
        assert d["type"] == "string"

    def test_io_from_dict(self):
        """Test IO deserialization."""
        data = {"name": "score", "type": "integer", "description": "Score value"}
        io = SkillIO.from_dict(data)
        assert io.name == "score"
        assert io.type == "integer"

    def test_io_validate_valid(self):
        """Test validation of valid IO."""
        io = SkillIO(name="valid", type="file")
        assert io.validate() is True

    def test_io_validate_invalid_type(self):
        """Test validation rejects invalid type."""
        io = SkillIO(name="x", type="custom")
        assert io.validate() is False


class TestSkill:
    """Tests for Skill class."""

    def _make_skill(self, **kwargs) -> Skill:
        """Helper to create a basic skill with defaults."""
        defaults = {
            "name": "test-skill",
            "description": "A test skill",
            "instructions": "You are a test assistant.",
        }
        defaults.update(kwargs)
        return Skill(**defaults)

    def test_create_skill(self):
        """Test basic skill creation."""
        skill = self._make_skill()
        assert skill.name == "test-skill"
        assert skill.description == "A test skill"
        assert skill.instructions == "You are a test assistant."
        assert skill.version == "1.0.0"
        assert skill.created_at != ""
        assert skill.updated_at != ""

    def test_skill_to_dict(self):
        """Test skill serialization to dictionary."""
        skill = self._make_skill()
        skill.add_parameter("input_text", "string", True, description="Input text")
        skill.add_output("result", "string", "The result")

        d = skill.to_dict()
        assert d["name"] == "test-skill"
        assert len(d["parameters"]) == 1
        assert len(d["outputs"]) == 1
        assert d["parameters"][0]["name"] == "input_text"

    def test_skill_from_dict(self):
        """Test skill deserialization from dictionary."""
        data = {
            "name": "from-dict",
            "description": "Created from dict",
            "instructions": "Instructions here",
            "version": "2.0.0",
            "parameters": [
                {"name": "p1", "type": "string", "required": True}
            ],
            "inputs": [
                {"name": "i1", "type": "string", "description": "Input"}
            ],
            "outputs": [
                {"name": "o1", "type": "string", "description": "Output"}
            ],
            "tags": ["test", "demo"],
        }
        skill = Skill.from_dict(data)
        assert skill.name == "from-dict"
        assert skill.version == "2.0.0"
        assert len(skill.parameters) == 1
        assert len(skill.inputs) == 1
        assert len(skill.outputs) == 1
        assert skill.tags == ["test", "demo"]

    def test_skill_to_json(self):
        """Test JSON serialization."""
        skill = self._make_skill()
        json_str = skill.to_json()
        parsed = json.loads(json_str)
        assert parsed["name"] == "test-skill"

    def test_skill_from_json(self):
        """Test JSON deserialization."""
        skill = self._make_skill()
        json_str = skill.to_json()
        restored = Skill.from_json(json_str)
        assert restored.name == skill.name
        assert restored.description == skill.description
        assert restored.instructions == skill.instructions

    def test_skill_validate_valid(self):
        """Test validation of a valid skill."""
        skill = self._make_skill()
        errors = skill.validate()
        assert errors == []

    def test_skill_validate_missing_name(self):
        """Test validation detects missing name."""
        skill = Skill(name="", description="desc", instructions="inst")
        errors = skill.validate()
        assert any("name" in e for e in errors)

    def test_skill_validate_missing_description(self):
        """Test validation detects missing description."""
        skill = Skill(name="x", description="", instructions="inst")
        errors = skill.validate()
        assert any("description" in e for e in errors)

    def test_skill_validate_missing_instructions(self):
        """Test validation detects missing instructions."""
        skill = Skill(name="x", description="desc", instructions="")
        errors = skill.validate()
        assert any("instructions" in e for e in errors)

    def test_add_parameter(self):
        """Test adding a parameter to a skill."""
        skill = self._make_skill()
        skill.add_parameter("param1", "string", True, description="First param")
        assert len(skill.parameters) == 1
        assert skill.parameters[0].name == "param1"

    def test_add_input(self):
        """Test adding an input to a skill."""
        skill = self._make_skill()
        skill.add_input("data", "string", "Input data")
        assert len(skill.inputs) == 1
        assert skill.inputs[0].name == "data"

    def test_add_output(self):
        """Test adding an output to a skill."""
        skill = self._make_skill()
        skill.add_output("result", "object", "Result object")
        assert len(skill.outputs) == 1
        assert skill.outputs[0].name == "result"

    def test_json_roundtrip_preserves_all_fields(self):
        """Test full JSON roundtrip preserves all fields."""
        skill = self._make_skill()
        skill.add_parameter("p1", "integer", True, default=10)
        skill.add_parameter("p2", "boolean", False)
        skill.add_input("i1", "string", "Input")
        skill.add_output("o1", "array", "Output")
        skill.tags = ["a", "b"]

        json_str = skill.to_json()
        restored = Skill.from_json(json_str)

        assert restored.name == skill.name
        assert restored.version == skill.version
        assert restored.instructions == skill.instructions
        assert len(restored.parameters) == 2
        assert restored.parameters[0].default == 10
        assert restored.parameters[1].required is False
        assert len(restored.inputs) == 1
        assert len(restored.outputs) == 1
        assert restored.tags == ["a", "b"]
