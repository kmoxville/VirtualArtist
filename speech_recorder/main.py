import logging
import sys

from shared import RabbitMQClient
from audio_recorder import AudioRecorder


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("speech_recorder")

if __name__ == "__main__":
    logger.info("Starting SpeechRecorder...")

    rabbitmq_client = RabbitMQClient(RabbitMQClient.AUDIO_QUEUE)
    recorder = AudioRecorder()

    while True:
        audio_data = recorder.record_audio()
        rabbitmq_client.send_message(audio_data)