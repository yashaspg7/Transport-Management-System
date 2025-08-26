#!/usr/bin/env python3
import os
import subprocess
import sys
import time

from rich.align import Align
from rich.console import Console
from rich.panel import Panel
from rich.text import Text

# --- Configuration ---
CI_COMMANDS = [
    # {"cmd": "uv run ruff check . --fix", "desc": "Linting code with Ruff"},
    {"cmd": "uv run ruff check --select I --fix", "desc": "Organizing imports"},
    {"cmd": "uv run ruff format .", "desc": "Formatting code with Ruff"},
    {"cmd": "uv run pytest", "desc": "Running tests with Pytest"},
    {"cmd": "hurl tests/hurl/ --test", "desc": "Tests API with hurl"},
    {"cmd": "hurl scripts/seed_data.hurl", "desc": "Seeds the data to api"},
    {"cmd": "hurl scripts/cleanup_data.hurl", "desc": "Cleans up the data"},
    {"cmd": "uv run pyright .", "desc": "Type checking with Pyright"},
]

# Initialize the rich console
console = Console()


def run_command(command: str, timeout: int = 300) -> tuple[bool, str]:
    """
    Runs a command, captures its output, and preserves colors.
    """
    try:
        env = os.environ.copy()
        env["FORCE_COLOR"] = "1"
        env["PY_COLORS"] = "1"

        color_command = command
        if "pytest" in command and "--color=" not in command:
            color_command += " --color=yes"

        process = subprocess.run(
            color_command,
            shell=True,
            capture_output=True,
            text=True,
            timeout=timeout,
            env=env,
        )
        return process.returncode == 0, process.stdout + process.stderr
    except subprocess.TimeoutExpired:
        return False, f"Command timed out after {timeout} seconds."


def main() -> None:
    """Runs the CI checks with a sequential, pipeline-style output."""
    os.system("cls" if os.name == "nt" else "clear")

    total_steps = len(CI_COMMANDS)
    console.print(
        Panel(
            Align.center(f"🚀 Starting CI Pipeline ({total_steps} steps)"),
            style="bold blue",
            expand=True,  # This makes the panel full-width for centering
        )
    )

    start_time = time.time()

    for i, step in enumerate(CI_COMMANDS, 1):
        command = step["cmd"]
        description = step["desc"]
        step_info = f"Step {i}/{total_steps}"

        with console.status(
            f"[bold yellow]{step_info}: {description}...[/bold yellow]", spinner="dots"
        ):
            success, output = run_command(command)

        if success:
            console.print(
                f"✅ [bold green]{step_info} Passed[/bold green]: {description}"
            )
        else:
            console.print(f"❌ [bold red]{step_info} Failed[/bold red]: {command}")
            console.print("     [red]↓[/red]")

            error_panel = Panel(
                Text.from_ansi(output.strip()),
                title="[bold red]Error Output[/bold red]",
                border_style="red",
            )
            console.print(error_panel)
            sys.exit(1)

        if i < total_steps:
            console.print("     [blue]↓[/blue]")

    total_time = f"{time.time() - start_time:.2f}"
    console.print(
        Panel(
            Align.center(
                f"✅ All {total_steps} checks passed successfully in {total_time}s!"
            ),
            style="bold green",
        )
    )


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        console.print("\n[yellow]Pipeline cancelled by user.[/yellow]")
        sys.exit(1)
