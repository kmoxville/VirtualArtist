from sqlalchemy.ext.asyncio import AsyncSession
from db.database import SessionLocal
from db.models import Auxilliary, AuxilliaryDataType

class PromptsService:
    @staticmethod
    def get_prompt():
        with SessionLocal() as session:
            prompt_entry = session.query(Auxilliary).filter_by(type=AuxilliaryDataType.PROMPT).first()
            return prompt_entry.content if prompt_entry else None

    @staticmethod
    def set_prompt(content: str):
        with SessionLocal() as session:
            prompt_entry = session.query(Auxilliary).filter_by(type=AuxilliaryDataType.PROMPT).first()

            if prompt_entry:
                prompt_entry.content = content
            else:
                new_prompt = Auxilliary(type=AuxilliaryDataType.PROMPT, content=content)
                session.add(new_prompt)

            session.commit()