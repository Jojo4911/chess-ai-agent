# --- Imports ---
from app.schemas.stockfish import StockfishResponse
from app.services.stockfish_service import evaluate_position

# --- Tests ---
def test_regular_position():
    result = evaluate_position("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq d3 0 1")
    assert result.evaluation.type == "cp"
    assert result.best_move != ""
    assert result.top_moves != []
    assert isinstance(result, StockfishResponse)

def test_mate_position():
    result = evaluate_position("k7/8/1K6/8/8/8/8/7R w - - 0 1")
    assert result.evaluation.type == "mate"
    assert result.evaluation.value == 1
    assert result.best_move == "h1h8"
    assert result.top_moves != []