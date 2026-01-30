"""Application configuration using pydantic-settings."""

from typing import List, Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    # Application
    app_name: str = "GovProposalAI"
    version: str = "0.1.0"
    environment: str = "development"
    debug: bool = True

    # API
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    # CORS
    cors_origins: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    # Database - supports both individual vars and DATABASE_URL
    database_url: Optional[str] = None
    postgres_host: str = "localhost"
    postgres_port: int = 5432
    postgres_user: str = "govproposal"
    postgres_password: str = "devpassword"
    postgres_db: str = "govproposal"

    @property
    def postgres_url(self) -> str:
        """Build PostgreSQL connection URL."""
        if self.database_url:
            return self.database_url
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # JWT
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 30
    jwt_refresh_token_expire_days: int = 7

    # MFA
    mfa_issuer_name: str = "GovProposalAI"

    # Redis
    redis_url: Optional[str] = None

    # External APIs
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    sam_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8", "extra": "ignore"}


settings = Settings()
