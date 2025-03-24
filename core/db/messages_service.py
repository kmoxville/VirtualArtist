from sqlalchemy.ext.asyncio import AsyncSession
from db.database import SessionLocal
from db.models import StreamerMessage

class MessagesService:
    @staticmethod
    def save_message(content: str, source: str):
        session = SessionLocal()
        new_message = StreamerMessage(content=content, source=source)
        session.add(new_message)
        session.commit()

    @staticmethod
    def get_messages(limit: int = 10):
        pass