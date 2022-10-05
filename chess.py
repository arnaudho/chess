from src.piece import Piece
from src.board import Game, Move, Board
from colorama import Fore, Back, Style, init
init(autoreset=False)


game = Game()
game.run("human", "computer")



"""

print("========== TEST CASES ============")
print("======================")
list = [
    Piece.NONE,
    Piece.KING | Piece.BLACK,
    Piece.PAWN | Piece.BLACK,
    Piece.KNIGHT | Piece.BLACK,
    Piece.BISHOP | Piece.BLACK,
    Piece.ROOK | Piece.BLACK,
    Piece.QUEEN | Piece.BLACK,
]
for piece in list:
    print("TESTING ALL COMBINATIONS ===========")
    print("Testing ", piece)
    print(piece == Piece.NONE)
    print(Piece.is_piece(piece, Piece.NONE))
    print("---")
    print(Piece.is_piece(piece, Piece.KING))
    print(Piece.is_piece(piece, Piece.PAWN))
    print(Piece.is_piece(piece, Piece.KNIGHT))
    print(Piece.is_piece(piece, Piece.BISHOP))
    print(Piece.is_piece(piece, Piece.ROOK))
    print(Piece.is_piece(piece, Piece.QUEEN))
    print("is rook/queen : " , Piece.is_rook_or_queen(piece))
    print("is bishop/queen : " , Piece.is_bishop_or_queen(piece))
    print("is sliding piece : " , Piece.is_sliding_piece(piece))

# Testing pieces colors

print("========== PIECES COLORS & NAMES ============")
list = [
    Piece.NONE,
    Piece.KING | Piece.BLACK,
    Piece.PAWN | Piece.BLACK,
    Piece.KNIGHT | Piece.BLACK,
    Piece.BISHOP | Piece.WHITE,
    Piece.ROOK | Piece.WHITE,
    Piece.QUEEN | Piece.WHITE,
]
for piece in list:
    print(piece, " color : ", Piece.get_color_name(piece), " -- name : ", Piece.get_piece_name(piece))

board = Board()
for num in range(-1, 66):
    square = board.get_square(num)
    if square:
        print("Case ", num, " : ", square)
        print("col 1 : ", board.square_is_line(num, 1))
        print("col 2 : ", board.square_is_column(num, 2))
        
# Testing all squares
print("========== SQUARES ============")
for num in range(-1, 66):
    square = board.get_square(num)
    if square:
        print("Case ", num, " : ", square)

"""
"""
print('===== TEST available moves on specific positions =====')
board = Board()
fen_code = None
# TEST en passant
#fen_code = "rnbqkbnr/p1ppppp1/8/Pp5p/8/8/1PPPPPPP/RNBQKBNR w KQkq b6 0 3"
# TEST castle + test checks
#fen_code = "r3k3/p1P5/7r/7p/5Q1b/8/PP1P3P/R3K1BR w KQq - 0 8"
# TEST promotion
#fen_code = "b3k3/1Pp5/2K5/8/8/8/8/8 w - - 0 1"
# fen_code = "8/8/8/8/5k2/4rn2/3PPP2/3NKR2 w - - 0 1"
# Perft position 3
#fen_code = "8/2p5/3p4/KP5r/1R3p1k/8/4P1P1/8 w - - 0 1"
# Perft position 4
#fen_code = "r3k2r/Pppp1ppp/1b3nbN/nP6/BBP1P3/q4N2/Pp1P2PP/R2Q1RK1 w kq - 0 1"
# Test ambiguous moves
#fen_code = "rnbq1bnr/1pppkppp/8/4p3/p3P3/RP1N1N2/2P1K3/RB6 w - - 0 2"
if fen_code is not None:
    board.load_fen(fen_code)

board.display(True)
available_moves = board.get_available_moves()
print(len(available_moves), "moves available")
"""




"""
board = Board()
# TEST position evaluation - COMPARE 2 boards

fen_code = "rnbqkbnr/pppppppp/8/8/8/2N5/PPPPPPPP/R1BQKBNR b KQkq - 0 1"
board.load_fen(fen_code)
evaluation = board.evaluate_position(True)
print(Back.RED + str(evaluation) + Back.RESET)
board.display()

fen_code = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq - 0 1"
board.load_fen(fen_code)
evaluation = board.evaluate_position(True)
print(Back.RED + str(evaluation) + Back.RESET)
board.display()
"""

"""
# TEST Perft depth - check moves count in depths 4-5-6 etc.
# https://www.chessprogramming.org/Perft_Results

for depth in [1,2,3,4]:
    start = time.process_time()
    moves = board.count_available_moves(depth)
    end = time.process_time()
    print("DEPTH ", depth, " - available moves : ", moves, " (", round(end-start, 3), " seconds)")
"""
