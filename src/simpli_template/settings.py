"""Application settings loaded from environment variables."""

from simpli_core.settings import SimpliSettings


class Settings(SimpliSettings):
    """Application settings with defaults matching .env.example."""


settings = Settings()
