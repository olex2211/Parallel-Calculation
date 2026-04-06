from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "appointment-service"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    PATIENT_SERVICE_URL: str
    REDIS_URL: str = "redis://localhost:6379/1"
    CACHE_TTL: int = 60 * 5

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
