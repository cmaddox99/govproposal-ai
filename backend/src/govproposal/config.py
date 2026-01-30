"""Application configuration using pydantic-settings."""

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

    # Database
    postgres_host: str = "localhost"
    postgres_port: int = 5433
    postgres_user: str = "govproposal"
    postgres_password: str = "devpassword"
    postgres_db: str = "govproposal"

    @property
    def postgres_url(self) -> str:
        """Build PostgreSQL connection URL."""
        return (
            f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    # JWT
    jwt_secret_key: str = "dev-secret-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 15
    jwt_refresh_token_expire_days: int = 7

    # MFA
    mfa_issuer_name: str = "GovProposalAI"

    # External APIs
    anthropic_api_key: str = ""
    anthropic_model: str = "claude-sonnet-4-20250514"
    sam_api_key: str = ""

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
