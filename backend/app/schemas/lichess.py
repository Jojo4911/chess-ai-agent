# --- Modèles de données ---
from pydantic import BaseModel, NonNegativeInt, NonNegativeFloat

class CandidateOpening(BaseModel):
    """Une ouverture candidate avec ses statistiques."""
    eco: str
    name: str

class CandidateMove(BaseModel):
    """Un coup candidat avec ses statistiques."""
    san: str
    white_ratio: NonNegativeFloat
    draws_ratio: NonNegativeFloat
    black_ratio: NonNegativeFloat
    total_games: NonNegativeInt
    opening: CandidateOpening | None

class PositionStats(BaseModel):
    """Une position avec ses statistiques."""
    white_ratio: NonNegativeFloat
    draws_ratio: NonNegativeFloat
    black_ratio: NonNegativeFloat
    total_games: NonNegativeInt

class OpeningExplorerResponse(BaseModel):
    """Réponse structurée de l'Opening Explorer."""
    opening: CandidateOpening | None
    moves: list[CandidateMove]
    position_stats: PositionStats