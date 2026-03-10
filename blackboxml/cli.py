"""bbml — BlackBoxML command-line interface."""

import json
import logging

import click

from blackboxml.store import delete_all_runs, list_runs

logger = logging.getLogger("blackboxml")


def _format_duration(seconds: float | None) -> str:
    """Convert seconds to a human-readable string like '13m 46s'."""
    if seconds is None:
        return "-"
    total = int(seconds)
    if total < 60:
        return f"{total}s"
    minutes, secs = divmod(total, 60)
    if minutes < 60:
        return f"{minutes}m {secs}s"
    hours, minutes = divmod(minutes, 60)
    return f"{hours}h {minutes}m {secs}s"


def _format_date(iso_timestamp: str | None) -> str:
    """Extract a short date string from an ISO timestamp."""
    if not iso_timestamp:
        return "-"
    return iso_timestamp.replace("T", " ")[:19]


@click.group()
def main() -> None:
    """bbml — BlackBoxML CLI for inspecting training runs."""


@main.command()
def runs() -> None:
    """List all logged runs."""
    all_runs = list_runs()
    if not all_runs:
        click.echo("no runs found.")
        return

    # Column widths
    w_name = max(len(r.get("name", "")) for r in all_runs)
    w_name = max(w_name, 4)  # minimum width for header "NAME"
    w_date = 19  # "YYYY-MM-DD HH:MM:SS"
    w_dur = 12
    w_steps = 5
    # tags get the rest

    header = (
        f"{'NAME':<{w_name}}  "
        f"{'DATE':<{w_date}}  "
        f"{'DURATION':>{w_dur}}  "
        f"{'STEPS':>{w_steps}}  "
        f"TAGS"
    )
    click.echo(header)
    click.echo("-" * len(header))

    for run in all_runs:
        name = run.get("name", "")
        date = _format_date(run.get("start"))
        duration = _format_duration(run.get("duration_seconds"))
        step_data = run.get("steps", [])
        steps = str(len(step_data)) if isinstance(step_data, list) else "-"
        tags = ", ".join(run.get("tags", []))

        line = (
            f"{name:<{w_name}}  "
            f"{date:<{w_date}}  "
            f"{duration:>{w_dur}}  "
            f"{steps:>{w_steps}}  "
            f"{tags}"
        )
        click.echo(line)


@main.command()
@click.argument("run_name")
def show(run_name: str) -> None:
    """Pretty-print a run by name."""
    all_runs = list_runs()
    for run in all_runs:
        if run.get("name") == run_name:
            click.echo(json.dumps(run, indent=2))
            return

    click.echo(f"run not found: {run_name}")


@main.command()
def clean() -> None:
    """Delete all logged runs."""
    if not click.confirm("delete all runs?", default=False):
        return

    count = delete_all_runs()
    click.echo(f"deleted {count} run(s).")
