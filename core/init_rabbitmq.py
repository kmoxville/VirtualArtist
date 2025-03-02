import pika
import shared


async def setup_queues():
    connection = pika.BlockingConnection(pika.URLParameters(shared.get_connection_string()))
    channel = connection.channel()

    channel.queue_declare(queue="chat_engine_streamer_messages", durable=True)
    channel.queue_declare(queue="chat_engine_chat_messages", durable=True)

    connection.close()

if __name__ == "__main__":
    setup_queues()