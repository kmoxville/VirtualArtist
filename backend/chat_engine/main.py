import sys
import threading
import logging
from chat_engine import ChatEngine
from config import OPENAI_API_KEY

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("chat_engine")

if __name__ == "__main__":
    logger.info("Starting ChatEngine...")
    chat_engine = ChatEngine(OPENAI_API_KEY)
    chat_engine.start()