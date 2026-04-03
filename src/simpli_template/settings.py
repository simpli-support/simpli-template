"""Application settings loaded from environment variables."""

from simpli_core.connectors.settings import SalesforceSettings
from simpli_core.settings import SimpliSettings


class Settings(SimpliSettings, SalesforceSettings):
    """Application settings with defaults matching .env.example."""

    app_port: int = 8019


settings = Settings()
