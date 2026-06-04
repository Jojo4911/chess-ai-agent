from langchain.tools import tool
from langchain_core.tools import ToolException
from app.rag.rag_service import search_knowledge

@tool()
def search_chess_knowledge(query: str) -> str:
    """
    Interroge le RAG de la base de connaissances sur les ouvertures aux échecs et retourne des informations historiques et des explications sur ces ouvertures.
    
    À utiliser :
    * Quand l'utilisateur est dans la phase d'ouverture d'une partie, les premiers coups.
    * Quand l'utilisateur veut en savoir plus sur une ouverture spécifique (histoire, théorie).
    * Quand l'utilisateur se trouve dans une ouverture spécifique pour lui apporter des informations supplémentaires.

    À ne pas utiliser :
    * Quand l'utilisateur veut connaître les coups les plus joués par les maîtres sur une ouverture spécifique.

    Args:
        query: Question en langage naturel concernant une ouverture.
    
    Returns:
        str: Donne des informations sur une ouverture spécifique en langage naturel.
    """
    try:
        result = search_knowledge(query)
        formatted = "\n\n".join(
            f"[{r['nom']} | ECO : {r['eco']}]\n{r['text']}"
            for r in result
        )
        return formatted if formatted else "Aucune information trouvée sur ce sujet."
    except ToolException as e:
        return str(e)