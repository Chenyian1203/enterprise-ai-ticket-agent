from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import get_db
from services.agent_service import run_agent

router = APIRouter(prefix="/api/chat", tags=["智能客服"])

class ChatRequest(BaseModel):
    message: str

@router.post("/")
def chat_with_ai(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        reply = run_agent(request.message, db)
        return {"reply": reply}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))