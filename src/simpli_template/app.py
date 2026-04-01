"""FastAPI application."""

from fastapi import FastAPI

app = FastAPI(
    title="Simpli Template",
    version="0.1.0",
    description="Simpli Support template project",
)


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}
