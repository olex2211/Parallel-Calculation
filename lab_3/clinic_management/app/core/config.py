from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "Clinic Management API"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    model_config = {"env_file": ".env", "extra": "ignore"}

settings = Settings()
