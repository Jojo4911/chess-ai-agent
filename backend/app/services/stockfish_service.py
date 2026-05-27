# --- Imports ---
from stockfish import Stockfish
from app.schemas.stockfish import PositionEvaluation, TopMove, StockfishResponse
from typing import Literal
from dotenv import load_dotenv
import os

load_dotenv()
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
DEPTH = int(os.getenv("STOCKFISH_DEPTH"))

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
    
    # Instanciation du moteur Stockfish
    sf = Stockfish(path=STOCKFISH_PATH, depth=depth)
    # Chargement de la position FEN
    sf.set_fen_position(fen)
    # Récupération des statistiques
    evaluation = sf.get_evaluation()
    position_eval = PositionEvaluation(**evaluation)
    top_moves = [
        TopMove(move=m['Move'], centipawn=m['Centipawn'], mate=m['Mate'])
        for m in sf.get_top_moves(5)
    ]
    active_color = get_active_color(fen)

    return StockfishResponse(evaluation=position_eval, best_move=sf.get_best_move(), top_moves=top_moves, active_color=active_color)