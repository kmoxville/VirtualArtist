import asyncio
import logging
import threading

from shared import RabbitMQClient
from db.messages_service import MessagesService

logger = logging.getLogger("core")

class StorageService:
    STORAGE_PREFIX = 'storage_'
    QUEUES = [STORAGE_PREFIX + RabbitMQClient.CHAT_QUEUE,
              STORAGE_PREFIX + RabbitMQClient.STREAMER_QUEUE,
              STORAGE_PREFIX + RabbitMQClient.GPT_ANSWERS_QUEUE]

    def __init__(self):
        self.clients = {queue: RabbitMQClient(queue) for queue in self.QUEUES}
        self.threads = []
        self.shutdown_event = threading.Event()

    def consume_chat_messages(self):
        pass

    def process_chat_message(self, message_body):
        pass

    def consume_streamer_messages(self):
        queue_name = StorageService.storage_queue(RabbitMQClient.STREAMER_QUEUE)
        client = self.clients[queue_name]

        while not self.shutdown_event.is_set():
            try:
                client.consume_messages(self.process_streamer_message)
            except Exception as e:
                logger.error(f"Error in streamer consumer: {e}")

    def process_streamer_message(self, message_body):
        if isinstance(message_body, bytes):
            message_body = message_body.decode("utf-8")

        logger.info(f"Streamer message processing started: {message_body}")
        MessagesService.save_message(message_body, "streamer")
        logger.info(f"Streamer message processing ended: {message_body}")

    def consume_gpt_messages(self):
        queue_name = StorageService.storage_queue(RabbitMQClient.GPT_ANSWERS_QUEUE)
        client = self.clients[queue_name]

        while not self.shutdown_event.is_set():
            try:
                client.consume_messages(self.process_gpt_message)
            except Exception as e:
                logger.error(f"Error in streamer consumer: {e}")

    def process_gpt_message(self, message_body):
        if isinstance(message_body, bytes):
            message_body = message_body.decode("utf-8")

        logger.info(f"GPT message processing started: {message_body}")
        MessagesService.save_message(message_body, "gpt")
        logger.info(f"GPT message processing ended: {message_body}")

    def storage_queue(queue_name):
        return "storage_" + queue_name

    def start_consumers(self):
        for queue_name in self.QUEUES:
            if queue_name == StorageService.storage_queue(RabbitMQClient.STREAMER_QUEUE):
                thread = threading.Thread(target=self.consume_streamer_messages)
            elif queue_name == StorageService.storage_queue(RabbitMQClient.CHAT_QUEUE):
                thread = threading.Thread(target=self.consume_chat_messages)
            elif queue_name == StorageService.storage_queue(RabbitMQClient.GPT_ANSWERS_QUEUE):
                thread = threading.Thread(target=self.consume_gpt_messages)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def stop_consumers(self):
        logger.info("Stopping consumers...")
        self.shutdown_event.set()
        for thread in self.threads:
            thread.join()
        logger.info("All consumers stopped.")