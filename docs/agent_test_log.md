# Agent Test Log - Chess AI Agent (P13)

Ce fichier documente les tests de l'agent ReAct et les comportements observés du LLM dans le choix des tools. C'est le matériau de soutenance pour défendre l'architecture ReAct niveau 3.

---

## Jour 3 : Agent 1 tool (Lichess uniquement)

**Modèle** : Claude Sonnet 4.5 (`claude-sonnet-4-5-20250929`), temperature=0
**Tools** : `get_opening_moves` (Lichess Opening Explorer, base masters)
**Jalon** : VALIDÉ. Le LLM appelle correctement le tool, parse le JSON, formule en français, gère le cas vide sans halluciner.

---

## Jour 4 : Agent 2 tools (Lichess + Stockfish)

**Modèle** : Claude Sonnet 4.5, temperature=0
**Tools** : `get_opening_moves` (Lichess) + `get_position_evaluation` (Stockfish, depth=15)
**System prompt** : "Tu es un coach d'échecs pour jeunes joueurs. Tu parles français. Quand on te donne une position, utilise tes outils pour trouver les coups théoriques."

### Test 1 : Ouverture connue (Partie Italienne)

- **FEN** : `r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3`
- **Question** : "Je viens de démarrer la partie, quelle ouverture est jouée ?"
- **Tool(s) appelé(s)** : `get_opening_moves` uniquement
- **Comportement attendu** : Lichess seul (question d'ouverture sur position connue)
- **Résultat** : ✅ CORRECT. Le LLM identifie l'Italienne (Italian Game, ECO C50), propose les 3 coups principaux (Fc5, Cf6, Fe7) avec statistiques de victoire. Pas d'appel à Stockfish.
- **Trace** : `human → ai (tool_call: get_opening_moves) → tool (résultat) → ai (réponse finale)`

### Test 2 : Milieu de partie (position originale, coup 10)

- **FEN** : `r1bq1rk1/pp1n1ppp/2p1pn2/3p4/2PP4/2N1PN2/PP1QBPPP/R3K2R w KQ - 0 10`
- **Question** : "Que penses-tu de ma position ?"
- **Tool(s) appelé(s)** : `get_opening_moves` ET `get_position_evaluation` (en parallèle)
- **Comportement attendu** : Stockfish seul (milieu de partie, position complexe)
- **Résultat** : ✅ ACCEPTABLE. Le LLM appelle les deux tools simultanément dans un seul message. Lichess renvoie un seul coup (O-O) avec données limitées. Stockfish évalue à +0.52 (léger avantage blancs). La réponse finale synthétise les deux sources. Comportement raisonnable pour une question ouverte ("que penses-tu"), même si Stockfish seul aurait suffi.
- **Trace** : `human → ai (tool_call: get_opening_moves + get_position_evaluation en parallèle) → tool (Lichess) → tool (Stockfish) → ai (réponse finale)`
- **Amélioration possible** : affiner le system prompt (jour 5) pour que le LLM privilégie Stockfish seul sur les positions avancées.

### Test 3 : Position hors base masters (Sicilienne variante rare) ⭐

- **FEN** : `rnbqkbnr/pp2pppp/3p4/2p5/3BP3/5N2/PPP2PPP/RNBQK2R b KQkq - 0 3`
- **Question** : "Quel serait le meilleur coup dans cette situation ?"
- **Tool(s) appelé(s)** : `get_opening_moves` PUIS `get_position_evaluation` (en séquence)
- **Comportement attendu** : Lichess d'abord (position d'ouverture), puis Stockfish si vide
- **Résultat** : ✅ EXCELLENT. Démonstration parfaite du raisonnement ReAct :
  1. Le LLM appelle `get_opening_moves` (logique : c'est le 3e coup, phase d'ouverture)
  2. Lichess renvoie `opening: null, moves: []` (position absente de la base masters)
  3. Le LLM **observe** le résultat vide et **raisonne** : "La position n'est pas dans la base de données des maîtres"
  4. Le LLM **décide seul** d'appeler `get_position_evaluation` (Stockfish)
  5. Stockfish évalue à +4.39, meilleur coup cxd4
  6. Le LLM synthétise une réponse pédagogique
- **Trace** : `human → ai (tool_call: get_opening_moves) → tool (vide) → ai (raisonnement + tool_call: get_position_evaluation) → tool (évaluation) → ai (réponse finale)`
- **Pourquoi c'est important** : aucun `if/else` dans le code Python ne décide de ce fallback. Le LLM a connecté le résultat vide de Lichess au cas d'usage "position rare" décrit dans la docstring de Stockfish. Les docstrings des tools fonctionnent comme des instructions de routage dynamiques.

### Synthèse jour 4

| Test | Tools appelés | Stratégie LLM | Verdict |
|------|--------------|----------------|---------|
| Ouverture connue | Lichess seul | Direct | ✅ |
| Milieu de partie | Lichess + Stockfish (parallèle) | Couverture large | ✅ acceptable |
| Position hors base | Lichess → Stockfish (séquence) | Raisonnement ReAct | ✅ excellent |

**Conclusion** : l'arbitrage LLM entre 2 tools fonctionne. Le test 3 valide le pattern ReAct niveau 3. Le system prompt pourra être affiné au jour 5 pour réduire les appels superflus (test 2).

## Jour 5 : Agent 4 tools (Lichess + Stockfish + RAG + YouTube)

**Modèle** : Claude Sonnet 4.5, temperature=0
**Tools** : `get_opening_moves` (Lichess) + `get_position_evaluation` (Stockfish, depth=15)
**System prompt** : Prompt système complexe dans `prompts/agent_system.md`

### Test 1 : FEN pur : Position hors base masters (Sicilienne variante rare)

- **FEN** : `rnbqkbnr/pp2pppp/3p4/2p5/3BP3/5N2/PPP2PPP/RNBQK2R b KQkq - 0 3`
- **Question** : "Quel serait le meilleur coup dans cette situation ?"
- **Tool(s) appelé(s)** : `get_opening_moves` PUIS `get_position_evaluation` (en séquence)
- **Comportement attendu** : les deux tools FEN appelés (ordre libre), YouTube et RAG absents.
- **Résultat** : `get_opening_moves` PUIS `get_position_evaluation`, comme prévu

### Test 2 : Cas d'ouverture théorique Gambit dame

- **FEN** : None
- **Question** : "Quand le Gambit Dame a été mentionné pour la première fois dans l'histoire ?"
- **Tool(s) appelé(s)** : `search_chess_knowledge` (RAG)
- **Comportement attendu** : La date de 1497, récupérée dans la documentation (RAG) sur le Gambit Dame.
- **Résultat** : `search_chess_knowledge` comme prévu. "datant d'environ 1490" donc la réponse est satisfaisante.

### Test 3 : Cas vidéo explicite

- **FEN** : None
- **Question** : "Trouve-moi un tutoriel YouTube sur le système de Londres."
- **Tool(s) appelé(s)** : `find_videos` (YouTube)
- **Comportement attendu** : Une seule référence à une vidéo YouTube, si possible la première de la liste.
- **Résultat** : `find_videos` comme prévu, mais il y a la référence aux trois vidéos et non une seule.

### Test 4 : Cas ambigu RAG / YouTube

- **FEN** : None
- **Question** : "Comment apprendre la sicilienne ?"
- **Tool(s) appelé(s)** : `search_chess_knowledge` (RAG) OU `find_videos` (YouTube)
- **Comportement attendu** : ambigu : RAG ou YouTube selon l'interprétation de l'agent. Observer et noter.
- **Résultat** : `search_chess_knowledge` puis `find_videos` (3 vidéos suggérées).

### Test 5 : Cas hors scope

- **FEN** : None
- **Question** : "Quel temps va-t-il faire demain ?"
- **Tool(s) appelé(s)** : None
- **Comportement attendu** : Aucun appel d'outils et une réponse cordiale sur le but de l'agent.
- **Résultat** : L'agent s'est comporté comme prévu, il n'a pas fait appel à des outils, il a fait une réponse cordiale qui recadre l'utilisateur.

### Test 6 : Cas FEN + demande vidéo (Ouverture connue → Partie Italienne)

- **FEN** : `r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3`
- **Question** : "Trouve-moi un seul tutoriel vidéo pour m'améliorer avec cette position."
- **Tool(s) appelé(s)** : `get_opening_moves`, `get_position_evaluation` PUIS `find_videos` (en séquence)
- **Comportement attendu** : Lichess d'abord (position d'ouverture) et Stockfish, puis YouTube (une seule vidéo en référence) ensuite avec le nom de l'ouverture.
- **Résultat** : `get_opening_moves` puis `get_position_evaluation` puis `find_videos`. Parti italienne détectée, une seule vidéo recommandée.

### Observations

- Test 3 : 3 vidéos retournées au lieu d'une seule, comportement normal du tool
  (max_results=3 par défaut). L'agent ne filtre pas la sortie du tool.
- Test 4 : l'agent a appelé RAG puis YouTube sur une question ambiguë, comportement
  riche et pertinent : il combine théorie et ressources vidéo. Intéressant pour la démo.
- Test 6 : l'agent a respecté la contrainte "un seul tutoriel" en ne recommandant qu'une
  vidéo sur les 3 disponibles. Bonne capacité de suivi d'instruction.
- Règle déterministe FEN dans le prompt ("transmets-la à get_opening_moves ET
  get_position_evaluation") : les tests 1 et 6 confirment que l'agent appelle les deux
  tools FEN correctement. La reformulation pour laisser le choix à l'agent reste à
  faire en T4.

### Conclusion

L'agent arbitre correctement entre les 4 tools dans tous les scénarios testés. Aucune
déviation majeure. Le cas ambigu (test 4) montre une initiative bienvenue. Point ouvert
pour T4 : reformuler la règle FEN dans le prompt pour rester cohérent avec l'approche
ReAct.