import typing as t
from fastapi import APIRouter
from pydantic import BaseModel

from src.ensemble import Ensemble

router = APIRouter()

class EvaluationCompletion(BaseModel):
    question: str
    context: str 

@router.post("/chat/llm", response_model=t.Dict)
async def evaluate() -> t.Dict:

    # model inference endpoint either model or ensemble or agent queue
    
    return {"message": "this will be the model evaluation"}