from fastapi import APIRouter, HTTPException
from app.agent.agent import call_agent
from pydantic import BaseModel, field_validator, ValidationError
from app.schemas.chess import ValidFen
from app.services.mongo_service import log_interaction
from datetime import datetime, timezone
import time

router = APIRouter(prefix="/api/v1/agent", tags=["agent"])

class AskRequest(BaseModel):
    """Schéma d'entrée"""
    fen: str | None = None
    question: str
    role: str = "user"

    @field_validator("fen")
    @classmethod
    def validate_fen(cls, v):
        if v is None:
            return v
        try:
            ValidFen(fen=v)  # délègue : déclenche check_fen_legality
        except ValidationError as e:
            raise ValueError(str(e))
        return v

@router.post("/ask")
async def ask(request: AskRequest):
    start = time.time()
    if request.fen:
        full_question = f"Position FEN : {request.fen}\n{request.question}"
    else:
        full_question = request.question

    result, tool_calls = call_agent(full_question, request.role)
    duration_ms = int((time.time() - start) * 1000)

    try:
        log_interaction({
            "timestamp": datetime.now(timezone.utc),
            "fen": request.fen,
            "question": request.question,
            "role": request.role,
            "answer": result,
            "tool_calls": tool_calls,
            "duration_ms": duration_ms,
        })
    except Exception:
        pass

    if isinstance(result, dict):
        raise HTTPException(status_code=500, detail=result)
    return {"answer": result}