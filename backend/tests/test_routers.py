# --- Imports ---
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from langchain_core.tools import ToolException
from api.main import app

@pytest.fixture
def client():
    return TestClient(app)


# --- POST /api/v1/agent/ask ---

def test_ask_success(client):
    with (
        patch("app.api.v1.routers.agent_router.call_agent", return_value=("Réponse de l'agent", [])),
        patch("app.api.v1.routers.agent_router.log_interaction")
    ):
        response = client.post("/api/v1/agent/ask", json={
            "question": "Qu'est-ce que l'ouverture sicilienne ?",
            "role": "user"
        })
        assert response.status_code == 200
        assert response.json() == {"answer": "Réponse de l'agent"}

def test_ask_recursion_error(client):
    error_dict = {"error": "recursion_limit_reached", "message": "L'agent a atteint le nombre maximum d'itérations."}
    with (
        patch("app.api.v1.routers.agent_router.call_agent", return_value=(error_dict, [])),
        patch("app.api.v1.routers.agent_router.log_interaction")
    ):
        response = client.post("/api/v1/agent/ask", json={
            "question": "Analyse cette position",
            "role": "user"
        })
        assert response.status_code == 500


def test_ask_invalid_fen(client):
    response = client.post("/api/v1/agent/ask", json={
        "fen": "position_invalide",
        "question": "Analyse",
        "role": "user"
    })
    assert response.status_code == 422


# --- GET /api/v1/moves/{fen} ---

VALID_FEN = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

def test_moves_success(client):
    with patch("app.api.v1.routers.chess_router.get_theoretical_moves", return_value=["e5", "c5"]):
        response = client.get(f"/api/v1/moves/{VALID_FEN}")
        assert response.status_code == 200
        assert response.json() == {"moves": ["e5", "c5"]}


def test_moves_tool_exception(client):
    with patch("app.api.v1.routers.chess_router.get_theoretical_moves", side_effect=ToolException("Lichess indisponible")):
        response = client.get(f"/api/v1/moves/{VALID_FEN}")
        assert response.status_code == 503


# --- GET /api/v1/evaluate/{fen} ---

def test_evaluate_success(client):
    with patch("app.api.v1.routers.chess_router.evaluate_position", return_value={"score": 30}):
        response = client.get(f"/api/v1/evaluate/{VALID_FEN}")
        assert response.status_code == 200
        assert response.json() == {"evaluation": {"score": 30}}


def test_evaluate_tool_exception(client):
    with patch("app.api.v1.routers.chess_router.evaluate_position", side_effect=ToolException("Stockfish indisponible")):
        response = client.get(f"/api/v1/evaluate/{VALID_FEN}")
        assert response.status_code == 503