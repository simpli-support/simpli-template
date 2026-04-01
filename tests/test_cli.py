"""Tests for the CLI interface."""

from typer.testing import CliRunner

from simpli_template import __version__
from simpli_template.cli import app

runner = CliRunner()


def test_version() -> None:
    result = runner.invoke(app, ["version"])
    assert result.exit_code == 0
    assert __version__ in result.output
