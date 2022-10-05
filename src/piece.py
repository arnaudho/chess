class Piece:
    NONE = 0
    KING = 1
    PAWN = 2
    KNIGHT = 3
    BISHOP = 5
    ROOK = 6
    QUEEN = 7

    WHITE = 8
    BLACK = 16

    TYPE_MASK = 0b00111
    COLOR_MASK = WHITE | BLACK

    NAME_PIECES = {KING:"king", QUEEN:"queen", ROOK:"rook", BISHOP:"bishop", KNIGHT:"knight", PAWN:"pawn"}
    PIECES_INITIALS_DISPLAY = {KING:"K", QUEEN:"Q", ROOK:"R", BISHOP:"B", KNIGHT:"N", PAWN:"o"}
    NAME_PIECES_INITIAL = {KING:"k", QUEEN:"q", ROOK:"r", BISHOP:"b", KNIGHT:"n", PAWN:"p"}
    INITIAL_PIECES = {"k":KING, "q":QUEEN, "r":ROOK, "b":BISHOP, "n":KNIGHT, "p":PAWN}
    EVALUATION_PIECES = {KING: 0, QUEEN: 9, ROOK: 5, BISHOP: 3, KNIGHT: 3, PAWN: 1}

    def get_color(piece):
        return piece & Piece.COLOR_MASK

    def get_color_name(piece):
        name = ""
        color = piece & Piece.COLOR_MASK
        if color == Piece.BLACK:
            name = "black"
        elif color == Piece.WHITE:
            name = "white"
        return name
    
    def get_piece_name(piece):
        name = " "
        piece = piece & Piece.TYPE_MASK
        if piece in Piece.NAME_PIECES:
            name = Piece.NAME_PIECES[piece]
        else:
            print("WARNING : piece name not found : ", piece)
        return name
    
    def get_piece_initial(piece, display=False):
        name = " "
        piece = piece & Piece.TYPE_MASK
        if piece in Piece.NAME_PIECES_INITIAL:
            if display is True:
                name = Piece.PIECES_INITIALS_DISPLAY[piece]
            else:
                name = Piece.NAME_PIECES_INITIAL[piece]
        else:
            pass
        return name
    
    def is_color(test_piece, color):
        return (test_piece & Piece.COLOR_MASK) == color
    
    def is_piece(test_piece, piece_type):
        return piece_type == (test_piece & Piece.TYPE_MASK)
    
    def is_bishop_or_queen(piece):
        return piece & 0b101 == 0b101

    def is_rook_or_queen(piece):
        return piece & 0b110 == 0b110

    def is_sliding_piece(piece):
        return piece & 0b100 != 0
