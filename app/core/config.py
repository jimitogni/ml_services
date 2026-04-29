from functools import lru_cache

from pydantic import BaseModel


class Settings(BaseModel):
    service_name: str = "clinic-ml-service"
    api_title: str = "Clinic ML Service"
    model_version: str = "v0.1-rule-based"


@lru_cache
def get_settings() -> Settings:
    return Settings()
