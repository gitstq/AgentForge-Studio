"""
CLI Entry Point - Command-line interface for AgentForge Studio.

Provides the main `agentforge` command with subcommands for managing
skills, agents, teams, templates, and the TUI dashboard.
"""

import argparse
import json
import sys
from typing import Optional

from . import __version__
from .core.skill import Skill
from .core.agent import Agent
from .core.team import Team
from .core.engine import SkillExecutor, TeamExecutor
from .templates import get_builtin_templates, get_template_names, apply_template
from .export.mcp import MCPExporter
from .sandbox.tester import SkillTester
from .tui.dashboard import Dashboard
from .utils.file_io import FileIO


def create_parser() -> argparse.ArgumentParser:
    """Create the main argument parser with all subcommands.

    Returns:
        Configured ArgumentParser instance.
    """
    parser = argparse.ArgumentParser(
        prog="agentforge",
        description="AgentForge Studio - AI Agent Skill Factory & Team Orchestration Engine",
    )
    parser.add_argument(
        "--version", "-v",
        action="version",
        version=f"AgentForge Studio v{__version__}",
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # --- init command ---
    subparsers.add_parser("init", help="Initialize project directory")

    # --- skill subcommands ---
    skill_parser = subparsers.add_parser("skill", help="Manage skills")
    skill_sub = skill_parser.add_subparsers(dest="skill_command")

    # skill create
    skill_create = skill_sub.add_parser("create", help="Create a new skill")
    skill_create.add_argument("name", help="Skill name")
    skill_create.add_argument("--description", "-d", default="", help="Skill description")
    skill_create.add_argument("--instructions", "-i", default="", help="Skill instructions")

    # skill list
    skill_sub.add_parser("list", help="List all skills")

    # skill show
    skill_show = skill_sub.add_parser("show", help="Show skill details")
    skill_show.add_argument("name", help="Skill name")

    # skill test
    skill_test = skill_sub.add_parser("test", help="Test a skill")
    skill_test.add_argument("name", help="Skill name")

    # skill export
    skill_export = skill_sub.add_parser("export", help="Export a skill")
    skill_export.add_argument("name", help="Skill name")
    skill_export.add_argument("--format", "-f", default="mcp",
                              choices=["mcp"], help="Export format")
    skill_export.add_argument("--output", "-o", default="",
                              help="Output file path")

    # --- agent subcommands ---
    agent_parser = subparsers.add_parser("agent", help="Manage agents")
    agent_sub = agent_parser.add_subparsers(dest="agent_command")

    # agent create
    agent_create = agent_sub.add_parser("create", help="Create a new agent")
    agent_create.add_argument("name", help="Agent name")
    agent_create.add_argument("--role", "-r", default="", help="Agent role description")
    agent_create.add_argument("--system-prompt", "-s", default="", help="System prompt")
    agent_create.add_argument("--model", "-m", default="default", help="LLM model name")

    # agent list
    agent_sub.add_parser("list", help="List all agents")

    # agent assign
    agent_assign = agent_sub.add_parser("assign", help="Assign a skill to an agent")
    agent_assign.add_argument("agent", help="Agent name")
    agent_assign.add_argument("skill", help="Skill name")

    # --- team subcommands ---
    team_parser = subparsers.add_parser("team", help="Manage teams")
    team_sub = team_parser.add_subparsers(dest="team_command")

    # team create
    team_create = team_sub.add_parser("create", help="Create a new team")
    team_create.add_argument("name", help="Team name")
    team_create.add_argument("--description", "-d", default="", help="Team description")

    # team add
    team_add = team_sub.add_parser("add", help="Add an agent to a team")
    team_add.add_argument("team", help="Team name")
    team_add.add_argument("agent", help="Agent name")
    team_add.add_argument("--depends-on", nargs="*", default=[],
                          help="Agent dependencies")

    # team visualize
    team_viz = team_sub.add_parser("visualize", help="Visualize team DAG")
    team_viz.add_argument("name", help="Team name")

    # team run
    team_run = team_sub.add_parser("run", help="Execute team orchestration")
    team_run.add_argument("name", help="Team name")

    # --- template subcommands ---
    template_parser = subparsers.add_parser("template", help="Manage templates")
    template_sub = template_parser.add_subparsers(dest="template_command")

    # template list
    template_sub.add_parser("list", help="List built-in templates")

    # template apply
    template_apply = template_sub.add_parser("apply", help="Apply a template")
    template_apply.add_argument("template", help="Template name")
    template_apply.add_argument("name", help="New skill name")

    # --- dashboard command ---
    subparsers.add_parser("dashboard", help="Launch TUI dashboard")

    return parser


def main(argv: Optional[list] = None) -> int:
    """Main CLI entry point.

    Args:
        argv: Command-line arguments (defaults to sys.argv[1:]).

    Returns:
        Exit code (0 for success, non-zero for errors).
    """
    parser = create_parser()
    args = parser.parse_args(argv)

    if not args.command:
        parser.print_help()
        return 0

    dashboard = Dashboard()
    file_io = FileIO()

    # --- init ---
    if args.command == "init":
        dirs = file_io.init_project()
        dashboard.show_success(f"Project initialized at {file_io.base_dir}")
        for name, path in dirs.items():
            dashboard.show_info(f"  Created {name}/ directory")

    # --- skill commands ---
    elif args.command == "skill":
        if not hasattr(args, "skill_command") or not args.skill_command:
            parser.parse_args(["skill", "--help"])
            return 1

        if args.skill_command == "create":
            _cmd_skill_create(args, dashboard, file_io)

        elif args.skill_command == "list":
            _cmd_skill_list(dashboard, file_io)

        elif args.skill_command == "show":
            _cmd_skill_show(args, dashboard, file_io)

        elif args.skill_command == "test":
            _cmd_skill_test(args, dashboard, file_io)

        elif args.skill_command == "export":
            _cmd_skill_export(args, dashboard, file_io)

    # --- agent commands ---
    elif args.command == "agent":
        if not hasattr(args, "agent_command") or not args.agent_command:
            parser.parse_args(["agent", "--help"])
            return 1

        if args.agent_command == "create":
            _cmd_agent_create(args, dashboard, file_io)

        elif args.agent_command == "list":
            _cmd_agent_list(dashboard, file_io)

        elif args.agent_command == "assign":
            _cmd_agent_assign(args, dashboard, file_io)

    # --- team commands ---
    elif args.command == "team":
        if not hasattr(args, "team_command") or not args.team_command:
            parser.parse_args(["team", "--help"])
            return 1

        if args.team_command == "create":
            _cmd_team_create(args, dashboard, file_io)

        elif args.team_command == "add":
            _cmd_team_add(args, dashboard, file_io)

        elif args.team_command == "visualize":
            _cmd_team_visualize(args, dashboard, file_io)

        elif args.team_command == "run":
            _cmd_team_run(args, dashboard, file_io)

    # --- template commands ---
    elif args.command == "template":
        if not hasattr(args, "template_command") or not args.template_command:
            parser.parse_args(["template", "--help"])
            return 1

        if args.template_command == "list":
            _cmd_template_list(dashboard)

        elif args.template_command == "apply":
            _cmd_template_apply(args, dashboard, file_io)

    # --- dashboard ---
    elif args.command == "dashboard":
        _cmd_dashboard(dashboard, file_io)

    return 0


# ============================================================
# Command handlers
# ============================================================

def _cmd_skill_create(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'skill create' command."""
    # Check if skill already exists
    existing = file_io.load_skill(args.name)
    if existing:
        dashboard.show_error(f"Skill '{args.name}' already exists")
        return

    skill = Skill(
        name=args.name,
        description=args.description or f"Skill: {args.name}",
        instructions=args.instructions or f"You are a helpful assistant for {args.name}.",
    )

    errors = skill.validate()
    if errors:
        dashboard.show_error(f"Validation failed: {'; '.join(errors)}")
        return

    filepath = file_io.save_skill(skill)
    dashboard.show_success(f"Skill '{args.name}' created -> {filepath}")


def _cmd_skill_list(dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'skill list' command."""
    names = file_io.list_skills()
    if not names:
        dashboard.show_info("No skills found. Use 'agentforge skill create <name>' to create one.")
        return

    skills = []
    for name in names:
        skill = file_io.load_skill(name)
        if skill:
            skills.append(skill.to_dict())

    dashboard.show_skills(skills)


def _cmd_skill_show(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'skill show' command."""
    skill = file_io.load_skill(args.name)
    if not skill:
        dashboard.show_error(f"Skill '{args.name}' not found")
        return

    dashboard.show_skill_detail(skill.to_dict())


def _cmd_skill_test(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'skill test' command."""
    skill = file_io.load_skill(args.name)
    if not skill:
        dashboard.show_error(f"Skill '{args.name}' not found")
        return

    tester = SkillTester()
    test_cases = tester.generate_test_cases(skill)
    report = tester.test_skill(skill, test_cases)
    dashboard.show_test_report(report.summary_text())


def _cmd_skill_export(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'skill export' command."""
    skill = file_io.load_skill(args.name)
    if not skill:
        dashboard.show_error(f"Skill '{args.name}' not found")
        return

    if args.format == "mcp":
        exporter = MCPExporter()
        if args.output:
            exporter.export_to_file(skill, args.output)
            dashboard.show_success(f"Exported to {args.output}")
        else:
            content = exporter.export_to_json(skill)
            print(content)
    else:
        dashboard.show_error(f"Unsupported export format: {args.format}")


def _cmd_agent_create(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'agent create' command."""
    existing = file_io.load_agent(args.name)
    if existing:
        dashboard.show_error(f"Agent '{args.name}' already exists")
        return

    agent = Agent(
        name=args.name,
        role=args.role or f"Agent: {args.name}",
        system_prompt=args.system_prompt or f"You are {args.name}.",
        model=args.model,
    )

    errors = agent.validate()
    if errors:
        dashboard.show_error(f"Validation failed: {'; '.join(errors)}")
        return

    filepath = file_io.save_agent(agent)
    dashboard.show_success(f"Agent '{args.name}' created -> {filepath}")


def _cmd_agent_list(dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'agent list' command."""
    names = file_io.list_agents()
    if not names:
        dashboard.show_info("No agents found. Use 'agentforge agent create <name>' to create one.")
        return

    agents = []
    for name in names:
        agent = file_io.load_agent(name)
        if agent:
            agents.append(agent.to_dict())

    dashboard.show_agents(agents)


def _cmd_agent_assign(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'agent assign' command."""
    agent = file_io.load_agent(args.agent)
    if not agent:
        dashboard.show_error(f"Agent '{args.agent}' not found")
        return

    skill = file_io.load_skill(args.skill)
    if not skill:
        dashboard.show_error(f"Skill '{args.skill}' not found")
        return

    agent.assign_skill(args.skill)
    filepath = file_io.save_agent(agent)
    dashboard.show_success(
        f"Skill '{args.skill}' assigned to agent '{args.agent}' -> {filepath}"
    )


def _cmd_team_create(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'team create' command."""
    existing = file_io.load_team(args.name)
    if existing:
        dashboard.show_error(f"Team '{args.name}' already exists")
        return

    team = Team(
        name=args.name,
        description=args.description or f"Team: {args.name}",
    )

    filepath = file_io.save_team(team)
    dashboard.show_success(f"Team '{args.name}' created -> {filepath}")


def _cmd_team_add(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'team add' command."""
    team = file_io.load_team(args.team)
    if not team:
        dashboard.show_error(f"Team '{args.team}' not found")
        return

    agent = file_io.load_agent(args.agent)
    if not agent:
        dashboard.show_error(f"Agent '{args.agent}' not found")
        return

    team.add_node(args.agent, depends_on=args.depends_on)
    errors = team.validate()
    if errors:
        dashboard.show_error(f"Validation failed: {'; '.join(errors)}")
        return

    filepath = file_io.save_team(team)
    dashboard.show_success(
        f"Agent '{args.agent}' added to team '{args.team}' -> {filepath}"
    )


def _cmd_team_visualize(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'team visualize' command."""
    team = file_io.load_team(args.name)
    if not team:
        dashboard.show_error(f"Team '{args.name}' not found")
        return

    dag_text = team.visualize_ascii()
    dashboard.show_team_dag(dag_text)


def _cmd_team_run(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'team run' command."""
    team = file_io.load_team(args.name)
    if not team:
        dashboard.show_error(f"Team '{args.name}' not found")
        return

    # Load all agents for the team
    agents = {}
    for node in team.nodes:
        agent = file_io.load_agent(node.agent_name)
        if agent:
            agents[agent.name] = agent
        else:
            dashboard.show_error(f"Agent '{node.agent_name}' not found, skipping")

    executor = TeamExecutor(agents=agents)
    log = executor.execute(team)

    summary = log.summary()
    dashboard.show_info(
        f"Team '{args.name}' execution complete: "
        f"{summary['successful']}/{summary['total_executions']} succeeded "
        f"in {summary['total_duration_ms']:.2f}ms"
    )

    for result in log.results:
        status = "OK" if result.success else "FAIL"
        dashboard.show_info(f"  [{status}] {result.executor}: {result.action}")


def _cmd_template_list(dashboard: Dashboard) -> None:
    """Handle 'template list' command."""
    templates = get_builtin_templates()
    template_list = []
    for name, skill in sorted(templates.items()):
        template_list.append({
            "name": name,
            "description": skill.description,
            "param_count": len(skill.parameters),
            "output_count": len(skill.outputs),
        })

    dashboard.show_templates(template_list)


def _cmd_template_apply(args, dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'template apply' command."""
    try:
        skill = apply_template(args.template, args.name)
    except KeyError as e:
        dashboard.show_error(str(e))
        return

    filepath = file_io.save_skill(skill)
    dashboard.show_success(
        f"Skill '{args.name}' created from template '{args.template}' -> {filepath}"
    )


def _cmd_dashboard(dashboard: Dashboard, file_io: FileIO) -> None:
    """Handle 'dashboard' command."""
    dashboard.show_welcome()

    # Show overview
    skill_names = file_io.list_skills()
    agent_names = file_io.list_agents()
    team_names = file_io.list_teams()

    dashboard.show_info(
        f"Skills: {len(skill_names)} | Agents: {len(agent_names)} | Teams: {len(team_names)}"
    )

    # Show skills
    if skill_names:
        skills = []
        for name in skill_names:
            skill = file_io.load_skill(name)
            if skill:
                skills.append(skill.to_dict())
        dashboard.show_skills(skills)

    # Show agents
    if agent_names:
        agents = []
        for name in agent_names:
            agent = file_io.load_agent(name)
            if agent:
                agents.append(agent.to_dict())
        dashboard.show_agents(agents)

    # Show teams
    if team_names:
        teams = []
        for name in team_names:
            team = file_io.load_team(name)
            if team:
                teams.append(team.to_dict())
        dashboard.show_teams(teams)


if __name__ == "__main__":
    sys.exit(main())
