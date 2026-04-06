from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "appointment-service"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    PATIENT_SERVICE_URL: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
