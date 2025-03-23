import time
import pika
import logging
import os

logger = logging.getLogger("rabbitmq_client")

class RabbitMQClient:

    AUDIO_QUEUE = "audio_queue"
    STREAMER_QUEUE = "chat_engine_streamer_messages"
    CHAT_QUEUE = "chat_engine_chat_messages"
    
    def __init__(self, queue_name="", save_to_storage: bool = False):
        self.queue_name = queue_name
        self.connection = None
        self.channel = None
        self.user = os.getenv("RABBITMQ_USER")
        self.password = os.getenv("RABBITMQ_PASSWORD")
        self.max_retries = 5
        self.retry_delay = 3
        self.send_to_storage = save_to_storage

        if save_to_storage:
            self.storage_client = RabbitMQClient("storage_" + queue_name)


    def get_connection_string(self) -> str:
        if os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true":
            return f"amqp://{self.user}:{self.password}@rabbitmq:5672"
        else:
            return f"amqp://{self.user}:{self.password}@localhost:5672"
        
    
    def setup_queues(self):
        logger.info("Queues setup started")
        connection = pika.BlockingConnection(pika.URLParameters(self.get_connection_string()))
        channel = connection.channel()

        channel.queue_declare(queue=self.AUDIO_QUEUE, durable=True)
        channel.queue_declare(queue=self.STREAMER_QUEUE, durable=True)
        channel.queue_declare(queue=self.CHAT_QUEUE, durable=True)

        channel.queue_declare(queue='storage_'+self.STREAMER_QUEUE, durable=True)
        channel.queue_declare(queue='storage_'+self.CHAT_QUEUE, durable=True)

        connection.close()
        logger.info("Queues setup ended")


    def connect(self):
        retries = 0
        while retries < self.max_retries:
            try:
                parameters = pika.URLParameters(self.get_connection_string())
                self.connection = pika.BlockingConnection(parameters)
                self.channel = self.connection.channel()
                self.channel.queue_declare(queue=self.queue_name, durable=True)
                logger.info(f"Connected to RabbitMQ, queue: {self.queue_name}")
                return
            except pika.exceptions.AMQPConnectionError as e:
                retries += 1
                logger.error(f"Connection attempt {retries} failed: {e}")
                if retries >= self.max_retries:
                    logger.critical("Max retries reached. Could not connect to RabbitMQ.")
                    raise
                else:
                    logger.info(f"Retrying in {self.retry_delay} seconds...")
                    time.sleep(self.retry_delay)


    def send_message(self, message: bytes, send_to_storage: bool = False):
        if not self.channel:
            self.connect()

        try:
            self.channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=message,
                properties=pika.BasicProperties(delivery_mode=2)
            )
            logger.info(f"Sent message to {self.queue_name}")
        except Exception as e:
            logger.error(f"Failed to send message: {e}")
            self.connect()
            self.send_message(message)

        if send_to_storage:
            self.storage_client.send_message(message)


    def consume_messages(self, callback):
        if not self.channel:
            self.connect()

        def wrapper(ch, method, properties, body):
            callback(body)
            ch.basic_ack(delivery_tag=method.delivery_tag)

        try:
            self.channel.basic_consume(queue=self.queue_name, on_message_callback=wrapper)
            logger.info(f"Listening for messages on {self.queue_name}...")
            self.channel.start_consuming()
        except pika.exceptions.AMQPConnectionError as e:
            logger.error(f"Connection error while consuming messages: {e}")
            self.connect()
            self.consume_messages(callback)


    def close(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
            logger.info("RabbitMQ connection closed.")