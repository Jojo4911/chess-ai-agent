from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from app.tools.lichess_tool import get_opening_moves
from app.tools.stockfish_tool import get_position_evaluation
from dotenv import load_dotenv
import os

load_dotenv()
llm_model = os.getenv("LLM_MODEL")

# Initialisation du modèle
model = init_chat_model(
    llm_model,
    #"claude-sonnet-4-5-20250929",
    temperature=0
)

# Création de l'agent ReAct avec DEUX tools
agent = create_agent(
    model=model,
    tools=[get_opening_moves, get_position_evaluation],
    system_prompt="Tu es un coach d'échecs pour jeunes joueurs. Tu parles français. Quand on te donne une position, utilise tes outils pour trouver les coups théoriques."
)

# Test sur 3 positions
def test_agent():
    # Test 1 : Question sur la PARTIE ITALIENNE (où Lichess devrait être appelé)
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Je viens de démarer la partie, quelle ouverture est jouée ? La position est : r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"}]
    })
    print("=== TEST 1 : Ouverture Italienne → Lichess ===")
    print(response["messages"][-1].content)

    for msg in response["messages"]:
        print(f"{msg.type}: {msg.content[:100]}")

    # Test 2 : Question sur une position de milieu de partie originale (où Stockfish devrait être appelé)
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Que penses tu de ma position ? FEN : r1bq1rk1/pp1n1ppp/2p1pn2/3p4/2PP4/2N1PN2/PP1QBPPP/R3K2R w KQ - 0 10"}]
    })
    print("\n=== TEST 2 : Milieu de partie originale → Stockfish ===")
    print(response["messages"][-1].content)

    for msg in response["messages"]:
        print(f"{msg.type}: {msg.content[:100]}")

    # Test 3 : Question sur la SICILIENNE (où les deux outils pourraient être utiles)
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Quel serait le meilleur coup dans cette situation ? FEN : rnbqkbnr/pp2pppp/3p4/2p5/3BP3/5N2/PPP2PPP/RNBQK2R b KQkq - 0 3"}]
    })
    print("\n=== TEST 3 : Ouverture Sicilienne avec demande de meilleur coup → Lichess + Stockfish ===")
    print(response["messages"][-1].content)

    for msg in response["messages"]:
        print(f"{msg.type}: {msg.content[:100]}")

test_agent()