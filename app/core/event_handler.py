from typing import Callable

from fastapi import FastAPI

from app.services.model import MLModel


def _startup_model(app: FastAPI, checkpoint: str, device: str) -> None:
    model_instance = MLModel(seed_images_dir="seed_images", checkpoint=checkpoint, device=device)
    app.state.model = model_instance


def _shutdown_model(app: FastAPI) -> None:
    app.state.model = None


def start_app_handler(app: FastAPI, checkpoint: str, device: str) -> Callable:
    def startup() -> None:
        _startup_model(app, checkpoint, device)

    return startup


def stop_app_handler(app: FastAPI) -> Callable:
    def shutdown() -> None:
        _shutdown_model(app)

    return shutdown
