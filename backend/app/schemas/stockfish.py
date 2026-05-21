# --- Modèles de données Stockfish ---
from pydantic import BaseModel
from typing import Literal

class PositionEvaluation(BaseModel):
    """Une évaluation d'un coup."""
    type: Literal["cp", "mate"]
    value: int

class TopMove(BaseModel):
    """Un des meilleurs coups à jouer."""
    move: str
    centipawn: int | None
    mate: int | None

class StockfishResponse(BaseModel):
    """Réponse structurée de Stockfish."""
    evaluation: PositionEvaluation
    best_move: str
    top_moves: list[TopMove]