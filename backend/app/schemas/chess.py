# --- Modèles de données Stockfish ---
from pydantic import BaseModel
from typing import Literal

class FenPosition(BaseModel):
    """Décomposition de la notation FEN d'une position."""
    piece_placement: str
    active_color: Literal["w", "b"]
    castling: str
    en_passant: str
    halfmove_clock: int
    fullmove_number: int