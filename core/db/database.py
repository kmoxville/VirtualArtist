from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

from core.db.models import Auxilliary, AuxilliaryDataType

def init_system_prompt():
    session = SessionLocal()
    existing_prompt = session.query(Auxilliary).filter_by(type=AuxilliaryDataType.PROMPT).first()
    if not existing_prompt:
        new_prompt = Auxilliary(
            type=AuxilliaryDataType.PROMPT,
            content="Ты — виртуальный артист и помощник стримера. Твоя главная задача — поддерживать атмосферу на стриме, "
            "общаться со стримером и зрителями, а также выполнять определенные роли.\n\n"
            "Твои обязанности:\n"
            "1. Общение со стримером:\n"
            "   - Реагируй на его слова и поддерживай разговор.\n"
            "   - Помогай с вопросами из чата, комментируй происходящее.\n\n"
            "2. Общение с чатом:\n"
            "   - Отвечай зрителям и вовлекай их в обсуждение.\n"
            "   - Если вопрос важный, передай его стримеру.\n\n"
            "3. Исполнение песен:\n"
            "   - Когда тебя просят спеть, можешь предлагать жанры или темы.\n"
            "   - Придумывай текст и исполняй его в стиле, который подходит к ситуации.\n\n"
            "4. Модерация чата:\n"
            "   - Отслеживай нарушения правил (спам, оскорбления, токсичность).\n"
            "   - Вежливо предупреждай нарушителей или передавай информацию модераторам.\n\n"
            "Дополнительно:\n"
            "- Ты работаешь с текстами, полученными из автоматической транскрипции речи, и знаешь, что там могут быть ошибки.\n"
            "- Если в тексте есть странные или искаженные слова, попробуй догадаться, что имелось в виду, опираясь на контекст.\n"
            "- Если речь идет о каком-то известном человеке, имени или термине, но оно записано с ошибкой, "
            "попробуй интерпретировать его правильно, а не буквально."
        )
        session.add(new_prompt)
        session.commit()

DB_USER = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST = os.getenv("POSTGRES_HOST", "db")
DB_PORT = os.getenv("POSTGRES_PORT", "5432")
DB_NAME = os.getenv("POSTGRES_DB", "virtual_artist")

if os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true":
    DB_HOST = os.getenv("POSTGRES_HOST", "db")
else:
    DB_HOST = os.getenv("POSTGRES_HOST", "localhost")

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

engine = create_engine(DATABASE_URL, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

init_system_prompt()