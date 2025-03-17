import logging

from transcriber import WhisperTranscriber
from shared import RabbitMQClient


logger = logging.getLogger("speech_parser")

class SpeechParser:
    def __init__(self, lang: str):
        self.connection = None
        self.channel = None
        self.transcriber = WhisperTranscriber("medium")
        self.streamer_queue = RabbitMQClient(RabbitMQClient.STREAMER_QUEUE)
        self.lang = lang


    def process_audio(self, body):
        text = self.transcriber.transcribe(body, self.lang)
        logger.info(f"Transcribed text: {text}")
        self.streamer_queue.send_message(text)
