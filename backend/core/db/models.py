import enum
from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Text, func, Enum

Base = declarative_base()

class StreamerMessage(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=func.now())
    content = Column(Text, nullable=False)
    source = Column(String, default="streamer")

class AuxilliaryDataType(str, enum.Enum):
    PROMPT = "prompt"

class Auxilliary(Base):
    __tablename__ = "auxilliary"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)
    type = Column(Enum(AuxilliaryDataType, name="auxilliary_data_type"), nullable=False, unique=True)