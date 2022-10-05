import math, copy, re, random, time
from turtle import color
from colorama import Fore, Back, Style, init
from src.piece import Piece

class Move:
    piece = None
    origin_square_num = None
    destination_square_num = None
    castle_status_before_move = None
    en_passant_square_num_before_move = None
    capture = None
    promotion = None

    def __init__(self, piece, origin_square_num, destination_square_num, capture = None, castle_status_before_move = None, 
            en_passant_square_num_before_move = None, promotion = None):
        self.piece = piece
        self.origin_square_num = origin_square_num
        self.destination_square_num = destination_square_num
        self.capture = capture
        self.promotion = promotion
        self.castle_status_before_move = castle_status_before_move
        self.en_passant_square_num_before_move = en_passant_square_num_before_move
    
    def display(self):
        prom = '' if self.promotion is None else ('= ' + Piece.get_piece_name(self.promotion))
        capt = '' if self.capture is None else ('x ' + Piece.get_piece_name(self.capture))
        # ep = '' if self.en_passant_square_num_before_move is None else 'e-p'
        print(Piece.get_piece_name(self.piece), Board.get_square(None, self.origin_square_num), '-', Board.get_square(None, self.destination_square_num), capt, prom)
    
    def get_piece(self):
        return self.piece

    def get_capture(self):
        return self.capture
    
    def get_promotion(self):
        return self.promotion
    
    def get_origin_square_num(self):
        return self.origin_square_num
    
    def get_destination_square_num(self):
        return self.destination_square_num
    
    def get_castle_status_before_move(self):
        return self.castle_status_before_move
    
    def get_en_passant_square_num_before_move(self):
        return self.en_passant_square_num_before_move
    
    def get_notation(self, available_moves):
        """Returns the Standard Algebric Notation for the current move
    
        Attrs:
        - available_moves (list): available moves in current position, used for move disambiguation
    
        Returns:
        - string representing the notation
        """
        # TODO handle checks & mate notation ? move notation is used to treat user input

        move_piece = self.get_piece() & Piece.TYPE_MASK
        # handle castling
        if Piece.is_piece(move_piece, Piece.KING):
            if self.get_destination_square_num() == (self.get_origin_square_num() + 2):
                return 'O-O'
            elif self.get_destination_square_num() == (self.get_origin_square_num() +- 2):
                return 'O-O-O'
            
        is_capture = 'x' if self.get_capture() is not None else ''
        is_prom = ''
        if self.get_promotion() is not None:
            piece_initial = self.get_promotion() & Piece.TYPE_MASK
            if piece_initial in Piece.NAME_PIECES_INITIAL:
                is_prom = '=' + Piece.NAME_PIECES_INITIAL[piece_initial].upper()
        piece_initial = ''
        piece_disambiguation = ''
        # TODO no piece initial if pawn capture
        if Piece.is_piece(move_piece, Piece.PAWN) and self.get_capture():
            piece_initial = Board.get_square(None, self.get_origin_square_num())
            piece_initial = piece_initial[0]
        elif not Piece.is_piece(move_piece, Piece.PAWN):
            piece_initial = Piece.NAME_PIECES_INITIAL[move_piece].upper()

        if available_moves is not None:
            for tmp_move in available_moves:
                if tmp_move.get_destination_square_num() == self.get_destination_square_num() and tmp_move.get_piece() == self.get_piece() and tmp_move != self:
                    # normal ambiguous moves
                    # normal promotions
                    # ambiguous promotions
                    # check that origin square is not the same (promotions make several moves with the same origin)
                    if tmp_move.get_origin_square_num() != self.get_origin_square_num():
                        # using column (a-h) if possible
                        if Board.get_column(None, tmp_move.get_origin_square_num()) != Board.get_column(None, self.get_origin_square_num()):
                            piece_disambiguation = Board.get_column(None, self.get_origin_square_num())
                        elif Board.get_line(None, tmp_move.get_origin_square_num()) != Board.get_line(None, self.get_origin_square_num()):
                            piece_disambiguation = Board.get_line(None, self.get_origin_square_num())
                        else:
                            piece_disambiguation = Board.get_square(None, self.get_origin_square_num())

        return piece_initial + str(piece_disambiguation) + is_capture + Board.get_square(None, self.get_destination_square_num()) + is_prom
    
    def get_notation_old(self):
        move_piece = self.get_piece() & Piece.TYPE_MASK
        # handle castling
        if Piece.is_piece(move_piece, Piece.KING):
            if self.get_destination_square_num() == (self.get_origin_square_num() + 2):
                return 'O-O'
            elif self.get_destination_square_num() == (self.get_origin_square_num() +- 2):
                return 'O-O-O'
            
        is_capture = 'x' if self.get_capture() is not None else ''
        is_prom = ''
        if self.get_promotion() is not None:
            piece_initial = self.get_promotion() & Piece.TYPE_MASK
            if piece_initial in Piece.NAME_PIECES_INITIAL:
                is_prom = '=' + Piece.NAME_PIECES_INITIAL[piece_initial]
        piece_origin = ''        
        piece_initial = ''
        if Piece.is_piece(move_piece, Piece.PAWN) and self.get_capture():
            piece_initial = Board.get_square(None, self.get_origin_square_num())
            piece_initial = piece_initial[0]
        elif not Piece.is_piece(move_piece, Piece.PAWN):
            piece_initial = Piece.NAME_PIECES_INITIAL[move_piece]
            if not self.get_capture():
                is_capture = '-'
            piece_origin = Board.get_square(None, self.get_origin_square_num())

        return piece_initial + piece_origin + is_capture + Board.get_square(None, self.get_destination_square_num()) + is_prom

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
    

class Game:
    chessboard = None
    HUMAN = "human"
    RANDOM = "random"
    COMPUTER = "computer"
    STATUS_OPENING = 1
    STATUS_MIDGAME = 2
    STATUS_ENDGAME = 3
    moves_list = None

    def __init__(self, fen_code=None):
        self.chessboard = Board()
        if fen_code is not None:
            self.chessboard.load_fen(fen_code)
        self.moves_list = []

    def get_board(self):
        return self.chessboard

    def display_moves(self, available_moves):
        for tmp_move in available_moves:
            print(tmp_move.get_notation(available_moves), ' ', end='')
        print("")
    
    def make_move_on_board(self, move):
        if isinstance(move, Move):
            board = self.get_board()
            board.make_move(move)
            self.moves_list.append(move)
        else:
            print(Fore.RED + "WARNING : not a Move object" + Fore.RESET)
            print(move)

    def run(self, player_white, player_black):
        players = {Piece.WHITE: player_white, Piece.BLACK: player_black}
        board = self.get_board()
        board.iterations = {}
        board.calc_av_moves = {"calcul": 0, "load": 0}
        available_moves = board.get_available_moves()
        board_move = None
        while len(available_moves) > 0:
            board.display()
            #print(board.evaluate_position(True))
            print(Piece.get_color_name(board.color_to_move), "to play : (", len(available_moves), "available moves)")
            print("")

            #if (board.move_count-1) in board.saved_available_moves:
            #board.saved_available_moves[board.move_count-1]
            # removes saved available_moves from earlier positions
            board.saved_available_moves.pop(board.move_count-1, None)

            player_to_move = players[board.color_to_move]
            if player_to_move == self.HUMAN:
                move_input = None
                board_move = None
                while move_input is None or board_move is None:
                    move_input = input("Your move : ")
                    if move_input == "end":
                        return 0
                    elif move_input == "fen":
                        print(board.get_fen_from_position())
                        continue
                    elif move_input == "hist":
                        for move in self.moves_list:
                            print(move.get_notation(None), ' ', end='')
                        print('')
                        continue
                    elif move_input == "takeback":
                        for i in range(2):
                            if len(self.moves_list) > 0:
                                tmp_move = self.moves_list.pop()
                                print(tmp_move.get_notation(None))
                                board.unmake_move(tmp_move)
                        board.display()
                        print(Piece.get_color_name(board.color_to_move), "to play : (", len(available_moves), "available moves)")
                        print("")
                        available_moves = board.get_available_moves()
                        continue
                    elif move_input == "moves":
                        self.display_moves(available_moves)
                        continue
                    board_move = board.get_move_from_notation(move_input)
                    if board_move is not None:
                        self.make_move_on_board(board_move)
                    else:
                        print("Move not found")
                
            elif player_to_move == self.COMPUTER:
                """
                break_first_move = False
                if board.move_count == 1:
                    for tmp_move in available_moves:
                        if tmp_move.get_notation(available_moves) == "d4":
                            self.make_move_on_board(tmp_move)
                            break_first_move = True
                if break_first_move is True:
                    continue
                """

                start = time.process_time()
                #board.iterations = {}
                board.eval_pos = {"calcul": 0, "load": 0}
                board.calc_av_moves = {"calcul": 0, "load": 0}
                board.time_spent = {}
                #tmp_len_eval = len(board.saved_evaluations)
                bestscore, board_move = board.alpha_beta(4)
                end = time.process_time()

                for func, val in board.time_spent.items():
                    print(Back.BLUE + func + " : " + str(val['count']) + " -- " + str(round(val['time'], 3)) + " sec" + Back.RESET)
                #print(board.iterations)
                print(board.eval_pos)
                print(board.calc_av_moves)
                #print(tmp_len_eval, " => ", len(board.saved_evaluations))

                self.make_move_on_board(board_move)
                print("==== COMPUTER MOVES : " + Back.LIGHTCYAN_EX + " " + board_move.get_notation(available_moves) + " " + Back.RESET + " (" + str(bestscore) + ") -- (" + str(round(end-start, 3)) + " seconds)")
                """
            elif player_to_move == self.RANDOM:
                board_move = random.choice(available_moves)                    
                self.make_move_on_board(board_move)
                print("==== COMPUTER MOVES : " + Back.LIGHTCYAN_EX + " " + board_move.get_notation(available_moves) + " " + Back.RESET)
                """
            else:
                print("ERROR - player id not found")
                return None

            if board_move is not None:
                if Piece.is_piece(board_move.get_piece(), Piece.PAWN):
                    board.saved_evaluations = {}
                available_moves = board.get_available_moves()
            """
            print(len(board.saved_available_moves))
            for k, v in board.saved_available_moves.items():
                print(k, " : ", len(v))
            """

        # handle endgame (checkmate, stalemate, material draws, 50-moves rules, etc.)

        # if no moves available, end the game (mate or stalemate)
        if len(available_moves) == 0:
            board.display(True)
            if board.is_king_in_check(board.color_to_move):
                print(Back.RED + "CHECKMATE : " + Piece.get_color_name(board.get_opposing_color(board.color_to_move)) + " wins the game" + Back.RESET)
            else:
                print(Back.RED + "STALEMATE : game is a draw" + Back.RESET)

class Board:
    board = []
    available_moves = None
    move_count = 1
    half_move_count = 0
    color_to_move = None
    en_passant_square_num = None
    castle_status = None
    king_square_num = {}
    saved_evaluations = {}
    saved_available_moves = {}
    iterations = None
    eval_pos = None
    calc_av_moves = None
    time_spent = {}

    CENTER_SQUARES = [27, 28, 35, 36]
    CENTER_HALF_SQUARES = [18, 19, 20, 21, 26, 29, 34, 37, 42, 43, 44, 45]

    def __init__(self):
        self.load_fen("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
        init(convert=True)
    
    def calculate_time_spent(function):
        
        def wrapper(*args, **kwargs):
            start = time.process_time()
            result = function(*args, **kwargs)
            #args[0] == Board object
            end = time.process_time()
            func_name = str(function.__name__)
            if func_name not in args[0].time_spent:
                args[0].time_spent[func_name] = {'count': 0, 'time': 0}
            args[0].time_spent[func_name]['count'] += 1
            args[0].time_spent[function.__name__]['time'] += end-start
            #print(Fore.RED + function.__name__ + Fore.RESET + " : " + str(round(end-start, 3)) + " seconds elapsed")
            return result

        return wrapper

    def get_fen_from_position(self):
        fen_code = ''
        count_empty_squares = 0

        for line in range(7, -1, -1):
            for col in range(0, 8):
                square_num = line*8+col
                square = self.board[square_num]
                if Piece.is_piece(square, Piece.NONE):
                    count_empty_squares += 1
                else:
                    if count_empty_squares > 0:
                        fen_code += str(count_empty_squares)
                        count_empty_squares = 0
                    piece_initial = Piece.get_piece_initial(square)
                    if Piece.is_color(square, Piece.WHITE):
                        piece_initial = piece_initial.upper()
                    fen_code += piece_initial
            
            if count_empty_squares > 0:
                fen_code += str(count_empty_squares)
                count_empty_squares = 0
            if line > 0:
                fen_code += '/'

        # color to move
        color_to_move = 'w'
        if self.color_to_move == Piece.BLACK:
            color_to_move = 'b'
        
        # castle status
        castle_status = ''
        if self.castle_status[Piece.WHITE][Piece.KING] is True:
            castle_status += "K"
        if self.castle_status[Piece.WHITE][Piece.QUEEN] is True:
            castle_status += "Q"
        if self.castle_status[Piece.BLACK][Piece.KING] is True:
            castle_status += "k"
        if self.castle_status[Piece.BLACK][Piece.QUEEN] is True:
            castle_status += "q"

        # en passant square
        en_passant_square = "-"
        if self.en_passant_square_num is not None:
            en_passant_square = self.get_square(self.en_passant_square_num)

        fen_code += " " + color_to_move + " " + castle_status + " " + en_passant_square + " " + str(self.half_move_count) + " " + str(self.move_count)
        return fen_code
    
    def load_fen(self, fen_code):
        # clean board
        self.board = [Piece.NONE for i in range(64)]
        # TODO check FEN format

        fen_parts = fen_code.split(' ',)
        if len(fen_parts) != 6:
            print('ERROR in fen loading : missing parts')
        
        col = 1
        line = 8
        count_squares = 0
        # for index, char in enumerate(fen_parts[0]):
        for char in fen_parts[0]:
            square_num = (line-1)*8+(col-1)
            # print("char : ", char, " | line : ", line, " | col : ", col, " | ", square_num, " | count_squares : ", count_squares, sep='')

            if (char == '/' and col != 9) or (char != '/' and char != ' ' and col == 9):
                print('ERROR in fen loading : columns count does not match')

            # if is int : add int(char) to col AND add int(char) to count_squares
            if char.isnumeric():
                count_squares += int(char)
                col += int(char)

            # if is / AND col == 8 : line -= 1 AND reset col to 1 ELSE error
            elif char == '/':
                line -= 1
                col = 1

            # if is letter : handle piece & color AND add 1 to count_squares (if piece not found : error)
            elif char.isalpha():
                char_color = Piece.WHITE if char.isupper() else Piece.BLACK
                char = char.lower()
                if char in Piece.INITIAL_PIECES:
                    char_name = Piece.INITIAL_PIECES[char]
                    self.board[square_num] = char_name | char_color
                    if char_name == Piece.KING:
                        self.king_square_num[char_color] = square_num
                else:
                    print("ERROR in fen loading : piece initial not found")
                    
                # print(Piece.get_piece_name(char_name), " (", char, " ", char_color, ") on square ", square_num)
                count_squares += 1
                col += 1
            
            # if is space : end pieces init
            elif char == ' ':
                break

        # if count_squares != 64 THEN error
        if count_squares != 64:
            print("ERROR in fen loading : incorrect count squares")
        
        # set color to move
        self.color_to_move = Piece.WHITE if fen_parts[1] == 'w' else Piece.BLACK
        
        # set castle status
        self.castle_status = {Piece.WHITE: {Piece.KING: False, Piece.QUEEN: False}, Piece.BLACK: {Piece.KING: False, Piece.QUEEN: False}}
        if fen_parts[2] != '-':
            self.castle_status = self.get_castle_status_from_string(fen_parts[2])

        # set en passant square
        if fen_parts[3] != '-':
            self.en_passant_square_num = self.get_square_num(fen_parts[3])

        # set half move count
        if not fen_parts[4].isnumeric():
            print("ERROR in fen loading : wrong format for half move count")
        self.half_move_count = int(fen_parts[4])
        
        # set move count
        if not fen_parts[5].isnumeric():
            print("ERROR in fen loading : wrong format for move count")
        self.move_count = int(fen_parts[5])

    def display(self, full_info = False):
        balance = self.get_material_balance()
        if balance > 0:
            balance = '+' + str(balance)
        print("Move ", self.move_count, " - ", ("White" if self.color_to_move == Piece.WHITE else "Black"), " to move  (", balance, ")", sep='')
        print('========== BOARD ==========')
        print('')
        for line in range (7, -1, -1):
            for col in range (0, 8):
                square_index = (line*8) + col
                if (square_index + line) % 2 == 0:
                    print(Back.GREEN + " ", end='')
                else:
                    print(Back.YELLOW + " ", end='')
                piece_display = " "
                current_piece = self.board[square_index]
                piece_color = (Fore.WHITE if Piece.is_color(current_piece, Piece.WHITE) == 1 else Fore.BLACK)

                piece_display = Piece.get_piece_initial(current_piece, True)
                print(piece_color + piece_display + Fore.RESET, " ", sep='', end='')
            print(Back.RESET + ' ', line+1)
        
        for i in range (0, 8):
            print (" ", chr(ord('a') + i), " ", sep='', end='')
        print(Back.RESET)
        if full_info:
            print(self.king_square_num)
            print(self.castle_status)
            print("En passant : ", self.en_passant_square_num)
            """
            available_moves = self.get_available_moves()
            print(len(available_moves), " available moves")
            """
        print("==================")

    def get_square(self, square_number):
        square = None
        if square_number >= 0 and square_number <= 63:
            line = 1 + math.floor(square_number/8)
            col = 1 + square_number % 8
            square = chr(ord('a') + col - 1) + str(line)
        else:
            print("WARNING : square out of board range : ", square_number)
        return square
    
    def get_square_num(self, square):
        square_num = None
        match = re.match(r"^[a-h][1-8]$", square)
        if match is None:
            print("Incorrect square coordinates")
        else:
            square_num = ord(square[0]) - 97 + (int(square[1]) - 1) * 8
        return square_num
    
    def square_has_allied_piece(self, destination_square_num, current_piece_color):
        destination_square_piece = self.board[destination_square_num]
        return (destination_square_piece != Piece.NONE) and Piece.is_color(destination_square_piece, current_piece_color)
    
    def square_has_enemy_piece(self, destination_square_num, current_piece_color):
        destination_square_piece = self.board[destination_square_num]
        return (destination_square_piece != Piece.NONE) and (not Piece.is_color(destination_square_piece, current_piece_color))
    
    def get_line(self, square_number):
        return 1 + math.floor(square_number/8)

    def get_column(self, square_number):
        return chr(ord('a') + square_number % 8)

    def get_column_number(self, square_number):
        return 1 + square_number % 8

    def square_is_line(self, square_number, line_number):
        line = 1 + math.floor(square_number/8)
        return (line == line_number)

    def square_is_column(self, square_number, column_number):
        col = 1 + square_number % 8
        return (col == column_number)

    def get_opposing_color(self, color):
        return Piece.WHITE if color == Piece.BLACK else Piece.BLACK

    def compress_castle_status(self):
        castle_status = ''
        if self.castle_status[Piece.WHITE][Piece.KING] is True:
            castle_status += "K"
        if self.castle_status[Piece.WHITE][Piece.QUEEN] is True:
            castle_status += "Q"
        if self.castle_status[Piece.BLACK][Piece.KING] is True:
            castle_status += "k"
        if self.castle_status[Piece.BLACK][Piece.QUEEN] is True:
            castle_status += "q"
        return castle_status
    
    def get_castle_status_from_string(self, castle_status_string):
        castle_status = {Piece.WHITE: {Piece.KING: False, Piece.QUEEN: False}, Piece.BLACK: {Piece.KING: False, Piece.QUEEN: False}}
        for char in castle_status_string:
            current_color = Piece.BLACK
            if not char.isalpha() or not (char in Piece.INITIAL_PIECES or char.lower() in Piece.INITIAL_PIECES):
                print("ERROR in fen loading : wrong castle initial")
            else:
                if char.isupper():
                    current_color = Piece.WHITE

                current_side = Piece.INITIAL_PIECES[char.lower()]
                if current_side == Piece.KING or current_side == Piece.QUEEN:
                    castle_status[current_color][current_side] = True
        return castle_status

    def get_move_from_notation(self, notation):
        if notation == '0-0':
            notation = 'O-O'
        if notation == '0-0-0':
            notation = 'O-O-O'
        found_move = None
        available_moves = self.get_available_moves()
        for move in available_moves:
            if move.get_notation(available_moves) == notation:
                found_move = move
        return found_move

    def alpha_beta(self, depth, initial_depth=None, alpha=-10000, beta=10000):
        if initial_depth is None:
            initial_depth = depth
        """
        if depth not in self.iterations:
            self.iterations[depth] = 0
        self.iterations[depth] += 1
        """
        if depth == initial_depth:
            max_time = 180
            start = time.process_time()
        """
        Returns a tuple (score, bestmove) for the position at the given depth
        """
        #print(Back.CYAN + " ALPHA-BETA depth " + str(depth) + "  (" + str(alpha) + " | " + str(beta) + ") " + Back.RESET)
        available_moves = self.get_available_moves()
        if depth == 0 or len(available_moves) == 0:
            fen_code = self.get_fen_from_position()
            evaluation = 0
            if fen_code in self.saved_evaluations:
                evaluation = self.saved_evaluations[fen_code]
                self.eval_pos['load'] += 1
            else:
                evaluation = self.evaluate_position(False)
                self.saved_evaluations[fen_code] = evaluation
                self.eval_pos['calcul'] += 1
            
            return (evaluation, None)
        else: 
            if self.color_to_move == Piece.WHITE:
                bestmove = None
                index = 0
                for current_move in available_moves:
                    if depth == initial_depth:
                        end = time.process_time()
                        if end - start > max_time:
                            print(Fore.RED + "BREAK - Only " + str(index) + " moves explored" + Fore.RESET)
                            break
                    # make move
                    self.make_move(current_move)
                    index += 1

                    # get next depth
                    score, tmp_move = self.alpha_beta(depth - 1, initial_depth, alpha, beta)
                    # tmp_move is the last response move which was tested before breaking

                    # unmake move
                    self.unmake_move(current_move)

                    if score > alpha: # white maximizes her score
                        alpha = score
                        bestmove = current_move
                        if alpha >= beta: # alpha-beta cutoff
                            #print("break (depth ", depth, ") - ", index, "/", len(available_moves), sep='')
                            break
                return (alpha, bestmove)
            else:
                # color_to_move = BLACK
                bestmove = None
                index = 0
                for current_move in available_moves:
                    if depth == initial_depth:
                        end = time.process_time()
                        if end - start > max_time:
                            print("BREAK - Only ", index, " moves explored")
                            break
                    # make move
                    self.make_move(current_move)
                    index += 1

                    # get next depth
                    score, tmp_move = self.alpha_beta(depth - 1, initial_depth, alpha, beta)
                    
                    # unmake move
                    self.unmake_move(current_move)

                    if score < beta: # black minimizes his score
                        beta = score
                        bestmove = current_move
                        if alpha >= beta: # alpha-beta cutoff
                            #print("break (depth ", depth, ") - ", index, "/", len(available_moves), sep='')
                            break
                
                return (beta, bestmove)

    def make_move(self, move: Move):
        origin_square_num = move.get_origin_square_num()
        destination_square_num = move.get_destination_square_num()
        piece = move.get_piece()
        piece_color = Piece.get_color(piece)
        piece_promotion = move.get_promotion()
        if piece_promotion is not None:
            piece = piece_promotion
        self.board[destination_square_num] = piece
        self.board[origin_square_num] = Piece.NONE
        
        # handle en passant square
        if destination_square_num == move.get_en_passant_square_num_before_move() and Piece.is_piece(piece, Piece.PAWN):
            # manually remove pawn taken this way
            if self.square_is_line(destination_square_num, 3):
                self.board[destination_square_num+8] = Piece.NONE
            elif self.square_is_line(destination_square_num, 6):
                self.board[destination_square_num-8] = Piece.NONE
        
        if Piece.is_piece(piece, Piece.PAWN) and destination_square_num == (origin_square_num + 16):
            self.en_passant_square_num = origin_square_num + 8
        elif Piece.is_piece(piece, Piece.PAWN) and destination_square_num == (origin_square_num - 16):
            self.en_passant_square_num = origin_square_num - 8
        else:
            self.en_passant_square_num = None
        
        # handle castling
        if Piece.is_piece(piece, Piece.KING) and destination_square_num == origin_square_num+2:
            castle_rook = self.board[origin_square_num+3]
            self.board[origin_square_num+3] = Piece.NONE
            self.board[origin_square_num+1] = castle_rook
        elif Piece.is_piece(piece, Piece.KING) and destination_square_num == origin_square_num-2:
            castle_rook = self.board[origin_square_num-4]
            self.board[origin_square_num-4] = Piece.NONE
            self.board[origin_square_num-1] = castle_rook

        # update piece position
        if Piece.is_piece(piece, Piece.KING):
            self.king_square_num[piece_color] = destination_square_num
            # set castle status
            self.castle_status[piece_color] = {Piece.QUEEN: False, Piece.KING: False}
        elif Piece.is_piece(piece, Piece.ROOK):
            # set castle status
            if self.castle_status[piece_color][Piece.QUEEN] is True and self.square_is_column(origin_square_num, 1):
                self.castle_status[piece_color][Piece.QUEEN] = False
            elif self.castle_status[piece_color][Piece.KING] is True and self.square_is_column(origin_square_num, 8):
                self.castle_status[piece_color][Piece.KING] = False

        # update moves count
        if piece_color == Piece.BLACK:
            self.move_count += 1
        
        # TODO update half moves count -- used for 50-move draw rule
        
        # switch color to play
        self.color_to_move = Piece.WHITE if piece_color == Piece.BLACK else Piece.BLACK
        # reset available moves as the board has changed
        self.available_moves = None
        # color_to_move and move_count OK
        
    def unmake_move(self, move: Move):        
        origin_square_num = move.get_origin_square_num()
        destination_square_num = move.get_destination_square_num()
        en_passant_square_num_before_move = move.get_en_passant_square_num_before_move()
        piece = move.get_piece()
        piece_color = Piece.get_color(piece)
        opposing_color = self.get_opposing_color(piece_color)
        piece_promotion = move.get_promotion()
        piece_captured = move.get_capture()
        if piece_captured is None:
            piece_captured = Piece.NONE
        else:
            piece_captured = piece_captured | opposing_color

        # reset move + handle promotion
        if piece_promotion is not None:
            piece = Piece.PAWN | piece_color
        self.board[origin_square_num] = piece

        # handle en passant particular capture case
        if en_passant_square_num_before_move == destination_square_num and Piece.is_piece(piece, Piece.PAWN) and move.get_capture() is not None:
            # reset taken pawn
            if self.square_is_line(destination_square_num, 3):
                self.board[destination_square_num+8] = Piece.PAWN | opposing_color
            elif self.square_is_line(destination_square_num, 6):
                self.board[destination_square_num-8] = Piece.PAWN | opposing_color
            piece_captured = Piece.NONE
        
        # reset destination square (nothing in case of en passant capture)
        self.board[destination_square_num] = piece_captured
            
        # reset en passant square_num
        self.en_passant_square_num = en_passant_square_num_before_move
        
        # handle castling
        if Piece.is_piece(piece, Piece.KING) and destination_square_num == origin_square_num+2:
            castle_rook = self.board[origin_square_num+1]
            self.board[origin_square_num+3] = castle_rook
            self.board[origin_square_num+1] = Piece.NONE
        elif Piece.is_piece(piece, Piece.KING) and destination_square_num == origin_square_num-2:
            castle_rook = self.board[origin_square_num-1]
            self.board[origin_square_num-4] = castle_rook
            self.board[origin_square_num-1] = Piece.NONE

        # update piece position
        if Piece.is_piece(piece, Piece.KING):
            self.king_square_num[piece_color] = origin_square_num
        
        if Piece.is_piece(piece, Piece.KING) or Piece.is_piece(piece, Piece.ROOK):
            # set back original castle status
            castle_status_before_move = move.get_castle_status_before_move()
            castle_status_before_move = self.get_castle_status_from_string(castle_status_before_move)

            if castle_status_before_move != self.castle_status:
                self.castle_status = castle_status_before_move
        
        # update moves count if we unmake a white move
        if piece_color == Piece.BLACK:
            self.move_count -= 1
        # switch color to play : back to the color which moved
        self.color_to_move = piece_color
        # reset available moves as the board has changed
        self.available_moves = None
        # color_to_move and move_count OK
        
    def get_piece_attacked_squares(self, square_num):
        squares = []
        current_piece = self.board[square_num]
        if current_piece == Piece.NONE:
            return []

        current_piece_color = Piece.get_color(current_piece)
        move_squares = []

        # get piece available moves if the board was clear, then add allied/enemy pieces
        
        # handle sliding pieces : QUEEN - BISHOP - ROOK
        if Piece.is_sliding_piece(current_piece):
            if Piece.is_rook_or_queen(current_piece):
                # add +8 +16 +24 etc. while those destination squares are <= 63
                move_square_distance = 8
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while (square_num+move_square_distance) <= 63:
                    slide_destination_square_num = square_num + move_square_distance
                    
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))
                        
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1
                    
                    move_square_distance += 8

                # add -8 -16 -24 etc. while those destination squares are >= 0
                move_square_distance = -8
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while (square_num+move_square_distance) >= 0:
                    slide_destination_square_num = square_num + move_square_distance
                    
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))
                        
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1
                    
                    move_square_distance -= 8

                # add +1 +2 +3 etc. while those destination squares are not on column 8
                move_square_distance = 0
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while not self.square_is_column(square_num+move_square_distance, 8):
                    move_square_distance += 1
                    slide_destination_square_num = square_num + move_square_distance
                    
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))
                        
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1

                # add -1 -2 -3 etc. while those destination squares are not on column 1
                move_square_distance = 0
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while not self.square_is_column(square_num+move_square_distance, 1):
                    move_square_distance -= 1
                    slide_destination_square_num = square_num + move_square_distance
                    
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))
                        
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1

            if Piece.is_bishop_or_queen(current_piece):
                # add +7 +14 +21 etc. while those destination squares are not on column 1 & <= 63
                move_square_distance = 0
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while not self.square_is_column(square_num+move_square_distance, 1):
                    move_square_distance += 7
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) > 63:
                        break
                        
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))

                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1

                # add +9 +18 +27 etc. while those destination squares are not on column 8 & <= 63
                move_square_distance = 0
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while not self.square_is_column(square_num+move_square_distance, 8):
                    move_square_distance += 9
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) > 63:
                        break
                        
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))

                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1

                # add -7 -14 -21 etc. while those destination squares are empty & not on column 8 & >= 0
                move_square_distance = 0
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while not self.square_is_column(square_num+move_square_distance, 8):
                    move_square_distance -= 7
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) < 0:
                        break
                        
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))
                        
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1

                # add -9 -18 -27 etc. while those destination squares are empty & not on column 1 & >= 0
                move_square_distance = 0
                count_allied_pieces = 0
                count_enemy_pieces = 0
                while not self.square_is_column(square_num+move_square_distance, 1):
                    move_square_distance -= 9
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) < 0:
                        break
                    
                    squares.append(PieceToSquare(slide_destination_square_num, self.board[slide_destination_square_num] & Piece.TYPE_MASK, 
                        self.board[slide_destination_square_num] & Piece.COLOR_MASK, count_allied_pieces, count_enemy_pieces))

                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        count_allied_pieces += 1

                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        count_enemy_pieces += 1

            # END sliding pieces if
        else:
            if Piece.is_piece(current_piece, Piece.KING):
                move_squares = [-8, 8]
                if not self.square_is_column(square_num, 1):
                    move_squares += [+7, -1, -9]
                if not self.square_is_column(square_num, 8):
                    move_squares += [-7, 1, 9]
            
            # KNIGHT
            elif Piece.is_piece(current_piece, Piece.KNIGHT):
                if not self.square_is_column(square_num, 1):
                    move_squares += [-17, 15]
                    if not self.square_is_column(square_num, 2):
                        move_squares += [-10, 6]
                if not self.square_is_column(square_num, 8):
                    move_squares += [-15, 17]
                    if not self.square_is_column(square_num, 7):
                        move_squares += [-6, 10]
            
            # PAWNS attack only diagonal squares
            elif Piece.is_piece(current_piece, Piece.PAWN):
                # if not on column 1 and square has an enemy piece, add -9 or +7
                move_square_distance = 7 if current_piece_color == Piece.WHITE else -9
                move_destination_square_num = square_num+move_square_distance
                if move_destination_square_num >= 0 and move_destination_square_num <= 63 and not self.square_is_column(square_num, 1):
                    move_squares += [move_square_distance]
                    
                # if not on column 8 and square has an enemy piece, add -7 or +9
                move_square_distance = 9 if current_piece_color == Piece.WHITE else -7
                move_destination_square_num = square_num+move_square_distance
                if move_destination_square_num >= 0 and move_destination_square_num <= 63 and not self.square_is_column(square_num, 8):
                    move_squares += [move_square_distance]
            
            for coord in move_squares:
                destination_square_num = square_num + coord
                # check if destination is outside the board
                if destination_square_num < 0 or destination_square_num > 63:
                    continue

                destination_square_piece = self.board[destination_square_num]
                squares.append(PieceToSquare(destination_square_num, destination_square_piece & Piece.TYPE_MASK, 
                    destination_square_piece & Piece.COLOR_MASK))

        return squares

    def get_piece_available_moves(self, square_num, check_king_in_check = True, check_available_castle = True):
        available_moves = []
        
        current_piece = self.board[square_num]
        if current_piece == Piece.NONE:
            return []

        current_piece_color = Piece.get_color(current_piece)
        move_squares = []
        # check availables moves depending on piece type
        if Piece.is_piece(current_piece, Piece.KING):
            move_squares = [-8, 8]
            if not self.square_is_column(square_num, 1):
                move_squares += [+7, -1, -9]
            if not self.square_is_column(square_num, 8):
                move_squares += [-7, 1, 9]
            if check_available_castle:
                opposing_color = self.get_opposing_color(current_piece_color)
                is_king_attacked = self.is_square_attacked_by_color(square_num, opposing_color)
                # check only if squares N and N+1 are attacked, as square N+2 is the destination square and will be checked afterwards
                if (self.castle_status[current_piece_color][Piece.KING] and 
                        self.board[square_num+3] == Piece.ROOK | current_piece_color and
                        self.board[square_num+1] == Piece.NONE and
                        self.board[square_num+2] == Piece.NONE and
                        is_king_attacked is False and
                        self.is_square_attacked_by_color(square_num+1, opposing_color) is False):
                    move_squares += [2]
                if (self.castle_status[current_piece_color][Piece.QUEEN] and
                        self.board[square_num-4] == Piece.ROOK | current_piece_color and
                        self.board[square_num-1] == Piece.NONE and
                        self.board[square_num-2] == Piece.NONE and
                        self.board[square_num-3] == Piece.NONE and
                        is_king_attacked is False and
                        self.is_square_attacked_by_color(square_num-1, opposing_color) is False):
                    move_squares += [-2]

        elif Piece.is_piece(current_piece, Piece.KNIGHT):
            if not self.square_is_column(square_num, 1):
                move_squares += [-17, 15]
                if not self.square_is_column(square_num, 2):
                    move_squares += [-10, 6]
            if not self.square_is_column(square_num, 8):
                move_squares += [-15, 17]
                if not self.square_is_column(square_num, 7):
                    move_squares += [-6, 10]
        elif Piece.is_sliding_piece(current_piece):
            if Piece.is_rook_or_queen(current_piece):
                # add +8 +16 +24 etc. while those destination squares are empty and <= 63
                move_square_distance = 8
                while (square_num+move_square_distance) <= 63:
                    slide_destination_square_num = square_num + move_square_distance
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break
                    move_square_distance += 8

                # add -8 -16 -24 etc. while those destination squares are empty and >= 0
                move_square_distance = -8
                while (square_num+move_square_distance) >=0:
                    slide_destination_square_num = square_num + move_square_distance
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break
                    move_square_distance -= 8

                # add +1 +2 +3 etc. while those destination squares are empty & not on column 8
                move_square_distance = 0
                while not self.square_is_column(square_num+move_square_distance, 8):
                    move_square_distance += 1
                    slide_destination_square_num = square_num + move_square_distance
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break

                # add -1 -2 -3 etc. while those destination squares are empty & not on column 1
                move_square_distance = 0
                while not self.square_is_column(square_num+move_square_distance, 1):
                    move_square_distance -= 1
                    slide_destination_square_num = square_num + move_square_distance
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break

            if Piece.is_bishop_or_queen(current_piece):
                # add +7 +14 +21 etc. while those destination squares are empty & not on column 1 & <= 63
                move_square_distance = 0
                while not self.square_is_column(square_num+move_square_distance, 1):
                    move_square_distance += 7
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) > 63:
                        break
                        
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break

                # add +9 +18 +27 etc. while those destination squares are empty & not on column 8 & <= 63
                move_square_distance = 0
                while not self.square_is_column(square_num+move_square_distance, 8):
                    move_square_distance += 9
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) > 63:
                        break
                        
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break

                # add -7 -14 -21 etc. while those destination squares are empty & not on column 8 & >= 0
                move_square_distance = 0
                while not self.square_is_column(square_num+move_square_distance, 8):
                    move_square_distance -= 7
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) < 0:
                        break
                        
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break

                # add -9 -18 -27 etc. while those destination squares are empty & not on column 1 & >= 0
                move_square_distance = 0
                while not self.square_is_column(square_num+move_square_distance, 1):
                    move_square_distance -= 9
                    slide_destination_square_num = square_num + move_square_distance
                    if (slide_destination_square_num) < 0:
                        break
                        
                    # Allied piece found : break before adding move
                    if self.square_has_allied_piece(slide_destination_square_num, current_piece_color):
                        break

                    move_squares += [move_square_distance]

                    # Enemy piece found : break before adding move
                    if self.square_has_enemy_piece(slide_destination_square_num, current_piece_color):
                        break

        elif Piece.is_piece(current_piece, Piece.PAWN):
            color_direction = 1
            if current_piece_color == Piece.BLACK:
                color_direction = -1

            # if not on column 1 and square has an enemy piece, add -9 or +7
            move_square_distance = 7 if current_piece_color == Piece.WHITE else -9
            move_destination_square_num = square_num+move_square_distance
            if move_destination_square_num >= 0 and move_destination_square_num <= 63:
                if not self.square_is_column(square_num, 1) and (move_destination_square_num == self.en_passant_square_num or (self.board[move_destination_square_num] != Piece.NONE and not Piece.is_color(self.board[move_destination_square_num], current_piece_color))):
                    move_squares += [move_square_distance]
                
            # if not on column 8 and square has an enemy piece, add -7 or +9
            move_square_distance = 9 if current_piece_color == Piece.WHITE else -7
            move_destination_square_num = square_num+move_square_distance
            if move_destination_square_num >= 0 and move_destination_square_num <= 63:
                if not self.square_is_column(square_num, 8) and (move_destination_square_num == self.en_passant_square_num or (self.board[move_destination_square_num] != Piece.NONE and not Piece.is_color(self.board[move_destination_square_num], current_piece_color))):
                    move_squares += [move_square_distance]

            # pawn push
            front_square = square_num+(8*color_direction)
            front_square_double = square_num+(16*color_direction)
            if front_square >= 0 and front_square <= 63:
                if self.board[front_square] == Piece.NONE:
                    move_squares += [8*color_direction]
                    if ((current_piece_color == Piece.WHITE and self.square_is_line(square_num, 2)) or (current_piece_color == Piece.BLACK and self.square_is_line(square_num, 7))) and self.board[front_square_double] == Piece.NONE:
                        move_squares += [16*color_direction]

        # get castle status before move
        castle_status_before_move = self.compress_castle_status()

        for coord in move_squares:
            move_is_capture = None
            destination_square_num = square_num + coord
            # check if destination is outside the board
            if destination_square_num < 0 or destination_square_num > 63:
                continue

            # check if there is allied piece
            destination_square_piece = self.board[destination_square_num]
            #print(Back.GREEN + "test color in destination square : " + str(current_piece_color) + Back.RESET)
            if destination_square_piece != Piece.NONE:
                # Allied piece found
                if Piece.is_color(destination_square_piece, current_piece_color):
                    #print(Fore.RED + "****allied piece found****" + Fore.RESET)
                    continue

                # Enemy piece found
                if not Piece.is_color(destination_square_piece, current_piece_color):
                    move_is_capture = destination_square_piece
                    # print(Fore.RED + "****enemy piece found : ", Piece.get_piece_name(destination_square_piece), "****" + Fore.RESET)

            elif Piece.is_piece(current_piece, Piece.PAWN) and destination_square_num == self.en_passant_square_num:
                #print("Move : ", square_num, "-", destination_square_num, " -- SETTING en passant : ", self.en_passant_square_num)
                move_is_capture = Piece.PAWN
            
            current_move = Move(current_piece, square_num, destination_square_num, move_is_capture, 
                castle_status_before_move, self.en_passant_square_num)

            # check if any moves puts our king in check
            if check_king_in_check:
                # make move
                self.make_move(current_move)

                # discard move if king is in check
                if self.is_king_in_check(current_piece_color):
                    #print("KING in check - discard move")
                    self.unmake_move(current_move)
                    continue

                # unmake move
                self.unmake_move(current_move)

            # handle captures enemy pieces
            # handle king castling (check that rook has not moved yet AND is still on its starting square / has not been captured)
            # handle en passant captures (careful about double pins !)

            # add piece moves to global moves
            # handle pawn promotion
            if Piece.is_piece(current_piece, Piece.PAWN) and ((current_piece_color == Piece.WHITE and self.square_is_line(destination_square_num, 8)) or (current_piece_color == Piece.BLACK and self.square_is_line(destination_square_num, 1))):
                for promotion_piece in [Piece.QUEEN, Piece.ROOK, Piece.BISHOP, Piece.KNIGHT]:
                    tmp_move = copy.deepcopy(current_move)
                    tmp_move.promotion = promotion_piece | current_piece_color
                    available_moves.append(tmp_move)
            else:
                available_moves.append(current_move)

        return available_moves
    
    def sort_moves(self, move:Move):
        weight = 0
        if move.get_capture() is not None:
            piece_type = move.get_piece() & Piece.TYPE_MASK
            capture_piece_type = move.get_capture() & Piece.TYPE_MASK
            weight += 5*Piece.EVALUATION_PIECES[capture_piece_type]/(2*Piece.EVALUATION_PIECES[piece_type]+1)
        if move.get_promotion() is not None:
            piece_type = move.get_promotion() & Piece.TYPE_MASK
            weight += Piece.EVALUATION_PIECES[piece_type] + 0.2
        if Piece.is_piece(move.get_piece(), Piece.PAWN):
            weight -= 0.1
        # TODO if move is check : +10
        return weight

    @calculate_time_spent
    def get_available_moves(self, color = None, check_king_in_check = True, check_available_castle = True):
        fen_code = self.get_fen_from_position()
        if self.move_count not in self.saved_available_moves:
            self.saved_available_moves[self.move_count] = {}
        if fen_code in self.saved_available_moves[self.move_count]:
            self.calc_av_moves['load'] += 1
            return self.saved_available_moves[self.move_count][fen_code]
        
        tmp_safeguard = copy.deepcopy(self.king_square_num)
        if color is None:
            color = self.color_to_move
        available_moves = []
        
        for square_num in range (0, 64):
            current_piece = self.board[square_num]
            if current_piece == Piece.NONE:
                continue
            current_piece_color = Piece.get_color(current_piece)
            if current_piece_color != color:
                continue
            
            # check availables moves for piece on square
            available_moves = available_moves + self.get_piece_available_moves(square_num, check_king_in_check, check_available_castle)

            #print("available moves : ", square_num)
            #self.display()
        # print(Fore.GREEN + str(len(available_moves)) + " moves available" + Fore.RESET)

        # sort available moves
        available_moves.sort(reverse=True, key=self.sort_moves)

        if tmp_safeguard != self.king_square_num:
            print("********* ERROR *********")
            print("START : ", tmp_safeguard)
            print("END : ", self.king_square_num)
            self.display(True)
        
        self.saved_available_moves[self.move_count][fen_code] = available_moves
        self.calc_av_moves['calcul'] += 1
        return available_moves

    # returns true if the king of a given color is able to get captured on the next move by any of the opposing color pieces
    # does not verify if a king-capturing move sets its own king in check (as pinned pieces can still check the opposing king)
    def is_king_in_check(self, color):
        #print("================== Is king in check ? ", Piece.get_color_name(color))
        is_in_check = False
        
        for square_num in range(0,64):
            current_piece = self.board[square_num]
            if current_piece == Piece.NONE:
                continue
            current_piece_color = Piece.get_color(current_piece)
            # get opposing color pieces one by one
            if current_piece_color != color:
                piece_moves = self.get_piece_available_moves(square_num, False, False)
                for move in piece_moves:
                    if move.get_destination_square_num() == self.king_square_num[color]:
                        return True

        """
        available_moves = self.get_available_moves(self.get_opposing_color(color), False, False)
        for move in available_moves:
            if move.get_destination_square_num() == self.king_square_num[color]:
                is_in_check = True
                break
        """
        return is_in_check

    def is_square_attacked_by_color(self, square_num, color):
        is_attacked = False
        available_moves = self.get_available_moves(color, False, False)
        for move in available_moves:
            # handle particular case : pawn pushes don't actually attack a given square, even if they can move onto it
            if Piece.is_piece(move.get_piece(), Piece.PAWN) and move.get_capture() is None:
                continue
            if move.get_destination_square_num() == square_num:
                is_attacked = True
                break
        return is_attacked
        
    def get_material_balance(self):
        balance = 0
        for square in self.board:
            if not Piece.is_piece(square, Piece.NONE):
                piece_color = 1 if Piece.get_color(square) == Piece.WHITE else -1
                piece_type = square & Piece.TYPE_MASK
                balance += Piece.EVALUATION_PIECES[piece_type]*piece_color
        return balance

    # evaluation position :
    # TODO find unprotected pieces or weak pawns in opponent's position
    # TODO malus for undevelopped pieces
    @calculate_time_spent
    def evaluate_position(self, debug = False):
        """Evaluates the current board position
    
        Attrs:
        - debug (bool): display specific evaluation for each piece
    
        Returns:
        - board evaluation as a float number, positive if white has the advantage, negative if black
        """
        evaluation = {Piece.WHITE: 0, Piece.BLACK: 0}
        available_moves = self.get_available_moves(self.color_to_move)
        
        game_status = Game.STATUS_MIDGAME
        if self.move_count <= 12:
            game_status = Game.STATUS_OPENING
        elif self.move_count >= 35:
            game_status = Game.STATUS_ENDGAME
        
        if len(available_moves) == 0:
            if self.is_king_in_check(self.color_to_move):
                evaluation_diff = 1000 if self.color_to_move == Piece.BLACK else -1000
            else:
                evaluation_diff = 0
            return evaluation_diff

        # TODO HANDLE GAME STATE
        # if no queens on the board / enough traded material ? : endgame

        # set king near squares:
        king_near_squares = {Piece.WHITE: [], Piece.BLACK: []}
        for tmp_color in [Piece.WHITE, Piece.BLACK]:
            for tmp_sqr in [-7, -8, -9, -1, 1, 7, 8, 9]:
                tmp_sqr_near = self.king_square_num[tmp_color] + tmp_sqr
                if tmp_sqr_near >= 0 and tmp_sqr_near <= 63:
                    king_near_squares[tmp_color].append(tmp_sqr_near)

        for square_num, square in enumerate(self.board):
            if not Piece.is_piece(square, Piece.NONE):
                defending_piece_rate = {Piece.KING: 0, Piece.QUEEN: 2, Piece.ROOK: 3, Piece.BISHOP: 6, Piece.KNIGHT: 6, Piece.PAWN: 4}
                attacking_piece_rate = {Piece.KING: 20, Piece.QUEEN: 10, Piece.ROOK: 6, Piece.BISHOP: 3, Piece.KNIGHT: 3, Piece.PAWN: 1}
                piece_color = Piece.get_color(square)
                piece_opposing_color = self.get_opposing_color(piece_color)
                piece_type = square & Piece.TYPE_MASK
                color_direction = 1 if piece_color == Piece.WHITE else -1
                piece_bonus = 0

                if debug is True:
                    print(Back.GREEN + " " + Back.RESET + self.get_square(square_num) + Back.GREEN + " " + Piece.get_color_name(piece_color) + " " + Piece.get_piece_name(piece_type) + Back.RESET)
                # get attacked squares :
                attacked_squares = self.get_piece_attacked_squares(square_num)
                for tmp_square in attacked_squares:
                    if tmp_square.piece_type != Piece.NONE:
                        if tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces >= 4:
                            # too many pieces in the way
                            continue

                        #print(" === ")
                        #tmp_square.display()
                        if tmp_square.piece_color == piece_color:
                            # defending allied piece
                            
                            # sliding pieces : defending bonus cancelled if more than 1 piece behind
                            piece_bonus_ratio = 1
                            if tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces == 1:
                                piece_bonus_ratio = 0.3
                            elif tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces > 1:
                                piece_bonus_ratio = 0

                            piece_bonus += defending_piece_rate[tmp_square.piece_type]*piece_bonus_ratio/12
                            
                            if debug is True:
                                print("- defending square bonus : ", round(defending_piece_rate[tmp_square.piece_type]*piece_bonus_ratio/10, 2), " -- ", defending_piece_rate[tmp_square.piece_type])
                            
                            if tmp_square.piece_type == Piece.PAWN and piece_type == Piece.PAWN:
                                # BONUS for pawn defending pawn
                                piece_bonus += 0.25
                            elif tmp_square.piece_type == Piece.ROOK and piece_type == Piece.ROOK:
                                # BONUS for connected rooks
                                piece_bonus += 0.4*piece_bonus_ratio

                            if debug is True:
                                #print("Allied piece defended : ", Piece.get_piece_name(tmp_square.piece_type), "through ", tmp_square.count_allied_pieces, tmp_square.count_enemy_pieces, " => ", round(piece_bonus, 2))
                                pass

                        else:
                            # attacking enemy piece : piece value/(count_enemy_pieces+count_allied_pieces)
                            attacking_piece_bonus = 1
                            # bonus if attacking with a lower value piece
                            if (not Piece.is_piece(piece_type, Piece.KING)) and Piece.EVALUATION_PIECES[piece_type] < Piece.EVALUATION_PIECES[tmp_square.piece_type]:
                                attacking_piece_bonus *= 2.5

                            piece_bonus_ratio = attacking_piece_bonus/pow(2, (tmp_square.count_allied_pieces+tmp_square.count_enemy_pieces))
                            piece_bonus += attacking_piece_rate[tmp_square.piece_type]*piece_bonus_ratio/10
                            
                            if debug is True:
                                print("- attacking square bonus : ", round(attacking_piece_rate[tmp_square.piece_type]*piece_bonus_ratio/7, 2), " -- ", attacking_piece_rate[tmp_square.piece_type])
                                #print("Attacking enemy piece : ", Piece.get_piece_name(tmp_square.piece_type), "through ", tmp_square.count_allied_pieces, tmp_square.count_enemy_pieces, " => ", round(piece_bonus, 2))
                                
                        
                    # bonus for attacking a square near the opponent's king
                    if tmp_square.square_num in king_near_squares[piece_opposing_color]:
                        piece_bonus += 0.8/pow(2, (tmp_square.count_allied_pieces+tmp_square.count_enemy_pieces))
                        if debug is True:
                            print("- bonus near king square :", round(0.8/pow(2, (tmp_square.count_allied_pieces+tmp_square.count_enemy_pieces)), 2))

                    if tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces == 0:
                        # bonus for each controlled square -- only if no piece in between
                        piece_bonus += 0.2
                        if debug is True:
                            print("- bonus controlled empty square : 0.2")
                    if tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces <= 1:
                        # bonus for controlling center squares
                        if tmp_square.square_num in self.CENTER_SQUARES:
                            piece_bonus += 0.2/(tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces+1)
                            if debug is True:
                                print("- bonus controlled center square :", round(0.2/(tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces+1), 2))
                        elif tmp_square.square_num in self.CENTER_HALF_SQUARES:
                            piece_bonus += 0.1/(tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces+1)
                            if debug is True:
                                print("- bonus controlled center half square :", round(0.1/(tmp_square.count_allied_pieces + tmp_square.count_enemy_pieces+1), 2))
                
                # pieces occupying the center of the board
                if square_num in self.CENTER_SQUARES:
                    piece_bonus += 0.4
                    if Piece.is_piece(square, Piece.PAWN):
                        piece_bonus += 2.2
                        if debug is True:
                            print("- bonus pawn on center square : 2.2")
                elif square_num in self.CENTER_HALF_SQUARES:
                    piece_bonus += 0.3
                
                if Piece.is_piece(square, Piece.PAWN):
                    # penalty for center pawn on its origin square
                    if game_status == Game.STATUS_OPENING and square_num in [11, 12, 51, 52]:
                        piece_bonus -= 4
                        if debug is True:
                            print("- malus original square in opening : -4")

                    # pawn bonus depending on line closer to promotion
                    line = self.get_line(square_num)-1
                    column = self.get_column_number(square_num)
                    if piece_color == Piece.BLACK:
                        line = 7 - line
                    piece_bonus += line*line*line/50

                    # pawn bonus defending the king on adjacent columns
                    king_square_line = self.get_line(self.king_square_num[piece_color])
                    king_square_column = self.get_column_number(self.king_square_num[piece_color])
                    if piece_color == Piece.BLACK:
                        king_square_line = 9 - king_square_line
                    if king_square_line < 3 and abs(king_square_column - column) <= 1 and line <= 1:
                        piece_bonus += 1

                elif Piece.is_piece(square, Piece.ROOK):
                    # + rook on semi-open/open column
                    # TODO make a specific method ?
                    column_has_allied_pawn = False
                    column_has_enemy_pawn = False
                    allied_pawn = Piece.PAWN | piece_color
                    enemy_pawn = Piece.PAWN | piece_opposing_color
                    tmp_square_num = square_num + 8*color_direction

                    while tmp_square_num >= 0 and tmp_square_num <= 63:
                        if self.board[tmp_square_num] == enemy_pawn:
                            column_has_enemy_pawn = True
                        elif self.board[tmp_square_num] == allied_pawn:
                            column_has_allied_pawn = True
                            break
                        tmp_square_num += 8*color_direction

                    if column_has_allied_pawn is False:
                        piece_bonus += 0.4
                        if column_has_enemy_pawn is False:
                            piece_bonus += 0.6

                elif Piece.is_piece(square, Piece.KING):
                    # handle king safety
                    column = self.get_column_number(square_num)
                    # check if king still on center of the board
                    if column in [4,5,6]:
                        piece_bonus += -4
                        # check if it can castle
                        if not (self.castle_status[piece_color][Piece.KING] & self.castle_status[piece_color][Piece.QUEEN]):
                            piece_bonus += -3

                elif game_status == Game.STATUS_OPENING and Piece.is_piece(square, Piece.BISHOP) or Piece.is_piece(square, Piece.KNIGHT):
                    # penalty for bishop/knight on its origin square
                    if square_num in [1, 2, 5, 6, 57, 58, 61, 62]:
                        piece_bonus -= 2
                        if debug is True:
                            print("- malus original square in opening : -2")
                elif Piece.is_piece(square, Piece.QUEEN):
                    pass

                # get all possible moves, weight with captures, checks and promotions
                
                evaluation[piece_color] += Piece.EVALUATION_PIECES[piece_type] + piece_bonus/4

                if debug is True:
                    # self.get_square(square)
                    print(Piece.get_color_name(piece_color), Piece.get_piece_name(square), "in", self.get_square(square_num), " : ", Piece.EVALUATION_PIECES[piece_type], " + ", round(piece_bonus/4, 2))

        evaluation[Piece.WHITE] = round(evaluation[Piece.WHITE], 2)
        evaluation[Piece.BLACK] = round(evaluation[Piece.BLACK], 2)
        return round(evaluation[Piece.WHITE] - evaluation[Piece.BLACK], 2)

    def count_available_moves(self, color, depth):
        if color is None:
            color = self.color_to_move
        available_moves = self.get_available_moves(color)
        if depth <= 1:
            return len(available_moves)
        else:
            count_moves = 0
            for move in available_moves:
                # make move
                self.make_move(move)

                # count moves with new position
                count_moves += self.count_available_moves(depth-1)

                # unmake move
                self.unmake_move(move)
            return count_moves

