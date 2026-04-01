"""Tests for logging configuration."""

import structlog

from simpli_template.logging import setup_logging


def test_setup_logging_console() -> None:
    setup_logging(json_logs=False)
    log = structlog.get_logger()
    assert log is not None


def test_setup_logging_json() -> None:
    setup_logging(json_logs=True)
    log = structlog.get_logger()
    assert log is not None
