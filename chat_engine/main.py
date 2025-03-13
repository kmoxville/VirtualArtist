import sys
import threading
import logging
from shared import RabbitMQClient

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)]
)

logger = logging.getLogger("chat_engine")

class ChatEngine:
    def __init__(self):
        self.rabbit_chat_client = RabbitMQClient(RabbitMQClient.CHAT_QUEUE)
        self.rabbit_streamer_client = RabbitMQClient(RabbitMQClient.STREAMER_QUEUE)

    def process_chat_message(self, message_body):
        logger.info(f"Processing chat message: {message_body}")
        logger.info(f"ChatGPT response:")

    def process_streamer_message(self, message_body):
        logger.info(f"Processing streamer message: {message_body}")
        logger.info(f"ChatGPT response:")

    def consume_chat_messages(self):
        self.rabbit_chat_client.consume_messages(self.process_chat_message)

    def consume_streamer_messages(self):
        self.rabbit_streamer_client.consume_messages(self.process_streamer_message)

    def start(self):
        chat_thread = threading.Thread(target=self.consume_chat_messages)
        streamer_thread = threading.Thread(target=self.consume_streamer_messages)

        chat_thread.start()
        streamer_thread.start()

        chat_thread.join()
        streamer_thread.join()


if __name__ == "__main__":
    logger.info("Starting ChatEngine...")
    chat_engine = ChatEngine()
    chat_engine.start()