"""FastAPI application."""

import json as json_module
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from typing import Any

import structlog
from fastapi import FastAPI, File, Form, UploadFile
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field

from simpli_core.connectors import (
    FieldMapping,
    FileConnector,
    SalesforceConnector,
    apply_mappings,
)
from simpli_core.connectors.mapping import CASE_TO_TICKET
from simpli_core.logging import setup_logging
from simpli_template import __version__
from simpli_template.settings import settings


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    """Application startup and shutdown."""
    setup_logging(json_output=settings.app_env != "development")
    log = structlog.get_logger()
    log.info("starting", version=__version__, env=settings.app_env)
    yield
    log.info("shutting_down")


logger = structlog.get_logger()

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


# ---------------------------------------------------------------------------
# Ingest models
# ---------------------------------------------------------------------------


class SalesforceIngestRequest(BaseModel):
    instance_url: str = ""
    client_id: str = ""
    client_secret: str = ""
    soql_where: str = ""
    limit: int = Field(default=100, ge=1, le=10000)
    mappings: list[FieldMapping] | None = None


class IngestResult(BaseModel):
    total: int
    processed: int
    results: list[dict[str, Any]]
    errors: list[dict[str, Any]] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# Ingest routes
# ---------------------------------------------------------------------------


def _detect_format(filename: str | None) -> str:
    if not filename:
        return "csv"
    suffix = filename.rsplit(".", 1)[-1].lower() if "." in filename else "csv"
    return suffix if suffix in FileConnector.SUPPORTED_FORMATS else "csv"


@app.post("/api/v1/ingest", response_model=IngestResult, tags=["ingest"])
async def ingest_file(
    file: UploadFile = File(...),
    mappings: str | None = Form(default=None),
) -> IngestResult:
    """Ingest data from a file upload."""
    logger.info("ingest_file", filename=file.filename)

    records = FileConnector.parse(file.file, format=_detect_format(file.filename))

    field_mappings: list[FieldMapping] | None = None
    if mappings:
        field_mappings = [FieldMapping(**m) for m in json_module.loads(mappings)]

    return await _process_ingest(records, field_mappings, apply_defaults=False)


@app.post(
    "/api/v1/ingest/salesforce", response_model=IngestResult, tags=["ingest"]
)
async def ingest_salesforce(request: SalesforceIngestRequest) -> IngestResult:
    """Pull cases from Salesforce."""
    instance_url = request.instance_url or settings.salesforce_instance_url
    client_id = request.client_id or settings.salesforce_client_id
    client_secret = request.client_secret or settings.salesforce_client_secret

    if not all([instance_url, client_id, client_secret]):
        return JSONResponse(  # type: ignore[return-value]
            status_code=400,
            content={
                "detail": "Salesforce credentials required (instance_url, client_id, client_secret)"
            },
        )

    logger.info("ingest_salesforce", instance_url=instance_url, limit=request.limit)

    connector = SalesforceConnector(
        instance_url=instance_url,
        client_id=client_id,
        client_secret=client_secret,
    )
    records = connector.get_cases(where=request.soql_where, limit=request.limit)

    return await _process_ingest(records, request.mappings)


async def _process_ingest(
    records: list[dict[str, Any]],
    custom_mappings: list[FieldMapping] | None,
    *,
    apply_defaults: bool = True,
) -> IngestResult:
    """Apply mappings and store records."""
    if custom_mappings:
        mapped = apply_mappings(records, custom_mappings)
    elif apply_defaults:
        mapped = apply_mappings(records, CASE_TO_TICKET)
    else:
        mapped = records

    results: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    for i, record in enumerate(mapped):
        try:
            results.append(record)
        except Exception as exc:
            errors.append({"index": i, "error": str(exc), "record": record})

    return IngestResult(
        total=len(records),
        processed=len(results),
        results=results,
        errors=errors,
    )
