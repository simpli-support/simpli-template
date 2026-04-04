"""Application settings loaded from environment variables."""

from simpli_core.connectors.settings import SalesforceSettings
from simpli_core.settings import CustomFieldSettings, SimpliSettings


class Settings(SimpliSettings, SalesforceSettings, CustomFieldSettings):
    """Application settings with defaults matching .env.example."""

    app_port: int = 8019


settings = Settings()
