"""CLI interface."""

import typer
import uvicorn

from simpli_template.settings import settings

app = typer.Typer(help="Simpli Template CLI")


@app.command()
def serve(
    host: str = typer.Option(settings.app_host, help="Bind host"),
    port: int = typer.Option(settings.app_port, help="Bind port"),
    reload: bool = typer.Option(settings.app_debug, help="Enable auto-reload"),
) -> None:
    """Start the API server."""
    uvicorn.run(
        "simpli_template.app:app",
        host=host,
        port=port,
        reload=reload,
        log_level=settings.app_log_level,
    )


@app.command()
def version() -> None:
    """Show version."""
    from simpli_template import __version__

    typer.echo(f"simpli-template {__version__}")
