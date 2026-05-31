"""
Skill Testing Sandbox - Simulated skill execution and validation.

Provides a sandboxed environment for testing skills without
actual LLM API calls, validating inputs/outputs and generating test reports.
"""

import json
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Dict, List, Optional

from ..core.skill import Skill
from ..core.engine import SkillExecutor, ExecutionResult


@dataclass
class TestCase:
    """Represents a single test case for skill testing."""

    name: str
    description: str = ""
    inputs: Dict[str, Any] = field(default_factory=dict)
    expected_outputs: List[str] = field(default_factory=list)  # Expected output keys
    should_succeed: bool = True

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "name": self.name,
            "description": self.description,
            "inputs": self.inputs,
            "expected_outputs": self.expected_outputs,
            "should_succeed": self.should_succeed,
        }


@dataclass
class TestResult:
    """Represents the result of a single test case execution."""

    test_name: str
    passed: bool
    skill_name: str
    execution_result: Optional[ExecutionResult] = None
    checks: List[Dict[str, Any]] = field(default_factory=list)
    error_message: str = ""
    duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "test_name": self.test_name,
            "passed": self.passed,
            "skill_name": self.skill_name,
            "execution_result": self.execution_result.to_dict() if self.execution_result else None,
            "checks": self.checks,
            "error_message": self.error_message,
            "duration_ms": self.duration_ms,
        }


@dataclass
class TestReport:
    """Aggregated test report for a skill."""

    skill_name: str
    total_tests: int = 0
    passed: int = 0
    failed: int = 0
    results: List[TestResult] = field(default_factory=list)
    started_at: str = ""
    finished_at: str = ""
    total_duration_ms: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "skill_name": self.skill_name,
            "total_tests": self.total_tests,
            "passed": self.passed,
            "failed": self.failed,
            "pass_rate": f"{(self.passed / self.total_tests * 100):.1f}%" if self.total_tests > 0 else "N/A",
            "results": [r.to_dict() for r in self.results],
            "started_at": self.started_at,
            "finished_at": self.finished_at,
            "total_duration_ms": round(self.total_duration_ms, 2),
        }

    def to_json(self, indent: int = 2) -> str:
        """Serialize to JSON string."""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)

    def summary_text(self) -> str:
        """Generate a human-readable summary."""
        lines = [
            f"=== Test Report: {self.skill_name} ===",
            f"Total: {self.total_tests} | Passed: {self.passed} | Failed: {self.failed}",
            f"Duration: {self.total_duration_ms:.2f}ms",
            "",
        ]
        for result in self.results:
            status = "PASS" if result.passed else "FAIL"
            lines.append(f"  [{status}] {result.test_name}")
            if not result.passed and result.error_message:
                lines.append(f"         Error: {result.error_message}")
        return "\n".join(lines)


class SkillTester:
    """Sandboxed skill tester with simulated execution.

    Tests skills by running simulated executions and validating
    input/output formats against the skill definition.
    """

    def __init__(self):
        """Initialize the skill tester."""
        self._executor = SkillExecutor()

    def test_skill(self, skill: Skill,
                   test_cases: Optional[List[TestCase]] = None) -> TestReport:
        """Run tests on a skill.

        Args:
            skill: The Skill to test.
            test_cases: Optional list of test cases. If not provided,
                       auto-generated test cases will be used.

        Returns:
            TestReport with all test results.
        """
        report = TestReport(skill_name=skill.name)
        report.started_at = datetime.now().isoformat()
        start_time = time.time()

        # Validate skill definition first
        validation_result = self._validate_definition(skill)
        report.total_tests += 1
        if validation_result["valid"]:
            report.passed += 1
            report.results.append(TestResult(
                test_name="definition_validation",
                passed=True,
                skill_name=skill.name,
                checks=[{"check": "Skill definition is valid", "passed": True}],
            ))
        else:
            report.failed += 1
            report.results.append(TestResult(
                test_name="definition_validation",
                passed=False,
                skill_name=skill.name,
                error_message="; ".join(validation_result["errors"]),
                checks=[
                    {"check": e, "passed": False}
                    for e in validation_result["errors"]
                ],
            ))

        # Validate parameters
        param_result = self._validate_parameters(skill)
        report.total_tests += 1
        if param_result["valid"]:
            report.passed += 1
            report.results.append(TestResult(
                test_name="parameter_validation",
                passed=True,
                skill_name=skill.name,
                checks=[{"check": "All parameters are valid", "passed": True}],
            ))
        else:
            report.failed += 1
            report.results.append(TestResult(
                test_name="parameter_validation",
                passed=False,
                skill_name=skill.name,
                error_message="; ".join(param_result["errors"]),
            ))

        # Validate inputs/outputs
        io_result = self._validate_io(skill)
        report.total_tests += 1
        if io_result["valid"]:
            report.passed += 1
            report.results.append(TestResult(
                test_name="io_validation",
                passed=True,
                skill_name=skill.name,
                checks=[{"check": "All inputs/outputs are valid", "passed": True}],
            ))
        else:
            report.failed += 1
            report.results.append(TestResult(
                test_name="io_validation",
                passed=False,
                skill_name=skill.name,
                error_message="; ".join(io_result["errors"]),
            ))

        # Run custom test cases if provided
        if test_cases:
            for tc in test_cases:
                report.total_tests += 1
                tc_result = self._run_test_case(skill, tc)
                if tc_result.passed:
                    report.passed += 1
                else:
                    report.failed += 1
                report.results.append(tc_result)

        # Run serialization test
        report.total_tests += 1
        ser_result = self._test_serialization(skill)
        if ser_result.passed:
            report.passed += 1
        else:
            report.failed += 1
        report.results.append(ser_result)

        report.finished_at = datetime.now().isoformat()
        report.total_duration_ms = (time.time() - start_time) * 1000
        return report

    def _validate_definition(self, skill: Skill) -> Dict[str, Any]:
        """Validate the skill definition."""
        errors = skill.validate()
        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_parameters(self, skill: Skill) -> Dict[str, Any]:
        """Validate all skill parameters."""
        errors = []
        for param in skill.parameters:
            if not param.validate():
                errors.append(f"Invalid parameter: {param.name}")
        return {"valid": len(errors) == 0, "errors": errors}

    def _validate_io(self, skill: Skill) -> Dict[str, Any]:
        """Validate all skill inputs and outputs."""
        errors = []
        for inp in skill.inputs:
            if not inp.validate():
                errors.append(f"Invalid input: {inp.name}")
        for out in skill.outputs:
            if not out.validate():
                errors.append(f"Invalid output: {out.name}")
        return {"valid": len(errors) == 0, "errors": errors}

    def _run_test_case(self, skill: Skill, test_case: TestCase) -> TestResult:
        """Run a single test case against the skill."""
        start_time = time.time()

        try:
            result = self._executor.execute(skill, test_case.inputs)
            elapsed = (time.time() - start_time) * 1000

            checks = []
            all_passed = True

            # Check if success matches expectation
            if result.success != test_case.should_succeed:
                checks.append({
                    "check": f"Expected success={test_case.should_succeed}, got {result.success}",
                    "passed": False,
                })
                all_passed = False
            else:
                checks.append({
                    "check": f"Execution success={result.success}",
                    "passed": True,
                })

            # Check expected output keys
            if test_case.expected_outputs and result.success:
                for key in test_case.expected_outputs:
                    found = key in result.outputs
                    checks.append({
                        "check": f"Output '{key}' present",
                        "passed": found,
                    })
                    if not found:
                        all_passed = False

            return TestResult(
                test_name=test_case.name,
                passed=all_passed,
                skill_name=skill.name,
                execution_result=result,
                checks=checks,
                duration_ms=round(elapsed, 2),
            )

        except Exception as e:
            elapsed = (time.time() - start_time) * 1000
            return TestResult(
                test_name=test_case.name,
                passed=False,
                skill_name=skill.name,
                error_message=str(e),
                duration_ms=round(elapsed, 2),
            )

    def _test_serialization(self, skill: Skill) -> TestResult:
        """Test JSON serialization and deserialization."""
        try:
            json_str = skill.to_json()
            restored = Skill.from_json(json_str)

            checks = [
                {"check": "to_json() produces valid JSON", "passed": True},
                {"check": "from_json() restores skill name", "passed": restored.name == skill.name},
                {"check": "from_json() restores description", "passed": restored.description == skill.description},
                {"check": "from_json() restores parameters count",
                 "passed": len(restored.parameters) == len(skill.parameters)},
                {"check": "from_json() restores inputs count",
                 "passed": len(restored.inputs) == len(skill.inputs)},
                {"check": "from_json() restores outputs count",
                 "passed": len(restored.outputs) == len(skill.outputs)},
            ]

            all_passed = all(c["passed"] for c in checks)

            return TestResult(
                test_name="serialization_roundtrip",
                passed=all_passed,
                skill_name=skill.name,
                checks=checks,
            )
        except Exception as e:
            return TestResult(
                test_name="serialization_roundtrip",
                passed=False,
                skill_name=skill.name,
                error_message=str(e),
            )

    def generate_test_cases(self, skill: Skill) -> List[TestCase]:
        """Auto-generate test cases for a skill based on its definition.

        Args:
            skill: The Skill to generate test cases for.

        Returns:
            List of generated TestCase objects.
        """
        cases = []

        # Test with all required parameters
        required_inputs = {}
        for param in skill.parameters:
            if param.required:
                required_inputs[param.name] = self._generate_sample_value(param)

        if required_inputs:
            cases.append(TestCase(
                name="required_params_only",
                description="Test with only required parameters",
                inputs=required_inputs,
                expected_outputs=[o.name for o in skill.outputs],
                should_succeed=True,
            ))

        # Test with all parameters
        all_inputs = dict(required_inputs)
        for param in skill.parameters:
            if not param.required:
                all_inputs[param.name] = self._generate_sample_value(param)

        if all_inputs:
            cases.append(TestCase(
                name="all_params",
                description="Test with all parameters",
                inputs=all_inputs,
                expected_outputs=[o.name for o in skill.outputs],
                should_succeed=True,
            ))

        # Test missing required parameters
        if skill.parameters:
            cases.append(TestCase(
                name="missing_required",
                description="Test with missing required parameters",
                inputs={},
                should_succeed=False,
            ))

        return cases

    def _generate_sample_value(self, param) -> Any:
        """Generate a sample value for a parameter based on its type."""
        type_samples = {
            "string": "sample_text",
            "integer": 42,
            "number": 3.14,
            "boolean": True,
            "array": ["item1", "item2"],
            "object": {"key": "value"},
        }
        return type_samples.get(param.type, "sample")
