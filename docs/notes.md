## Jour 3 : Premier tool Lichess + jalon tool calling

### Problèmes rencontrés et résolus :

* PowerShell aliase `curl` vers `Invoke-WebRequest` (un outil Microsoft différent), ce qui provoquait des 401 fantômes. Solution : utiliser Git Bash systématiquement, ou `curl.exe` dans PowerShell.
* L'API Opening Explorer Lichess exige un token Bearer depuis février 2026 (suite à la panne OVH). Avant c'était ouvert. Le token se génère sur `lichess.org/account/oauth/token` et se stocke en variable d'environnement.
* Import `ModuleNotFoundError` : lancer les scripts avec `uv run python -m` depuis `backend/` ou `PYTHONPATH=`. uv run python pour que Python trouve le package `app`.
* `StructuredTool does not support sync invocation` : les tools async ne fonctionnent pas directement avec `create_agent`. Solution : garder le tool synchrone (`httpx.Client`), l'async reviendra avec FastAPI.
* Ne pas mettre `@tool` sur la fonction service, uniquement sur le wrapper dans `tools/`.

### Décisions techniques :

* Architecture : séparation `schemas/` (modèles Pydantic), `services/` (logique API), `tools/` (wrappers LangGraph).
* Le tool retourne des données structurées (JSON), pas du texte pré-formaté. C'est le LLM qui formule en langage naturel.
* Option B pour le fallback masters/lichess : on reste sur masters uniquement, le LLM observe le résultat vide et décide de sa prochaine action (Stockfish). Cohérent avec l'architecture ReAct niveau 3.
* Top 5 coups triés explicitement par nombre total de parties, même si l'API semble déjà triée (code défensif).
* `opening` retourné comme `None` (pas de chaîne vide) quand la position n'a pas d'ouverture identifiée.

### Jalon validé :

* Claude Sonnet 4.5 appelle correctement le tool, parse le JSON, formule en français, gère le cas vide sans halluciner. Architecture ReAct confirmée, feu vert pour les tools suivants.

## Jour 4 : Tool Stockfish + agent ReAct 2 tools

### Réalisé
- Installation Stockfish : binaire Windows + lib Python `stockfish` via `uv add stockfish`
- Variable d'environnement `STOCKFISH_PATH` dans `.env` (le binaire change de nom entre Windows et Docker Linux)
- Variable d'environnement `STOCKFISH_DEPTH` (défaut 15)
- Schémas Pydantic dans `schemas/stockfish.py` : `PositionEvaluation` (avec `Literal["cp", "mate"]`), `TopMove`, `StockfishResponse`
- Service `services/stockfish_service.py` : fonction `evaluate_position(fen, depth)` retournant un `StockfishResponse`
- Tool LangGraph `tools/stockfish_tool.py` : `get_position_evaluation` avec docstring discriminante par rapport à Lichess
- Agent 2 tools testé sur 3 scénarios (voir `docs/agent_test_log.md`)
- Tests unitaires : 2 tests (position normale + position de mat), tous passés

### Problèmes rencontrés
- `AttributeError: 'Stockfish' object has no attribute '_stockfish'` : le nom de l'exécutable était incorrect dans le path (le binaire s'appelle `stockfish-windows-x86-64-avx2.exe`, pas `stockfish.exe`)
- `os.getenv()` renvoie une string : penser à `int()` pour STOCKFISH_DEPTH
- Pydantic n'accepte pas les arguments positionnels : utiliser les arguments nommés ou l'unpack `**dict`
- Les clés retournées par la lib Stockfish sont en majuscules (`Move`, `Centipawn`, `Mate`) alors que les champs Pydantic sont en minuscules : mapping manuel nécessaire

### Acquis consolidés
- Pattern service/tool identique à Lichess : le wrapper tool appelle le service et retourne `model_dump_json()`
- List comprehension pour transformer une liste de dicts en liste d'objets Pydantic
- Unpack de dict avec `**` pour construire un objet Pydantic depuis un dict
- Docstrings des tools comme instructions de routage pour le LLM (pas de la doc passive)

### Observation clé (soutenance)
Test 3 (position hors base masters) : le LLM appelle Lichess, observe un résultat vide, puis décide seul d'appeler Stockfish. Aucun `if/else` dans le code Python. C'est le raisonnement ReAct niveau 3 en action : les docstrings des deux tools se complètent et permettent au LLM de raisonner dynamiquement. C'est l'argument central pour défendre l'architecture.

### Prochaine étape (jour 5)
- System prompt soigné (persona entraîneur FFE, règles métier)
- Gestion erreurs et timeouts sur les appels API/Stockfish
- Validation Pydantic des entrées (FEN valide, etc.)
- Logging structuré