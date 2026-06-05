from langchain.tools import tool
from langchain_core.tools import ToolException
from app.schemas.chess import ValidFen
from app.services.lichess_service import get_theoretical_moves

@tool(args_schema=ValidFen)
def get_opening_moves(fen: str) -> str:
    """
    Interroge la base de données de parties de maîtres des échecs de l'Opening Explorer Lichess et retourne le nom de l'ouverture jouée (si connue), les coups théoriques principaux avec leurs statistiques.

    À utiliser :
    * Quand l'utilisateur est dans la phase d'ouverture d'une partie, les premiers coups.
    * Quand l'utilisateur veut connaître les coups les plus joués par les maîtres, et les statistiques de victoire, par rapport à une position donnée
    
    À NE PAS utiliser :
    * Quand l'utilisateur veut des informations sur une ouverture (histoire, théorie)

    Champs vides : L'outil peut retourner des champs vides si la position n'est pas dans la base de données

    Args:
        fen: Donne la position des pièces sur l'échiquier (Forsyth-Edwards Notation)
    
    Returns:
        opening: Donne l'ouverture de la position actuelle
        moves: Donne les 5 coups les plus joués, les ratios de victoires, le nombre de parties jouées et le nom des ouvertures liées
        position_stats: Donne les ratios de victoires et le nombre de parties jouées de la position actuelle
    """
    try:
        result = get_theoretical_moves(fen)
        return result.model_dump_json()
    except ToolException as e:
        return str(e)
    
get_opening_moves.handle_validation_error = lambda e: str(e)