# --- Modèles de données FEN ---
import chess
from pydantic import BaseModel, Field, field_validator

class ValidFen(BaseModel):
    """Schéma d'entrée partagé par tous les tools qui prennent un FEN."""
    fen: str = Field(description="Position FEN de l'échiquier")

    @field_validator("fen")
    @classmethod
    def check_fen_legality(cls, v: str) -> str:
        v = v.strip()
        try:
            board = chess.Board(v)
        except ValueError:
            raise ValueError("FEN mal formé, vérifie la syntaxe (6 champs séparés par des espaces).")
        if not board.is_valid():
            raise ValueError(f"Position illégale : {board.status()!r}")
        return v