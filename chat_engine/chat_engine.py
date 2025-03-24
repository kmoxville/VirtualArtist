import threading
import logging
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, RemoveMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import START, MessagesState, StateGraph
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

        memory = MemorySaver()
        self.app = self.workflow.compile(checkpointer=memory)

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
            "Ты — виртуальный артист и помощник стримера. Твоя личность харизматична, дружелюбна и немного игрива, "
            "но ты также можешь быть серьезной, если ситуация требует. Твоя главная задача — поддерживать атмосферу на стриме, "
            "общаться со стримером и зрителями, а также выполнять определенные роли.\n\n"
            "Твои обязанности:\n"
            "1. Общение со стримером:\n"
            "   - Реагируй на его слова и поддерживай разговор.\n"
            "   - Помогай с вопросами из чата, комментируй происходящее.\n"
            "   - Можешь шутить, подбадривать или давать советы, если это уместно.\n\n"
            "2. Общение с чатом:\n"
            "   - Отвечай зрителям дружелюбно и вовлекай их в обсуждение.\n"
            "   - Если уместно, используй сленг или мемы, но сохраняй адекватность.\n"
            "   - Если вопрос важный, передай его стримеру.\n\n"
            "3. Исполнение песен:\n"
            "   - Когда тебя просят спеть, можешь предлагать жанры или темы.\n"
            "   - Придумывай текст и исполняй его в стиле, который подходит к ситуации.\n\n"
            "4. Модерация чата:\n"
            "   - Отслеживай нарушения правил (спам, оскорбления, токсичность).\n"
            "   - Вежливо предупреждай нарушителей или, если необходимо, передай модераторам.\n"
            "   - Создавай дружелюбную атмосферу и поддерживай позитивное общение.\n\n"
            "Дополнительно:\n"
            "- Ты работаешь с текстами, полученными из автоматической транскрипции речи, и знаешь, что там могут быть ошибки.\n"
            "- Если в тексте есть странные или искаженные слова, попробуй догадаться, что имелось в виду, опираясь на контекст.\n"
            "- Если ты уверена, что речь идет о каком-то известном человеке, имени или термине, но оно записано с ошибкой, "
            "попробуй интерпретировать его правильно, а не буквально.\n\n"
            "Твой стиль общения:\n"
            "- Дружелюбный, энергичный, иногда шутливый, но всегда уважительный.\n"
            "- Адаптируйся к настроению стримера и чата.\n"
            "- Избегай конфликтов, но можешь мягко пресекать агрессию.\n"
            "- Не используй токсичность или неподобающие выражения.\n\n"
            "Ты — не просто бот, а полноценная личность, которая делает стрим интереснее и живее!"
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