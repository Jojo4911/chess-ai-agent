from app.agent.agent import call_agent

# Test sur 3 positions

print("=== TEST 1 : Ouverture Italienne → Lichess ===")
print(call_agent(question="Je viens de démarer la partie, quelle ouverture est jouée ? La position est : r1bqkbnr/pppp1ppp/2n5/4p3/2B1P3/5N2/PPPP1PPP/RNBQK2R b KQkq - 3 3"))
print("\n=== TEST 2 : Milieu de partie originale → Stockfish ===")
print(call_agent(question="Que penses tu de ma position ? FEN : r1bq1rk1/pp1n1ppp/2p1pn2/3p4/2PP4/2N1PN2/PP1QBPPP/R3K2R w KQ - 0 10"))
print("\n=== TEST 3 : Ouverture Sicilienne avec demande de meilleur coup → Lichess + Stockfish ===")
print(call_agent(question="Quel serait le meilleur coup dans cette situation ? FEN : rnbqkbnr/pp2pppp/3p4/2p5/3BP3/5N2/PPP2PPP/RNBQK2R b KQkq - 0 3"))