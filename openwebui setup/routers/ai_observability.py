from fastapi import APIRouter
from pydantic import BaseModel

from open_webui.observability_ai.summary import generate_summary
from open_webui.observability_ai.ask import answer_question

class QuestionRequest(BaseModel):
    question: str

router = APIRouter()


@router.get("/summary")
def summary():
    return generate_summary()

@router.get("/health")
def health():
    return {"status": "ok"}

@router.post("/ask")
def ask(req: QuestionRequest):
    intent, answer = answer_question(req.question)
    return {
        "question": req.question,
        "intent": intent,
        "answer": answer
    }