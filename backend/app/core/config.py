from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str
    
    CLERK_ISSUER_URL: str
    CLERK_JWKS_URL: str
    CLERK_WEBHOOK_SECRET : str

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )


settings = Settings()