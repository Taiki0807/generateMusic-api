import typing as T

from pydantic import BaseModel, Field, StrictStr


class PredictResponse(BaseModel):
    image: str = Field(title="image", description="Predicted spectrogram image")
    audio: str = Field(title="audio", description="Predicted audio in MP3 format")


class StartParams(BaseModel):
    prompt: StrictStr = Field(..., title="prompt", description="Text prompt for the start point")
    seed: int = Field(..., title="seed", description="Random seed for denoising at the start point")
    negative_prompt: T.Optional[str] = Field(
        None, title="negative_prompt", description="Negative prompt to avoid at the start point"
    )
    denoising: float = Field(0.75, title="denoising", description="Denoising strength at the start point")
    guidance: float = Field(7.0, title="guidance", description="Classifier-free guidance strength at the start point")


class EndParams(BaseModel):
    prompt: StrictStr = Field(..., title="prompt", description="Text prompt for the end point")
    seed: int = Field(..., title="seed", description="Random seed for denoising at the end point")
    negative_prompt: T.Optional[str] = Field(
        None, title="negative_prompt", description="Negative prompt to avoid at the end point"
    )
    denoising: float = Field(0.75, title="denoising", description="Denoising strength at the end point")
    guidance: float = Field(7.0, title="guidance", description="Classifier-free guidance strength at the end point")


class PredictRequest(BaseModel):
    start: StartParams = Field(
        ...,
        title="Start parameters",
        description="Parameters for the start point",
    )
    end: EndParams = Field(
        ...,
        title="End parameters",
        description="Parameters for the end point",
    )
    alpha: float = Field(
        0.5,
        title="alpha",
        description="Interpolation alpha [0, 1]. A value of 0 uses start fully, a value of 1 uses end fully.",
    )
    num_inference_steps: int = Field(
        50, title="num_inference_steps", description="Number of inner loops of the diffusion model"
    )
    seed_image_id: StrictStr = Field("og_beat", title="seed_image_id", description="Which seed image to use")
    mask_image_id: T.Optional[str] = Field(None, title="mask_image_id", description="ID of mask image to use")
