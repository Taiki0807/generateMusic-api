import io
from abc import ABC, abstractmethod
from pathlib import Path
from typing import Any, Optional

import PIL.Image

from app.services.riffusion.riffusion_pipeline import RiffusionPipeline
from app.services.riffusion.spectrogram_image_converter import SpectrogramImageConverter, SpectrogramParams
from app.services.riffusion.util import base64_util


class BaseMLModel(ABC):
    @abstractmethod
    def predict(self, req: Any) -> Any:
        raise NotImplementedError


class MLModel(BaseMLModel):
    """Sample ML model"""

    def __init__(self, seed_images_dir, checkpoint, device):
        print(checkpoint)
        global PIPELINE
        self.PIPELINE = RiffusionPipeline.load_checkpoint(
            checkpoint=checkpoint,
            use_traced_unet=not False,
            device=device,
        )
        self.seed_images_dir = seed_images_dir

    def predict(self, inputs):
        # Load the seed image by ID
        print(inputs.seed_image_id)
        init_image_path = Path(self.seed_images_dir, f"{inputs.seed_image_id}.png")
        if not init_image_path.is_file():
            return {"error": f"Invalid seed image: {inputs.seed_image_id}"}

        init_image = PIL.Image.open(str(init_image_path)).convert("RGB")

        # Load the mask image by ID
        mask_image: Optional[PIL.Image.Image] = None
        if inputs.mask_image_id:
            mask_image_path = Path(self.seed_images_dir, f"{inputs.mask_image_id}.png")
            if not mask_image_path.is_file():
                return {"error": f"Invalid mask image: {inputs.mask_image_id}"}
            mask_image = PIL.Image.open(str(mask_image_path)).convert("RGB")

        # Execute the model to get the spectrogram image
        image = self.PIPELINE.riffuse(inputs, init_image=init_image, mask_image=mask_image)

        # Reconstruct audio from the image
        params = SpectrogramParams(min_frequency=0, max_frequency=10000)
        converter = SpectrogramImageConverter(params=params, device=str(self.PIPELINE.device))
        segment = converter.audio_from_spectrogram_image(image, apply_filters=True)

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
        duration_s = segment.duration_seconds
        return image, audio, duration_s
