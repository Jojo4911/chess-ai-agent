from langchain.agents import create_agent
from langchain.chat_models import init_chat_model
from langgraph.errors import GraphRecursionError
from app.tools.lichess_tool import get_opening_moves
from app.tools.stockfish_tool import get_position_evaluation
from dotenv import load_dotenv
import os
from pathlib import Path

load_dotenv()
llm_model = os.getenv("LLM_MODEL")
prompt_path = Path(__file__).parents[3] / "prompts" / "agent_system.md"

# Lecture du system prompt
def load_system_prompt(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
# Initialisation du modèle
model = init_chat_model(
    llm_model,
    temperature=0
)

# Création de l'agent ReAct avec DEUX tools
agent = create_agent(
    model=model,
    tools=[get_opening_moves, get_position_evaluation],
    system_prompt=load_system_prompt(prompt_path)
).with_config({"recursion_limit":10})

# Fonction d’appel d’agent
def call_agent(question: str, role: str = "user"):
    try:
        response = agent.invoke({
            "messages": [{"role": role, "content": question}]
        })
        return response["messages"][-1].content
    except GraphRecursionError:
        return {"error": "recursion_limit_reached", "message": "L'agent a atteint le nombre maximum d'itérations."}