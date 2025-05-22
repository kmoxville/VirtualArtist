from sqlalchemy.ext.asyncio import AsyncSession
from shared.rabbitmq_client import RabbitMQClient
from db.database import SessionLocal
from db.models import Auxilliary, AuxilliaryDataType

class AudioService:
    @staticmethod
    def send_audio(audio_data):
        rabbitmq_client = RabbitMQClient(RabbitMQClient.AUDIO_QUEUE)
        rabbitmq_client.send_message(audio_data)
