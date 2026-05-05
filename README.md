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

Tools exposés à l'agent :
- `get_theoretical_moves` : statistiques d'ouverture via Lichess
- `evaluate_with_stockfish` : analyse de position
- `search_chess_knowledge` : RAG sur Wikichess (Milvus)
- `find_videos` : recherche pédagogique YouTube

## Prérequis

- Docker Desktop (avec Docker Compose v2)
- Git
- Clés API : Anthropic, YouTube Data v3

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

├── backend/         # API FastAPI + agent LangGraph + tools
├── frontend/        # Application Angular
├── data/            # Données brutes (gitignoré, à régénérer via scripts)
├── docs/            # Documentation, note MCP, schémas
├── infra/           # Configurations Milvus, MongoDB, services
├── prompts/         # System prompt agent + templates
├── scripts/         # Utilitaires de dev (download, populate, seed)
├── docker-compose.yml
├── .env.example
└── README.md

## Statut du projet

Projet en cours de développement (POC). Voir `docs/` pour la roadmap et la note de faisabilité MCP.

## Auteur

Jonathan Fernandez, formation AI Engineer OpenClassrooms.