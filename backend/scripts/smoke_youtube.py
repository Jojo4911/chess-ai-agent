# scripts/smoke_youtube.py
from app.services import youtube_service
from app.services.youtube_service import search_videos
import app.tools.youtube_tool as yt_tool
from app.tools.youtube_tool import find_videos


def test_service_reel():
    print("== Service, appel réel ==")
    for opening in ["Sicilienne", "Défense française"]:
        videos = search_videos(f"{opening} ouverture échecs tutoriel")
        print(f"\n{opening} : {len(videos)} vidéo(s)")
        for v in videos:
            print(f"  - {v['titre']} ({v['chaine']})\n    {v['url']}")
        assert videos, f"Aucune vidéo pour {opening}, suspect"


def test_tool_format():
    print("\n== Tool, formatage ==")
    sortie = find_videos.invoke({"opening": "Sicilienne"})
    print(sortie)
    assert "youtube.com/watch" in sortie


def test_zero_resultat():
    print("\n== Cas zéro résultat ==")
    original = yt_tool.search_videos
    yt_tool.search_videos = lambda query, max_results=3: []
    try:
        sortie = find_videos.invoke({"opening": "ouverturequinexistepas"})
        print(sortie)
        assert sortie == "Aucune vidéo trouvée pour cette ouverture."
    finally:
        yt_tool.search_videos = original


def test_cle_manquante():
    print("\n== Cas clé manquante ==")
    original = youtube_service.YOUTUBE_API_KEY
    youtube_service.YOUTUBE_API_KEY = None
    try:
        sortie = find_videos.invoke({"opening": "Sicilienne"})
        print(sortie)
        assert "YOUTUBE_API_KEY" in sortie
    finally:
        youtube_service.YOUTUBE_API_KEY = original


if __name__ == "__main__":
    test_service_reel()
    test_tool_format()
    test_zero_resultat()
    test_cle_manquante()
    print("\nTous les checks passent.")