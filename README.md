# Agent IA pour la Fédération Française des Échecs

POC d'agent IA conversationnel d'aide à l'apprentissage des ouvertures aux échecs, destiné aux jeunes espoirs de la FFE.

## Stack technique

- **Backend** : Python, FastAPI, LangGraph (agent ReAct), MongoDB
- **Vectorstore** : Milvus
- **Moteur d'analyse** : Stockfish
- **APIs externes** : Lichess Opening Explorer, YouTube Data v3
- **LLM** : Claude Sonnet 4.5 (Anthropic)
- **Frontend** : Angular, ngx-chess-board
- **Orchestration** : Docker Compose

## Architecture

Agent ReAct au sens moderne : le LLM choisit lui-même quel(s) tool(s) appeler en fonction de la question utilisateur et de la position d'échecs courante. Aucune logique de routage codée en dur côté Python.

```mermaid
flowchart TD
    A([__start__]) --> B(ReAct agent)
    B -. tool_calls .-> Tools
    Tools --> B
    B -. no tool_calls .-> C([__end__])
    subgraph Tools
        direction TB
        D(get_opening_moves)
        E(get_position_evaluation)
        F(search_chess_knowledge)
        G(find_videos)
    end
```

### Tools exposés à l'agent

| Tool | Source | Description |
|------|--------|-------------|
| `get_opening_moves` | Lichess Opening Explorer (base masters) | Statistiques d'ouverture : coups les plus joués, taux de victoire, nom de l'ouverture |
| `get_position_evaluation` | Stockfish (depth 15) | Évaluation objective d'une position : score en centipawns ou mat, meilleur coup, top 5 coups |
| `search_chess_knowledge` | Milvus (RAG sur Wikichess) | Contexte théorique et historique sur les ouvertures |
| `find_videos` | YouTube Data v3 | Recherche de vidéos pédagogiques sur les ouvertures |

### Arbitrage LLM (ReAct niveau 3)

Le LLM orchestre les tools via leurs docstrings, sans `if/else` côté Python :
- Position d'ouverture connue : appelle Lichess pour la théorie des maîtres.
- Position rare ou milieu/fin de partie : appelle Stockfish pour l'évaluation objective.
- Lichess renvoie un résultat vide : le LLM observe et bascule sur Stockfish de lui-même.
- Question sur l'histoire d'une ouverture : appelle le RAG Wikichess.
- Demande de ressource vidéo : appelle YouTube.

## Prérequis

- Docker Desktop (avec Docker Compose v2)
- Git
- Stockfish (binaire système)
- Clés API : Anthropic, Lichess, YouTube Data v3

## Installation rapide

```bash
git clone <repo-url>
cd <repo-name>
cp .env.example .env
# Renseigner les clés API dans .env
docker compose up --build
```

L'application sera accessible sur :
- Frontend : http://localhost:4200
- Backend API : http://localhost:8000
- Swagger : http://localhost:8000/docs

## Structure du projet

```
├── backend/
│   ├── app/
│   │   ├── schemas/          # Modèles Pydantic (lichess.py, stockfish.py)
│   │   ├── services/         # Logique métier API (lichess_service.py, stockfish_service.py)
│   │   └── tools/            # Wrappers @tool LangGraph (lichess_tool.py, stockfish_tool.py)
│   ├── scripts/              # Scripts de test (test_agent_minimal.py)
│   └── tests/                # Tests unitaires pytest
├── frontend/                 # Application Angular (à venir)
├── data/                     # Données brutes (gitignoré, à régénérer via scripts)
├── docs/                     # Documentation, note MCP, test log agent
├── infra/                    # Configurations Milvus, MongoDB, services
├── prompts/                  # System prompt agent + templates
├── scripts/                  # Utilitaires de dev (download, populate, seed)
├── docker-compose.yml
├── .env.example
└── README.md
```

## Avancement

- [x] Étape 1 : Environnement (repo, Docker Compose, FastAPI hello world)
- [x] Étape 2a : Tool Lichess (service + schemas Pydantic + tool LangGraph)
- [x] Étape 2b : Tool Stockfish (service + schemas Pydantic + tool LangGraph)
- [x] Jalon tool calling validé (agent 1 tool, puis agent 2 tools)
- [ ] Étape 2c : System prompt soigné + gestion erreurs/timeouts
- [ ] Étape 2d : Endpoints FastAPI
- [ ] Étape 3 : RAG Milvus (ingestion Wikichess + tool search)
- [ ] Étape 4 : Tool YouTube
- [ ] Étape 5 : Frontend Angular
- [ ] Étape 6 : Packaging Docker Compose final
- [ ] Étape 7 : Étude de faisabilité MCP

## Auteur

Jonathan Fernandez, formation AI Engineer OpenClassrooms.