import os
from dotenv import load_dotenv

load_dotenv()

RABBITMQ_USER = os.getenv("RABBITMQ_USER")
RABBITMQ_PASSWORD = os.getenv("RABBITMQ_PASSWORD")

def get_connection_string() -> str:
    if os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true":
        return f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@rabbitmq:5672"
    else:
        return f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASSWORD}@localhost:5672"