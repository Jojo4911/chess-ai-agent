# --- Imports ---
from stockfish import Stockfish, StockfishException
from langchain_core.tools import ToolException
from app.schemas.stockfish import PositionEvaluation, TopMove, StockfishResponse
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
DEPTH = int(os.getenv("STOCKFISH_DEPTH", "15"))

def get_active_color(fen: str) -> Literal["w", "b"]:
    """Renvoie la couleur active (blanc "w" ou noir "b") à partir d'une position FEN."""
    return fen.split(" ")[1]

# --- Tools ---
def evaluate_position(fen: str, depth: int = DEPTH) -> StockfishResponse:
    """
    Évalue n'importe quelle position d'une partie grâce au moteur Stockfish :
    * Note la position actuelle en centipawns (cp) ou en nombre de coups avant le mat (mate).
    * Renvoie le prochain meilleur coup.
    * Renvoie les 5 meilleurs coups avec leur score individuel.
    * Renvoie à qui est le tour de jouer.
    """
    if not STOCKFISH_PATH:
        raise EnvironmentError("STOCKFISH_PATH non définie dans .env")
    
    try:
        # Instanciation du moteur Stockfish
        sf = Stockfish(path=STOCKFISH_PATH, depth=depth)
        # Chargement de la position FEN
        sf.set_fen_position(fen)
        # Récupération des statistiques
        evaluation = sf.get_evaluation()
        best_move = sf.get_best_move()
        raw_top_moves = sf.get_top_moves(5)
    except (StockfishException, FileNotFoundError, ValueError) as e:
        raise ToolException("Le moteur Stockfish n'a pas pu évaluer la position.") from e

    if best_move is None:  # mat ou pat : aucun coup légal
        raise ToolException("Position terminée (mat ou pat), aucun coup à évaluer.")

    position_eval = PositionEvaluation(**evaluation)
    top_moves = [
        TopMove(move=m['Move'], centipawn=m['Centipawn'], mate=m['Mate'])
        for m in raw_top_moves
    ]
    active_color = get_active_color(fen)

    return StockfishResponse(
        evaluation=position_eval,
        best_move=best_move,
        top_moves=top_moves,
        active_color=active_color,
    )