from fastapi import APIRouter, Depends
from services.prompts_service import PromptsService

router = APIRouter(prefix="/prompts", tags=["Prompts"])

@router.get("/")
def get_prompt():
    return {"system_prompt": PromptsService.get_prompt()}

@router.post("/")
def set_prompt(content: str):
    PromptsService.set_prompt(content)
    return {"message": "system_prompt updated"}