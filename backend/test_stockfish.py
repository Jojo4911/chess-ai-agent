from stockfish import Stockfish

sf = Stockfish(path=r"C:\Users\jonat\Desktop\Tools\stockfish\stockfish-windows-x86-64-avx2.exe")
sf.set_fen_position("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1") # Test de base
#sf.set_fen_position("8/8/8/8/8/8/4K3/4k3 w - - 0 1") # Test pat, roi contre roi
#sf.set_fen_position("") # Test avec FEN invalide (vide)
print(sf.get_evaluation())
print(sf.get_best_move())
print(sf.get_top_moves(5))