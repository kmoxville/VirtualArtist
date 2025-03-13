import logging
import os
import tempfile

from recorder import AudioRecorder
from transcriber import WhisperTranscriber

logger = logging.getLogger("speech_parser")

class SpeechParser:
    def __init__(self, hotkey="`"):
        logger.debug("")
        self.recorder = AudioRecorder(hotkey)
        self.transcriber = WhisperTranscriber()
        self.speech_dir = os.path.join(tempfile.mkdtemp(), "speech_folder")
        os.makedirs(self.speech_dir, exist_ok=True)
        self.speech_file_path = os.path.join(self.speech_dir, "speech.wav")
        
    def run(self):
        while True:
            speech_file = self.recorder.record(self.speech_file_path)
            text = self.transcriber.transcribe(speech_file)
            logger.info(f"Transcribed text: {text}")

            