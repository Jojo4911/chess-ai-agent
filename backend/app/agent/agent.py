from langchain.chat_models import init_chat_model
from langchain_core.messages import SystemMessage, ToolMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.errors import GraphRecursionError
from app.tools.lichess_tool import get_opening_moves
from app.tools.stockfish_tool import get_position_evaluation
from app.tools.rag_tool import search_chess_knowledge
from app.tools.youtube_tool import find_videos
from dotenv import load_dotenv
from pathlib import Path
from typing import Literal
import os

load_dotenv()

llm_model = os.getenv("LLM_MODEL")
_docker_path = Path(__file__).parents[2] / "prompts" / "agent_system.md"
_local_path = Path(__file__).parents[3] / "prompts" / "agent_system.md"
prompt_path = _docker_path if _docker_path.exists() else _local_path

# Lecture du system prompt
def load_system_prompt(path: Path) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()
    
system_prompt_text = load_system_prompt(prompt_path)

tools = [get_opening_moves, get_position_evaluation, search_chess_knowledge, find_videos]
tools_by_name = {tool.name: tool for tool in tools}
    
# Initialisation du modèle
model = init_chat_model(
    llm_model,
    temperature=0
)
model_with_tools = model.bind_tools(tools)

def llm_call(state: MessagesState):
    return {
        "messages": [
            model_with_tools.invoke(
                [SystemMessage(content=system_prompt_text)] + state["messages"]
            )
        ]
    }

def tool_node(state: MessagesState):
    result = []
    for tool_call in state["messages"][-1].tool_calls:
        tool = tools_by_name[tool_call["name"]]
        try:
            observation = tool.invoke(tool_call["args"])
        except Exception as e:
            observation = str(e)
        result.append(ToolMessage(content=str(observation), tool_call_id=tool_call["id"]))
    return {"messages": result}

def should_continue(state: MessagesState) -> Literal["tool_node", "__end__"]:
    if state["messages"][-1].tool_calls:
        return "tool_node"
    return END

# Construction du graph
_builder = StateGraph(MessagesState)
_builder.add_node("llm_call", llm_call)
_builder.add_node("tool_node", tool_node)
_builder.add_edge(START, "llm_call")
_builder.add_conditional_edges("llm_call", should_continue, ["tool_node", END])
_builder.add_edge("tool_node", "llm_call")

agent = _builder.compile().with_config({"recursion_limit": 10})

# Fonction d’appel d’agent
def call_agent(question: str, role: str = "user"):
    try:
        tool_calls = []
        response = agent.invoke({
            "messages": [{"role": role, "content": question}]
        })
        for msg in response["messages"]:
            if hasattr(msg, "tool_calls") and msg.tool_calls:
                tool_calls.extend(msg.tool_calls)
        return response["messages"][-1].content, tool_calls
    except GraphRecursionError:
        return {"error": "recursion_limit_reached", "message": "L'agent a atteint le nombre maximum d'itérations."}, []