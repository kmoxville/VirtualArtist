import os
import tempfile
import wave
import keyboard
import pyaudio
import logging


logger = logging.getLogger("speech_recorder")

class AudioRecorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    
    
    def __init__(self, hotkey="F7"):
        self.hotkey = hotkey


    def record_audio(self):
        audio = pyaudio.PyAudio()
        stream = audio.open(format=self.FORMAT, channels=self.CHANNELS,
                            rate=self.RATE, input=True,
                            frames_per_buffer=self.CHUNK)
        frames = []

        logger.info("Waiting for hotkey...")
        keyboard.wait(self.hotkey)

        logger.info("Recording started...")
        while keyboard.is_pressed(self.hotkey):
            frames.append(stream.read(self.CHUNK))

        stream.stop_stream()
        stream.close()
        audio.terminate()
        logger.info("Recording stopped.")

        with tempfile.NamedTemporaryFile(delete=False, suffix='wav') as temp_file:
            with wave.open(temp_file, "wb") as wf:
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(audio.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(frames))

            with open(temp_file.name, 'rb') as file:
                audio_data = file.read()

        os.remove(temp_file.name)

        return audio_data