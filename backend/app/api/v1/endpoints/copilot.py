from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.user import User
from app.schemas.copilot import CopilotQueryRequest, CopilotQueryResponse
from app.services.copilot_service import copilot_service

router = APIRouter()

@router.post("/query", response_model=CopilotQueryResponse)
def ask_copilot(query_in: CopilotQueryRequest, db: Session = Depends(get_db)):
    user = db.query(User).first()
    if not user:
        raise HTTPException(status_code=400, detail="User not initialized")

    return copilot_service.answer_query(
        db=db,
        user_id=user.id,
        query=query_in.query,
        expense_id=query_in.expense_id,
        conversation_id=query_in.conversation_id
    )
