"""Smoke test gestion d'erreurs (J1, tâche 1). Lancer depuis backend/."""
from langchain_core.tools import ToolException
from app.services.lichess_service import get_theoretical_moves
from app.services.stockfish_service import evaluate_position
from app.tools.lichess_tool import get_opening_moves

VALID_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
BIDON_FEN = "jenesuispasunfen"

def service(label, fn, fen):
    """Un service DOIT renvoyer un objet sur succès, lever ToolException sur erreur."""
    print(f"\n=== [service] {label} ===")
    try:
        out = fn(fen)
        print("OK, renvoyé:", str(out)[:200])
    except ToolException as e:
        print("ToolException (attendu sur erreur):", e)
    except Exception as e:
        print("!! Exception non maîtrisée:", type(e).__name__, e)

def tool(label, fn, fen):
    """Un tool ne DOIT jamais lever : il renvoie le message en chaîne."""
    print(f"\n=== [tool] {label} ===")
    try:
        print("RENVOYÉ:", fn.invoke({"fen": fen})[:200])
    except Exception as e:
        print("!! Le tool a levé (anormal):", type(e).__name__, e)

def tool_validation(label, fn, fen):
    """args_schema doit bloquer et renvoyer un message, pas lever."""
    print(f"\n=== [validation] {label} ===")
    try:
        print("RENVOYÉ:", fn.invoke({"fen": fen})[:200])
    except Exception as e:
        print("!! Levé (handle_validation_error manquant ?):", type(e).__name__, e)

if __name__ == "__main__":
    service("Lichess FEN valide", get_theoretical_moves, VALID_FEN)
    service("Lichess FEN bidon", get_theoretical_moves, BIDON_FEN)
    service("Stockfish FEN valide", evaluate_position, VALID_FEN)
    service("Stockfish FEN bidon", evaluate_position, BIDON_FEN)
    tool("Tool Lichess FEN bidon (doit renvoyer une chaîne)", get_opening_moves, BIDON_FEN)
    tool_validation("FEN bidon", get_opening_moves, "jenesuispasunfen")
    tool_validation("FEN illégal (pas de roi)", get_opening_moves, "8/8/8/8/8/8/8/8 w - - 0 1")