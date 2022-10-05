from src.piece import Piece

class PieceToSquare:
    square_num = None
    piece_type = None
    piece_color = None
    count_allied_pieces = 0
    count_enemy_pieces = 0

    def __init__(self, square_num, piece_type, piece_color, count_allied_pieces = 0, count_enemy_pieces = 0):
        self.square_num = square_num
        self.piece_type = piece_type
        self.piece_color = piece_color
        self.count_allied_pieces = count_allied_pieces
        self.count_enemy_pieces = count_enemy_pieces
    
    def display(self):
        piece_name = '[ ]' if self.piece_type == Piece.NONE else Piece.get_piece_name(self.piece_type)
        print("PieceToSquare [", self.square_num, "] : ", Piece.get_color_name(self.piece_color), " ", piece_name, " (", 
            self.count_allied_pieces, "A / ", self.count_enemy_pieces, "E)", sep='')
    