import logging
import sys

from config import MAIN_LANG
from shared import RabbitMQClient
from speech_parser import SpeechParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("speech_parser")

if __name__ == "__main__":
    logger.info("Starting SpeechParser...")

    rabbit_client = RabbitMQClient(RabbitMQClient.AUDIO_QUEUE)
    speech_parser = SpeechParser(MAIN_LANG)

    rabbit_client.consume_messages(speech_parser.process_audio)