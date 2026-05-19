import asyncio
from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from app.tools.lichess_tool import get_opening_moves
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

# Création de l'agent ReAct avec UN seul tool
agent = create_agent(
    model=model,
    tools=[get_opening_moves],
    system_prompt="Tu es un coach d'échecs pour jeunes joueurs. Tu parles français. Quand on te donne une position, utilise tes outils pour trouver les coups théoriques."
)

# Test sur 3 positions
def test_agent():
    # Test 1 : Position de départ (riche)
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Quels sont les meilleurs premiers coups aux échecs ? La position est : rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"}]
    })
    print("=== TEST 1 : Position de départ ===")
    print(response["messages"][-1].content)

    # Test 2 : Après 1.e4 (moyenne)
    response = agent.invoke({
        "messages": [{"role": "user", "content": "J'ai joué 1.e4, que peut répondre mon adversaire ? FEN : rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"}]
    })
    print("\n=== TEST 2 : Après 1.e4 ===")
    print(response["messages"][-1].content)

    # Test 3 : Bongcloud (vide)
    response = agent.invoke({
        "messages": [{"role": "user", "content": "Que penses-tu de cette position ? FEN : rnbqkbnr/pppp1ppp/8/4p3/4P3/8/PPPPKPPP/RNBQ1BNR b kq - 1 2"}]
    })
    print("\n=== TEST 3 : Position sans théorie ===")
    print(response["messages"][-1].content)

test_agent()