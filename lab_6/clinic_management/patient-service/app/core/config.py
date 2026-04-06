from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "patient-service"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    REDIS_URL: str = "redis://localhost:6379/0"
    CACHE_TTL: int = 60 * 5

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
