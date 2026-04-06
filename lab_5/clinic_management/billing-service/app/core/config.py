from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "billing-service"
    API_PREFIX: str = "/api"
    DATABASE_URL: str
    APPOINTMENT_SERVICE_URL: str
    TREATMENT_SERVICE_URL: str

    model_config = {"env_file": ".env", "extra": "ignore"}


settings = Settings()
