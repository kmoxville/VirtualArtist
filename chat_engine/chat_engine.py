import threading
import logging
from langchain.chat_models import init_chat_model
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
from langchain_core.messages import AIMessage
from langchain_core.messages import HumanMessage
from shared import RabbitMQClient

logger = logging.getLogger("chat_engine")

class ChatEngine:
    def __init__(self, openai_api_key: str):
        self.rabbit_chat_client = RabbitMQClient(RabbitMQClient.CHAT_QUEUE)
        self.rabbit_streamer_client = RabbitMQClient(RabbitMQClient.STREAMER_QUEUE)
        self.openai_api_key = openai_api_key
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")

    def process_chat_message(self, message_body):
        logger.info(f"No implementation yet")

    def process_streamer_message(self, message_body):
        if isinstance(message_body, bytes):
            message_body = message_body.decode("utf-8")
        
        logger.info(f"Processing chat message: {message_body}")
        response = self.model.invoke([HumanMessage(content=message_body)])
        logger.info(f"ChatGPT response: {response.content}")

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