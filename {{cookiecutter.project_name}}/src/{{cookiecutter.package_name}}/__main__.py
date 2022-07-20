"""Command-line interface."""
import logging
import os
from typing import Optional

import coloredlogs  # type: ignore
import typer

from {{cookiecutter.package_name}} import __version__


logger = logging.getLogger("{{cookiecutter.package_name}}")
app = typer.Typer()


def version_callback(value: bool) -> None:
    """Prints current version and exits."""
    if value:
        typer.echo(f"{{cookiecutter.project_name}}: {__version__}")
        raise typer.Exit()


@app.callback()
def cli(
    version: Optional[bool] = typer.Option(  # noqa: B008, F841
        None, "--version", callback=version_callback, is_eager=True
    ),
    log_level: str = "INFO",
) -> None:
    """Command-line interface."""
    coloredlogs_args = {}
    if os.getenv("CI"):
        # force tty for colors when running in CI
        coloredlogs_args["isatty"] = True
    level = coloredlogs.level_to_number(log_level.upper())
    if level > logging.DEBUG:
        coloredlogs.install(level=level, **coloredlogs_args)
    else:
        # Only set DEBUG level for the CLI logger and keep other loggers at INFO
        coloredlogs.install(level="INFO", **coloredlogs_args)
        logger.propagate = False
        coloredlogs.install(logger=logger, level=level, **coloredlogs_args)


# Sample typer subcommand 'hello'
# @app.command()
# def hello() -> None:
#     """sample command hello"""
#     logging.info("Hello")


def main() -> None:
    """Main entrypoint."""
    app()


if __name__ == "__main__":
    app()
