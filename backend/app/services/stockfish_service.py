# --- Imports ---
from stockfish import Stockfish
from app.schemas.stockfish import PositionEvaluation, TopMove, StockfishResponse
from dotenv import load_dotenv
import os

load_dotenv()
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")
DEPTH = int(os.getenv("STOCKFISH_DEPTH"))

# --- Tools ---
def evaluate_position(fen: str, depth: int = DEPTH) -> StockfishResponse:
    """
    Évalue n'importe quelle position d'une partie grâce au moteur Stockfish :
    * Note la position actuelle en centipawns (cp) ou en nombre de coups avant le mat (mate).
    * Renvoie le prochain meilleur coup.
    * Renvoie les 5 meilleurs coups avec leur score individuel.
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

    return StockfishResponse(evaluation=position_eval, best_move=sf.get_best_move(), top_moves=top_moves)

#result = evaluate_position("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1") # Position de départ après 1.d4
#result = evaluate_position("2r2rk1/1pqn1ppp/p1n1b3/4p3/Q3P3/2N1B3/PP2BPPP/2R1K2R w K - 0 1") # Position milieu de partie
#result = evaluate_position("") # Position avec mat forcé
#print(result.model_dump_json(indent=2))