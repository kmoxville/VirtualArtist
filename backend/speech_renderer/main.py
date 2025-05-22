import logging
import sys

from shared import RabbitMQClient
from speech_renderer import SpeechRenderer
#from bark_model_loader import BarkModelLoader


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("speech_renderer")


if __name__ == "__main__":
    logger.info("Starting SpeechRenderer...")

    #loader = BarkModelLoader()
    #loader.preload()

    rabbit_client = RabbitMQClient(RabbitMQClient.AUDIO_QUEUE)
    speech_parser = SpeechRenderer()
    speech_parser.start()