import io
from pydantic import BaseModel
import os
import sys
import shutil
from pathlib import Path
from typing import Optional

import numpy as np
import PIL
import torch

models_path = Path("..") / "models"
sys.path.append(str(models_path.resolve()))

from app.services.riffusion.datatypes import InferenceInput, PromptInput
from app.services.riffusion.riffusion_pipeline import RiffusionPipeline
from app.services.riffusion.spectrogram_image_converter import SpectrogramImageConverter
from app.services.riffusion.spectrogram_params import SpectrogramParams
from app.services.riffusion.util import base64_util

sys.path.remove(str(models_path.resolve()))

MODEL_ID = "riffusion/riffusion-model-v1"
MODEL_CACHE = "riffusion-cache"

if os.path.exists(MODEL_CACHE):
    shutil.rmtree(MODEL_CACHE)
os.makedirs(MODEL_CACHE)

device = "cuda" if torch.cuda.is_available() else "cpu"

model = RiffusionPipeline.load_checkpoint(
    checkpoint=MODEL_ID,
    use_traced_unet=True,
    device=device,
    cache_dir=MODEL_CACHE,
)

class Item(BaseModel):
    prompt_a: str
    denoising: Optional[float] = 0.75
    prompt_b: Optional[str] = None
    alpha: Optional[float] = 0.5
    num_inference_steps: Optional[int] = 50
    seed_image_id: Optional[str] = "vibes"

def predict(item, run_id, logger):
    item = Item(**item)

    init_image_path = f"./seed_images/{item.seed_image_id}.png"
    init_image = PIL.Image.open(str(init_image_path)).convert("RGB")

    # fake max ints
    seed_a = np.random.randint(0, 2147483647)
    seed_b = np.random.randint(0, 2147483647)

    start = PromptInput(prompt=item.prompt_a, seed=seed_a, denoising=item.denoising)
    if not item.prompt_b:  # no transition
        prompt_b = item.prompt_a
        alpha = 0
    end = PromptInput(prompt=prompt_b, seed=seed_b, denoising=item.denoising)
    riffusion_input = InferenceInput(
        start=start,
        end=end,
        alpha=alpha,
        num_inference_steps=item.num_inference_steps,
        seed_image_id=item.seed_image_id,
    )

    # Execute the model to get the spectrogram image
    image = model.riffuse(riffusion_input, init_image=init_image, mask_image=None)

    # Reconstruct audio from the image
    params = SpectrogramParams(min_frequency=0, max_frequency=10000)
    converter = SpectrogramImageConverter(params=params, device=device)
    segment = converter.audio_from_spectrogram_image(image)

    # Export audio to MP3 bytes
    mp3_bytes = io.BytesIO()
    segment.export(mp3_bytes, format="mp3")
    mp3_bytes.seek(0)

    # Export image to JPEG bytes
    image_bytes = io.BytesIO()
    image.save(image_bytes, exif=image.getexif(), format="JPEG")
    image_bytes.seek(0)

    # Assemble the output dataclass
    image = "data:image/jpeg;base64," + base64_util.encode(image_bytes)
    audio = "data:audio/mpeg;base64," + base64_util.encode(mp3_bytes)


    return {"result": "Audio Generated","image":image,"audio":audio}
