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
