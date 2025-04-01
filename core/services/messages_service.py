from db.database import SessionLocal
from db.models import StreamerMessage

class MessagesService:
    @staticmethod
    def save_message(content: str, source: str):
        with SessionLocal() as session:
            new_message = StreamerMessage(content=content, source=source)
            session.add(new_message)
            session.commit()

    @staticmethod
    def get_messages(limit: int = 10, source: str = None):
        with SessionLocal() as session:
            query = session.query(StreamerMessage).order_by(StreamerMessage.timestamp.desc()).limit(limit)

            if source:
                query = query.filter(StreamerMessage.source == source)

            return query.all()