"""Test cases for the __main__ module."""
import logging

import pytest
from _pytest.monkeypatch import MonkeyPatch
from pytest_mock import MockerFixture
from typer.testing import CliRunner

from {{cookiecutter.package_name}}.__main__ import app


@pytest.fixture
def runner() -> CliRunner:
    """Fixture for invoking command-line interfaces."""
    return CliRunner()


def test_main_succeeds(runner: CliRunner) -> None:
    """It exits with a status code of zero."""
    result = runner.invoke(app, ["--version"])
    assert result.exit_code == 0


def test_coloredlogs_config_tty(
    runner: CliRunner, monkeypatch: MonkeyPatch, mocker: MockerFixture
) -> None:
    """Test tty is only set for CI environment."""
    mocked_install = mocker.patch("{{cookiecutter.package_name}}.__main__.coloredlogs.install")

    monkeypatch.delenv("CI", raising=False)
    result = runner.invoke(app, ["--log-level=INFO", "hello"])
    assert result.exit_code == 0
    mocked_install.assert_called_once_with(level=logging.INFO)

    mocked_install.reset_mock()
    monkeypatch.setenv("CI", "true")
    runner.invoke(app, ["--log-level=INFO", "hello"])
    mocked_install.assert_called_once_with(level=logging.INFO, isatty=True)


def test_coloredlogs_log_level_warn(runner: CliRunner) -> None:
    """Test special handling for DEBUG logging."""
    runner.invoke(app, ["--log-level=WARN", "hello"])
    assert logging.getLogger().getEffectiveLevel() == logging.WARN
    assert (
        logging.getLogger("{{cookiecutter.package_name}}.__main__").getEffectiveLevel() == logging.WARN
    )

    # Debug logging should be set only for the main logger, with root logger at INFO
    runner.invoke(app, ["--log-level=DEBUG", "hello"])
    assert logging.getLogger().getEffectiveLevel() == logging.INFO
    assert (
        logging.getLogger("{{cookiecutter.package_name}}.__main__").getEffectiveLevel() == logging.DEBUG
    )
