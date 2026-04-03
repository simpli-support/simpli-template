# Simpli Template

Starter template for creating new [Simpli Support](https://simpli.support) microservices. Clone this repo and rename to bootstrap a new service with the standard project structure.

## What's included

- FastAPI application using `create_app()` from simpli-core
- Settings class extending `SimpliSettings`
- Typer CLI with `serve` and `version` commands
- Dockerfile with multi-stage Python 3.12 build
- GitHub Actions CI (ruff + mypy + pytest)
- `.env.example` with common configuration

## Quick start

```bash
cp .env.example .env
pip install -e ".[dev]"
simpli-template serve
```

## Development

```bash
pytest tests/ -q
ruff check .
ruff format --check .
mypy src/
```

## Docker

```bash
docker build -t simpli-template .
docker run -p 8000:8000 simpli-template
```

## License

MIT
