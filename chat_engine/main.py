import time
import pika
import shared


def on_message_from_streamer(ch, method, properties, body):
    print(f" [🎤] Streamer message received: {body.decode()}")

def on_message_from_chat(ch, method, properties, body):
    print(f" [💬] Chat message received: {body.decode()}")


def main():
    try:
        print(" [🔌] Connecting to RabbitMQ...")

        connection = pika.BlockingConnection(pika.URLParameters(shared.get_connection_string()))
        channel = connection.channel()

        channel.basic_consume(
            queue='chat_engine_streamer_messages', 
            on_message_callback=on_message_from_streamer, 
            auto_ack=True
        )

        channel.basic_consume(
            queue='chat_engine_chat_messages', 
            on_message_callback=on_message_from_chat, 
            auto_ack=True
            )
        
        print(" [✅] Waiting for messages. To exit press CTRL+C")
        channel.start_consuming()
    
    except pika.exceptions.AMQPConnectionError as e:
        print(f" [⚠️] Connection failed: {e}. Retrying in 5 seconds...")
        time.sleep(5)
    except Exception as e:
            print(f" [❌] Unexpected error: {e}")


if __name__ == "__main__":
    main()
