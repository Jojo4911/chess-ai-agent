# --- Imports ---
import os
import time
import httpx
import html
from langchain_core.tools import ToolException

YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY")
YOUTUBE_SEARCH_URL = "https://www.googleapis.com/youtube/v3/search"

# --- Tools ---
def search_videos(query: str, max_results: int = 3) -> list[dict]:
    """
    Fais appel à l'API de Youtube pour trouver des vidéos en rapport avec l'ouverture traitée.
    """

    if not YOUTUBE_API_KEY:
        raise EnvironmentError("YOUTUBE_API_KEY non définie dans .env")
    
    params = {
        "key": YOUTUBE_API_KEY,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results,
        "relevanceLanguage": "fr",
    }
    
    with httpx.Client(timeout=httpx.Timeout(10.0)) as client:
        for attempt in range(3):
            try:
                response = client.get(YOUTUBE_SEARCH_URL, params=params)
                response.raise_for_status()
                break
            except httpx.HTTPStatusError as e:
                if e.response.status_code in (429, 500, 503):
                    time.sleep(attempt + 1)
                    continue
                raise ToolException(f"YouTube a renvoyé une erreur {e.response.status_code}.") from e
            except httpx.TimeoutException:
                time.sleep(attempt + 1)
                continue
            except httpx.RequestError as e:
                raise ToolException("Impossible de joindre YouTube (réseau).") from e
        else:
            raise ToolException("YouTube indisponible après 3 tentatives.")

    # - Décomposition de la réponse -    
    items = response.json().get("items", [])
    return [
        {
            "titre": html.unescape(item["snippet"]["title"]),
            "chaine": item["snippet"]["channelTitle"],
            "url": f"https://www.youtube.com/watch?v={item['id']['videoId']}",
        }
        for item in items
    ]