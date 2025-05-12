import os
import torch
from bark import SAMPLE_RATE
from bark.generation import (
    load_model,
    preload_models as original_preload,
)
from bark.generation import (
    semantic_to_waveform,
    generate_text_semantic,
    codec_decode,
    generate_coarse,
    generate_fine,
)
from bark.generation import load_codec_model, load_coarse_model, load_fine_model, load_text_semantic_model

class BarkModelLoader:
    def __init__(self, model_path=None):
        self.model_path = model_path or os.getenv("BARK_CACHE_DIR", "~/.cache/suno/bark_v0")
        self.device = "cuda" if torch.cuda.is_available() else "cpu"

    def _safe_load(self, path):
        return torch.load(path, map_location=self.device, weights_only=False)

    def preload(self):
        # ручная подгрузка всех моделей
        load_text_semantic_model(self.device)
        load_coarse_model(self.device)
        load_fine_model(self.device)
        load_codec_model(self.device)