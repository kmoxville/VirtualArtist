import os
import tempfile
import numpy as np
import whisper
import torch
import logging
import noisereduce as nr
from faster_whisper import WhisperModel

logger = logging.getLogger("speech_parser")

class WhisperTranscriber:
    def __init__(self, model_name="large"):
        logger.info("Initializing Whisper model...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = WhisperModel(model_name, self.device, compute_type="float16")

        logger.info(f"Model loaded on {self.device}")

        if self.device == "cuda":
            logger.info(f"Number of GPUs: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_name(i)
                logger.info(f"GPU {i}: {gpu_name}")

    def transcribe(self, audio_data, lang):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file.close()

            filename = temp_file.name

            segments, info = self.model.transcribe(
                filename, 
                language=lang,
                temperature=0.2,
                beam_size=5)

            os.remove(temp_file.name)
            
            return " ".join(segment.text for segment in segments)