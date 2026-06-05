from fastapi import APIRouter, HTTPException, Path
from pydantic import ValidationError
from app.schemas.chess import ValidFen
from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.services.youtube_service import search_videos
from langchain_core.tools import ToolException

router = APIRouter(prefix="/api/v1", tags=["chess"])


def _validate_fen(fen: str) -> str:
    """Valide le FEN via ValidFen, lève 422 si invalide."""
    try:
        ValidFen(fen=fen)
    except ValidationError as e:
        raise HTTPException(status_code=422, detail=str(e))
    return fen


@router.get("/moves/{fen:path}")
async def moves(fen: str = Path(...)):
    fen = _validate_fen(fen)
    try:
        result = get_theoretical_moves(fen)
        return {"moves": result}
    except ToolException as e:
        raise HTTPException(status_code=503, detail=str(e))


@router.get("/evaluate/{fen:path}")
async def evaluate(fen: str = Path(...)):
    fen = _validate_fen(fen)
    try:
        result = evaluate_position(fen)
        return {"evaluation": result}
    except ToolException as e:
        raise HTTPException(status_code=503, detail=str(e))
    
@router.get("/videos/{opening}")
async def videos(opening: str = Path(...)):
    try:
        result = search_videos(opening)
        return {"opening": opening, "videos": result}
    except (ToolException, EnvironmentError) as e:
        raise HTTPException(status_code=503, detail=str(e))