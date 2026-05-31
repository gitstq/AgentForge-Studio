"""
TUI Dashboard - Interactive terminal dashboard using Rich.

Provides a rich terminal interface for browsing skills, agents,
and teams with interactive menus and visual displays.

Requires the 'rich' library (optional dependency).
"""

import sys
from typing import Dict, List, Optional

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    from rich.tree import Tree
    from rich import box
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False


class Dashboard:
    """Interactive TUI dashboard for AgentForge Studio.

    Displays skills, agents, and teams in a rich terminal interface.
    Falls back to plain text output if rich is not available.
    """

    def __init__(self):
        """Initialize the dashboard."""
        if RICH_AVAILABLE:
            self._console = Console()
        else:
            self._console = None

    @property
    def rich_available(self) -> bool:
        """Check if rich library is available."""
        return RICH_AVAILABLE

    def show_welcome(self) -> None:
        """Display the welcome banner."""
        if not RICH_AVAILABLE:
            self._plain_welcome()
            return

        self._console.print()
        self._console.print(Panel(
            Text(
                "  AgentForge Studio v1.0.0\n"
                "  AI Agent Skill Factory & Team Orchestration Engine",
                style="bold cyan",
                justify="center",
            ),
            title="[bold yellow]AgentForge[/bold yellow]",
            subtitle="[dim]Terminal AI Agent Workshop[/dim]",
            box=box.DOUBLE_EDGE,
            padding=(1, 4),
        ))
        self._console.print()

    def _plain_welcome(self) -> None:
        """Plain text welcome banner (fallback)."""
        print()
        print("=" * 60)
        print("  AgentForge Studio v1.0.0")
        print("  AI Agent Skill Factory & Team Orchestration Engine")
        print("=" * 60)
        print()

    def show_skills(self, skills: List[Dict]) -> None:
        """Display a list of skills.

        Args:
            skills: List of skill dictionaries with name, description, version, tags.
        """
        if not RICH_AVAILABLE:
            self._plain_skills(skills)
            return

        table = Table(
            title="[bold cyan]Skills[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Version", style="green")
        table.add_column("Description", style="white")
        table.add_column("Tags", style="yellow")

        for skill in skills:
            tags = ", ".join(skill.get("tags", []))
            table.add_row(
                skill.get("name", ""),
                skill.get("version", "1.0.0"),
                skill.get("description", ""),
                tags,
            )

        self._console.print(table)

    def _plain_skills(self, skills: List[Dict]) -> None:
        """Plain text skills list (fallback)."""
        print("\n--- Skills ---")
        for skill in skills:
            tags = ", ".join(skill.get("tags", []))
            print(f"  {skill.get('name', '')} (v{skill.get('version', '1.0.0')})")
            print(f"    {skill.get('description', '')}")
            if tags:
                print(f"    Tags: {tags}")
        print()

    def show_skill_detail(self, skill: Dict) -> None:
        """Display detailed information about a skill.

        Args:
            skill: Skill dictionary with full details.
        """
        if not RICH_AVAILABLE:
            self._plain_skill_detail(skill)
            return

        # Main info panel
        info_text = (
            f"[bold]Name:[/bold] {skill.get('name', '')}\n"
            f"[bold]Version:[/bold] {skill.get('version', '1.0.0')}\n"
            f"[bold]Description:[/bold] {skill.get('description', '')}\n"
            f"[bold]Tags:[/bold] {', '.join(skill.get('tags', []))}\n"
            f"[bold]Created:[/bold] {skill.get('created_at', 'N/A')}\n"
        )
        self._console.print(Panel(info_text, title="[bold cyan]Skill Details[/bold cyan]", box=box.ROUNDED))

        # Instructions
        instructions = skill.get("instructions", "")
        if instructions:
            self._console.print(Panel(
                instructions[:500] + ("..." if len(instructions) > 500 else ""),
                title="[bold yellow]Instructions[/bold yellow]",
                box=box.ROUNDED,
            ))

        # Parameters table
        params = skill.get("parameters", [])
        if params:
            table = Table(title="Parameters", box=box.SIMPLE)
            table.add_column("Name", style="cyan")
            table.add_column("Type", style="green")
            table.add_column("Required", style="red")
            table.add_column("Default", style="white")
            table.add_column("Description", style="white")
            for p in params:
                table.add_row(
                    p.get("name", ""),
                    p.get("type", ""),
                    "Yes" if p.get("required") else "No",
                    str(p.get("default", "")),
                    p.get("description", ""),
                )
            self._console.print(table)

        # Inputs/Outputs
        for io_type, color in [("inputs", "green"), ("outputs", "blue")]:
            ios = skill.get(io_type, [])
            if ios:
                table = Table(title=f"{io_type.capitalize()}", box=box.SIMPLE)
                table.add_column("Name", style=color)
                table.add_column("Type", style="white")
                table.add_column("Description", style="white")
                for io in ios:
                    table.add_row(io.get("name", ""), io.get("type", ""), io.get("description", ""))
                self._console.print(table)

    def _plain_skill_detail(self, skill: Dict) -> None:
        """Plain text skill detail (fallback)."""
        print(f"\n=== Skill: {skill.get('name', '')} ===")
        print(f"Version: {skill.get('version', '1.0.0')}")
        print(f"Description: {skill.get('description', '')}")
        print(f"Tags: {', '.join(skill.get('tags', []))}")
        print(f"Created: {skill.get('created_at', 'N/A')}")
        print(f"\nInstructions:\n{skill.get('instructions', '')[:500]}")

        params = skill.get("parameters", [])
        if params:
            print("\nParameters:")
            for p in params:
                req = "required" if p.get("required") else "optional"
                print(f"  {p.get('name', '')} ({p.get('type', '')}, {req})")
                if p.get("description"):
                    print(f"    {p.get('description', '')}")

    def show_agents(self, agents: List[Dict]) -> None:
        """Display a list of agents.

        Args:
            agents: List of agent dictionaries.
        """
        if not RICH_AVAILABLE:
            self._plain_agents(agents)
            return

        table = Table(
            title="[bold cyan]Agents[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Role", style="green")
        table.add_column("Model", style="white")
        table.add_column("Skills", style="yellow")
        table.add_column("Temperature", style="white")

        for agent in agents:
            skills = ", ".join(agent.get("skills", []))
            table.add_row(
                agent.get("name", ""),
                agent.get("role", ""),
                agent.get("model", "default"),
                skills or "None",
                str(agent.get("temperature", 0.7)),
            )

        self._console.print(table)

    def _plain_agents(self, agents: List[Dict]) -> None:
        """Plain text agents list (fallback)."""
        print("\n--- Agents ---")
        for agent in agents:
            skills = ", ".join(agent.get("skills", []))
            print(f"  {agent.get('name', '')} - {agent.get('role', '')}")
            print(f"    Model: {agent.get('model', 'default')} | Skills: {skills or 'None'}")
        print()

    def show_teams(self, teams: List[Dict]) -> None:
        """Display a list of teams.

        Args:
            teams: List of team dictionaries.
        """
        if not RICH_AVAILABLE:
            self._plain_teams(teams)
            return

        table = Table(
            title="[bold cyan]Teams[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Agents", style="yellow")
        table.add_column("Nodes", style="white")

        for team in teams:
            nodes = team.get("nodes", [])
            agent_names = [n.get("agent_name", "") for n in nodes]
            table.add_row(
                team.get("name", ""),
                team.get("description", ""),
                ", ".join(agent_names),
                str(len(nodes)),
            )

        self._console.print(table)

    def _plain_teams(self, teams: List[Dict]) -> None:
        """Plain text teams list (fallback)."""
        print("\n--- Teams ---")
        for team in teams:
            nodes = team.get("nodes", [])
            agent_names = [n.get("agent_name", "") for n in nodes]
            print(f"  {team.get('name', '')} - {team.get('description', '')}")
            print(f"    Agents: {', '.join(agent_names)} ({len(nodes)} nodes)")
        print()

    def show_team_dag(self, dag_text: str) -> None:
        """Display a team DAG visualization.

        Args:
            dag_text: ASCII art DAG representation.
        """
        if not RICH_AVAILABLE:
            print(f"\n{dag_text}")
            return

        self._console.print(Panel(
            dag_text,
            title="[bold cyan]Team DAG[/bold cyan]",
            box=box.ROUNDED,
        ))

    def show_test_report(self, report_text: str) -> None:
        """Display a test report.

        Args:
            report_text: Test report text.
        """
        if not RICH_AVAILABLE:
            print(f"\n{report_text}")
            return

        self._console.print(Panel(
            report_text,
            title="[bold cyan]Test Report[/bold cyan]",
            box=box.ROUNDED,
        ))

    def show_templates(self, templates: List[Dict]) -> None:
        """Display available templates.

        Args:
            templates: List of template dictionaries.
        """
        if not RICH_AVAILABLE:
            self._plain_templates(templates)
            return

        table = Table(
            title="[bold cyan]Built-in Templates[/bold cyan]",
            box=box.ROUNDED,
            show_header=True,
            header_style="bold magenta",
        )
        table.add_column("Name", style="cyan", no_wrap=True)
        table.add_column("Description", style="green")
        table.add_column("Parameters", style="yellow")
        table.add_column("Outputs", style="white")

        for tmpl in templates:
            table.add_row(
                tmpl.get("name", ""),
                tmpl.get("description", ""),
                str(tmpl.get("param_count", 0)),
                str(tmpl.get("output_count", 0)),
            )

        self._console.print(table)

    def _plain_templates(self, templates: List[Dict]) -> None:
        """Plain text templates list (fallback)."""
        print("\n--- Built-in Templates ---")
        for tmpl in templates:
            print(f"  {tmpl.get('name', '')} - {tmpl.get('description', '')}")
        print()

    def show_error(self, message: str) -> None:
        """Display an error message.

        Args:
            message: Error message to display.
        """
        if not RICH_AVAILABLE:
            print(f"ERROR: {message}", file=sys.stderr)
            return

        self._console.print(f"[bold red]ERROR:[/bold red] {message}")

    def show_success(self, message: str) -> None:
        """Display a success message.

        Args:
            message: Success message to display.
        """
        if not RICH_AVAILABLE:
            print(f"OK: {message}")
            return

        self._console.print(f"[bold green]OK:[/bold green] {message}")

    def show_info(self, message: str) -> None:
        """Display an info message.

        Args:
            message: Info message to display.
        """
        if not RICH_AVAILABLE:
            print(f"INFO: {message}")
            return

        self._console.print(f"[bold blue]INFO:[/bold blue] {message}")

    def show_menu(self, title: str, options: List[str]) -> None:
        """Display an interactive menu.

        Args:
            title: Menu title.
            options: List of menu options.
        """
        if not RICH_AVAILABLE:
            print(f"\n--- {title} ---")
            for i, opt in enumerate(options, 1):
                print(f"  {i}. {opt}")
            return

        tree = Tree(f"[bold cyan]{title}[/bold cyan]")
        for opt in options:
            tree.add(f"[white]{opt}[/white]")
        self._console.print(tree)
