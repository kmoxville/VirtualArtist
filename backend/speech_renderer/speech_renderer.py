import logging
import io
from bark import generate_audio, preload_models  
import numpy as np
from transformers import AutoProcessor, BarkModel
import scipy.io.wavfile as wav
import os
import torch
#from TTS.api import TTS

from shared import RabbitMQClient

logger = logging.getLogger("speech_renderer")

class SpeechRenderer:
    def __init__(self):
        self.gpt_answers_queue = RabbitMQClient(RabbitMQClient.GPT_ANSWERS_QUEUE, False)
        self.generated_voice_queue = RabbitMQClient(RabbitMQClient.GENERATED_VOICE_QUEUE, False)
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        if True:
            self.processor = AutoProcessor.from_pretrained("suno/bark-small")
            self.model = BarkModel.from_pretrained("suno/bark-small", torch_dtype=torch.float16).to(self.device).to_bettertransformer()
            self.model.enable_cpu_offload()
        else:
            
            self.tts = TTS("tts_models/multilingual/multi-dataset/xtts_v2").to(self.device)
            print(self.tts.speakers)

    def process_gpt_answer(self, message_body):
        if isinstance(message_body, bytes):
            message_body = message_body.decode("utf-8") 

        logger.info(f"Processing chat message: {message_body}")

        if True:
            inputs = self.processor(message_body, voice_preset="v2/ru_speaker_1")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            with torch.no_grad():
                audio_array = self.model.generate(**inputs, do_sample = True, fine_temperature = 0.4, coarse_temperature = 0.8)

            audio_array = audio_array.cpu().numpy().squeeze()
            audio_array /=1.414
            audio_array *= 32767
            audio_array = audio_array.astype(np.int16)
            wav.write("output.wav", rate=24000, data=audio_array)
        else:
            self.tts.tts_to_file(
                text=message_body,
                language="ru",
                speaker="Ana Florence",
                file_path="output.wav"
                )
        
        wav_buffer = io.BytesIO()
        #wav.write(wav_buffer, rate=24000, data=audio_array)
        #wav_buffer.seek(0)

        #self.generated_voice_queue.send_message(wav_buffer.getvalue())

    def start(self):
        self.gpt_answers_queue.consume_messages(self.process_gpt_answer)