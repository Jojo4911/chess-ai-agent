## J1 - 29/05/2025

### Décisions techniques
- Contrat d'erreur : ToolException pour pannes runtime, EnvironmentError pour config manquante.
- Validation FEN : ValidFen (Pydantic) + python-chess, branché sur les deux tools.
- Boucle ReAct bornée : recursion_limit=10 (9 étapes max réalistes + 1 marge).
- Agent sorti de scripts/ vers app/agent/agent.py, call_agent() expose l'interface.

### Fichiers modifiés
app/schemas/chess.py, app/services/lichess_service.py, app/services/stockfish_service.py,
app/tools/lichess_tool.py, app/tools/stockfish_tool.py, app/agent/agent.py (nouveau),
backend/scripts/agent_minimal_testing.py

### Points ouverts
- call_agent() retourne un dict d'erreur sur GraphRecursionError : à câbler proprement sur l'endpoint FastAPI en J2.