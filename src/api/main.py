from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional

from rag.query import answer_question

app = FastAPI(title="Intelligent Data Copilot")


# ---- Request schema ----
class Question(BaseModel):
    question: str
    dialect: Optional[str] = None   # <-- FIXES 422 error


# ---- Health check ----
@app.get("/health")
def health():
    return {"status": "ok"}


# ---- Ask endpoint ----
@app.post("/ask")
def ask(q: Question):
    result = answer_question(q.question)

    return {
        "question": q.question,
        "answer": result["answer"],
        "sources": result["sources"],
    }
