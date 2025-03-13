import os
import tempfile
import numpy as np
import whisper
import torch
import logging
import noisereduce as nr

logger = logging.getLogger("speech_parser")

class WhisperTranscriber:
    def __init__(self, model_name="medium"):
        logger.info("Initializing Whisper model...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.model = whisper.load_model(model_name).to(self.device)

        logger.info(f"Model loaded on {self.device}")

        if self.device == "cuda":
            logger.info(f"Number of GPUs: {torch.cuda.device_count()}")
            for i in range(torch.cuda.device_count()):
                gpu_name = torch.cuda.get_device_name(i)
                logger.info(f"GPU {i}: {gpu_name}")

    
    def transcribe(self, audio_data):
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(audio_data)
            temp_file.close()

            filename = temp_file.name

            audio = whisper.load_audio(filename)
            audio = whisper.pad_or_trim(audio)
            mel = whisper.log_mel_spectrogram(audio).to(self.device)
            
            options = whisper.DecodingOptions(fp16=False, beam_size=5)
            result = whisper.decode(self.model, mel, options)
            result = self.model.transcribe(filename)

            os.remove(temp_file.name)
            
            return result["text"]