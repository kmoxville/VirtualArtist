import io
import logging

from transcriber import WhisperTranscriber


logger = logging.getLogger("speech_parser")

class SpeechParser:
    def __init__(self):
        self.connection = None
        self.channel = None
        self.transcriber = WhisperTranscriber("medium")


    def process_audio(self, body):
        text = self.transcriber.transcribe(body)
        logger.info(f"Transcribed text: {text}")