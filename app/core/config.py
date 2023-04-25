from pydantic import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "FastAPI Template"
    API_V1_STR: str = "/api/v1"
    checkpoint: str = "riffusion/riffusion-model-v1"
    device: str = "cuda"

    class Config:
        case_sensitive = True


settings = Settings()
