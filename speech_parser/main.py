import logging
import sys

from speech_parser import SpeechParser

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("speech_parser")

if __name__ == "__main__":
    logger.info("Starting SpeechParser...")
    speech_parser = SpeechParser()
    speech_parser.run()