"""FastAPI application."""

from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

import structlog
from fastapi import FastAPI

from simpli_template import __version__
from simpli_core.logging import setup_logging
from simpli_template.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application startup and shutdown."""
    setup_logging(json_output=settings.app_env != "development")
    log = structlog.get_logger()
    log.info("starting", version=__version__, env=settings.app_env)
    yield
    log.info("shutting_down")


app = FastAPI(
    title="Simpli Template",
    version=__version__,
    description="Simpli Support template project",
    lifespan=lifespan,
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
