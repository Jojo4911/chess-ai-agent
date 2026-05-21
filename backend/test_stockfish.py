from stockfish import Stockfish

sf = Stockfish(path=r"C:\Users\jonat\Desktop\Tools\stockfish\stockfish-windows-x86-64-avx2.exe")
sf.set_fen_position("rnbqkbnr/pppppppp/8/8/3P4/8/PPP1PPPP/RNBQKBNR b KQkq - 0 1")
print(sf.get_evaluation())
print(sf.get_best_move())
print(sf.get_top_moves(5))