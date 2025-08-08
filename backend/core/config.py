import json
from typing import Any, List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    BACKEND_CORS_ORIGINS: Any
    API_PREFIX: str

    # Database settings.
    DATABASE_URL: str   
    DATABASE_NAME: str

    # Bucket to store coverage files.
    BUCKET_NAME: str

    # Mailgun settings.
    MAILGUN_API_KEY: str
    MAILGUN_DOMAIN: str
    
    # Redis settings for Celery
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    MAILGUN_FROM_EMAIL: str

    # Model configuration.
    model_config = SettingsConfigDict(
        extra="allow",
        env_file=".env",
        case_sensitive=True
    )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, value: Union[str, List[str]]) -> Union[List[str], str]:
        """ Create the final list to allow specific origins.

        :param value: Values obtained from environment variables.
        """
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, str):
            parsed = json.loads(value)
            return parsed
        raise ValueError(value)


settings = Settings()
