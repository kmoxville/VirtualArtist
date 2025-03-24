from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, func

Base = declarative_base()

class StreamerMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=func.now())
    content = Column(Text, nullable=False)
    source = Column(String, default="streamer")