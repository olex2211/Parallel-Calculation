from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "patient-service"
    API_PREFIX: str = "/api"
    DATABASE_URL: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
