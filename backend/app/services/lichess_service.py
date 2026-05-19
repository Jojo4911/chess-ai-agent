# --- Imports ---
from app.schemas.lichess import OpeningExplorerResponse, CandidateMove, PositionStats, CandidateOpening
import httpx
import os
from dotenv import load_dotenv
from langchain.tools import tool
import asyncio # Seulement pour les tests

load_dotenv()

def victory_stats(white: int, draws: int, black: int):
    """
    Calcule les statistiques simples sur les victoires
    """
    total_games = white + draws + black

    if total_games == 0: # Pour éviter la division par zéro
        white_ratio = 0
        draws_ratio = 0
        black_ratio = 0
    else:
        white_ratio = round((white / total_games) * 100, 1)
        draws_ratio = round((draws / total_games) * 100, 1)
        black_ratio = round((black / total_games) * 100, 1)
    
    return total_games, white_ratio, draws_ratio, black_ratio

# --- Tools ---
@tool
async def get_theoretical_moves(fen: str) -> OpeningExplorerResponse:
    """
    Interroge la base de données de parties de maîtres des échecs de l'Opening Explorer Lichess et retourne les coups théoriques principaux avec leurs statistiques.

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
    lichess_url = os.getenv("LICHESS_URL")
    api_key = os.getenv("LICHESS_API_KEY")
    if not api_key:
        raise EnvironmentError("LICHESS_API_KEY non définie dans .env")
    
    async with httpx.AsyncClient(timeout=httpx.Timeout(10.0)) as client:
        try:
            response = await client.get(f"https://{lichess_url}/masters",
                headers={
                    "Authorization": "Bearer " + api_key
                },
                params={
                    "fen": fen
                }
            )
            response.raise_for_status()
        except httpx.TimeoutException as e:
            raise TimeoutError(f"Erreur de délais lors de l'appel API : {e}")
        except httpx.HTTPStatusError as e:
            raise ConnectionAbortedError(f"Erreur de status http lors de l'appel API : {e}")

    # - Décomposition de la réponse -    
    data = response.json()

    # - Ouverture -
    if data['opening'] is not None:
        pos_opening = CandidateOpening(eco=data['opening']['eco'], name=data['opening']['name'])
    else:
        pos_opening = None

    # - Statistiques de la position -
    pos_total_games, pos_white_ratio, pos_draws_ratio, pos_black_ratio = victory_stats(data['white'], data['draws'], data['black'])
    pos_stats = PositionStats(
                    white_ratio=pos_white_ratio,
                    draws_ratio=pos_draws_ratio,
                    black_ratio=pos_black_ratio,
                    total_games=pos_total_games,
                )

    # - Meilleurs coups -
    raw_moves = data['moves']
    moves = []
    for move in raw_moves:
        move_total_games, move_white_ratio, move_draws_ratio, move_black_ratio = victory_stats(move['white'], move['draws'], move['black'])
        moves.append(
            CandidateMove(
                san=move['san'],
                white_ratio=move_white_ratio,
                draws_ratio=move_draws_ratio,
                black_ratio=move_black_ratio,
                total_games=move_total_games,
                opening=move['opening'],
            )
        )
    sorted_moves = sorted(moves, key=lambda move: move.total_games, reverse=True)
    top_moves = sorted_moves[:5]
    return OpeningExplorerResponse(opening=pos_opening, moves=top_moves, position_stats=pos_stats)

#result = asyncio.run(get_theoretical_moves("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")) # Position riche = départ
#result = asyncio.run(get_theoretical_moves("rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1")) # Position moyenne = après 1.e4
#result = asyncio.run(get_theoretical_moves("rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR b kq - 1 2")) # Position vide = Bongcloud
#print(result.model_dump_json(indent=2))