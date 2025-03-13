import keyboard
import pyaudio
import wave
import os
import logging


logger = logging.getLogger("speech_parser")

class AudioRecorder:
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024
    
    def __init__(self, hotkey="`"):
        self.hotkey = hotkey
    
    def record(self, output_path):
        if os.path.exists(output_path):
            os.remove(output_path)

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
        
        with wave.open(output_path, "wb") as wf:
            wf.setnchannels(self.CHANNELS)
            wf.setsampwidth(audio.get_sample_size(self.FORMAT))
            wf.setframerate(self.RATE)
            wf.writeframes(b''.join(frames))

        return output_path