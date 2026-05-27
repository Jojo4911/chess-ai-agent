from langchain.tools import tool
from app.services.stockfish_service import evaluate_position

@tool
def get_position_evaluation(fen: str) -> str:
    """
    Interroge le moteur d'échecs Stockfish et retourne l'évaluation d'une position.

    À utiliser :
    * Quand on veut évaluer objectivement une position.
    * Dans une position rare, en milieu ou fin de partie.
    * Quand l'utilisateur demande si un coup est bon.

    À NE PAS utiliser :
    * Quand l'utilisateur veut connaître les coups les plus joués par les maîtres.

    Champs vides : L'outil peut retourner des champs vides, par exemple le paramètre 'Mate' peut être vide pour un début de partie.

    Args:
        fen: Donne la position des pièces sur l'échiquier (Forsyth-Edwards Notation)
    
    Returns:
        evaluation: Note la position actuelle en centipawns (cp) ou en nombre de coups avant le mat (mate) → toujours du point de vue des Blancs.
        best_move: Renvoie le prochain meilleur coup.
        top_moves: Renvoie les N (défaut à 5) meilleurs coups avec leur score individuel.
        active_color: Renvoie a qui est le tour de jouer ("w" pour les blancs, "b" pour les noirs)
    """
    result = evaluate_position(fen)
    return result.model_dump_json()