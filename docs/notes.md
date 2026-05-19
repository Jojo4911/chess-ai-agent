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