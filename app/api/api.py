from typing import Any

from fastapi import APIRouter, Request

from app.models.predict import PredictRequest, PredictResponse

api_router = APIRouter()


@api_router.post("/predict", response_model=PredictResponse)
async def predict(request: Request, params: PredictRequest) -> Any:
    """
    ML Prediction API
    """
    model = request.app.state.model
    image, audio, duration_s = model.predict(params)

    return PredictResponse(image=image, audio=audio)
