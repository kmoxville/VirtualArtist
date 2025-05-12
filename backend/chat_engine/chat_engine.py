import threading
import logging
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langgraph.checkpoint.postgres import PostgresSaver
from langgraph.graph import START, MessagesState, StateGraph
import psycopg
import psycopg2
from psycopg2.extras import RealDictCursor

from shared import RabbitMQClient

logger = logging.getLogger("chat_engine")

class ChatEngine:
    def __init__(self, openai_api_key: str):
        self.rabbit_chat_client = RabbitMQClient(RabbitMQClient.CHAT_QUEUE)
        self.rabbit_streamer_client = RabbitMQClient(RabbitMQClient.STREAMER_QUEUE)
        self.openai_api_key = openai_api_key
        self.model = init_chat_model("gpt-4o-mini", model_provider="openai")
        self.workflow = StateGraph(state_schema=MessagesState)
        self.workflow.add_node("model", self.call_model)
        self.workflow.add_edge(START, "model")
        self.gpt_answers_queue = RabbitMQClient(RabbitMQClient.GPT_ANSWERS_QUEUE, True)
        self.summary_limit = 1024

        self.db_user = os.getenv("POSTGRES_USER")
        self.db_pass = os.getenv("POSTGRES_PASSWORD")
        self.db_host = os.getenv("POSTGRES_HOST", "db")
        self.db_port = os.getenv("POSTGRES_PORT", "5432")
        self.db_name = os.getenv("POSTGRES_DB", "virtual_artist")

        if os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true":
            self.db_host = os.getenv("POSTGRES_HOST", "db")
        else:
            self.db_host = os.getenv("POSTGRES_HOST", "localhost")

        db_url = f"postgresql://{self.db_user}:{self.db_pass}@{self.db_host}:{self.db_port}/{self.db_name}"

        with PostgresSaver.from_conn_string(db_url) as checkpointer:
            checkpointer.setup()
        
        self.conn = psycopg.connect(db_url, autocommit=True)
        memory = PostgresSaver(self.conn)
        self.memory = memory
        self.app = self.workflow.compile(checkpointer=memory)

    def get_prompt(self):
        conn = psycopg2.connect(
            dbname=self.db_name, 
            user=self.db_user, 
            password=self.db_pass, 
            host=self.db_host,
            port=self.db_port
        )
        cursor = conn.cursor(cursor_factory=RealDictCursor)

        try:
            cursor.execute("SELECT content FROM auxilliary WHERE type = 'PROMPT' LIMIT 1;")
            result = cursor.fetchone()

            if result:
                system_prompt = result["content"]
            else:
                system_prompt = "Привет! Чем могу помочь?"

        except Exception as e:
            print(f"Error fetching prompt: {e}")
            system_prompt = "Привет! Чем могу помочь?"

        finally:
            cursor.close()
            conn.close()

        return system_prompt

    def process_chat_message(self, message_body):
        logger.info(f"No implementation yet")

    def process_streamer_message(self, message_body):
        if isinstance(message_body, bytes):
            message_body = message_body.decode("utf-8")
        
        logger.info(f"Processing chat message: {message_body}")
        response = self.app.invoke(
            {
                "messages": [HumanMessage(message_body)]
            },
            config={"configurable": {"thread_id": "1"}})
        
        try:
            gpt_answer = response["messages"][-1].content
        except Exception as e:
            logger.error(f"gpt didn`t return reponse: {e}")
            gpt_answer = ""
        
        self.gpt_answers_queue.send_message(message=gpt_answer, send_to_storage=True)
        logger.info(f'ChatGPT response: {gpt_answer}')


    def consume_chat_messages(self):
        self.rabbit_chat_client.consume_messages(self.process_chat_message)

    def consume_streamer_messages(self):
        self.rabbit_streamer_client.consume_messages(self.process_streamer_message)

    def call_model(self, state: MessagesState):
        system_prompt = (
            self.get_prompt()
        )
        system_message = SystemMessage(content=system_prompt)
        message_history = state["messages"][:-10]
        if len(message_history) >= 20:
            last_human_messages = state["messages"][-10:]
            summary_prompt = (
                f"Сконденсируй приведенные выше сообщения чата в одно итоговое сообщение. Включи как можно больше конкретных деталей. Уложись в {self.summary_limit} символов"
            )
            summary_message = self.model.invoke(
                message_history + [HumanMessage(content=summary_prompt)]
            )

            delete_messages = [RemoveMessage(id=m.id) for m in state["messages"]]
            response = self.model.invoke([system_message, summary_message] + last_human_messages)
            message_updates = [summary_message] + last_human_messages + [response] + delete_messages
        else:
            message_updates = self.model.invoke([system_message] + state["messages"])

        return {"messages": message_updates}

    def start(self):
        chat_thread = threading.Thread(target=self.consume_chat_messages)
        streamer_thread = threading.Thread(target=self.consume_streamer_messages)

        chat_thread.start()
        streamer_thread.start()

        chat_thread.join()
        streamer_thread.join()

    def close(self):
        if self.conn:
            self.conn.close()
            print("PostgreSQL connection closed")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close()