from langchain.tools import tool
from langchain_core.tools import ToolException
from app.services.youtube_service import search_videos

@tool
def find_videos(opening: str) -> str:
    """
    Recherche des vidéos YouTube pédagogiques sur une ouverture d'échecs.

    À utiliser : 
    * Quand l'utilisateur veut des ressources vidéo pour apprendre une ouverture.

    À NE PAS utiliser :
    * Pour les coups théoriques (get_opening_moves) ni l'évaluation d'une position (get_position_evaluation).
    """
    try:
        videos = search_videos(opening)
    except (ToolException, EnvironmentError) as e:
        return str(e)
    
    if not videos:
        return "Aucune vidéo trouvée pour cette ouverture."
    
    return "\n\n".join(f"{v['titre']} ({v['chaine']})\n{v['url']}" for v in videos)