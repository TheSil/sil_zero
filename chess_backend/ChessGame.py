from common import Position, PlayerEnum, PieceEnum
import copy

only_king = {
            PieceEnum.pawn: 0,
            PieceEnum.rook: 0,
            PieceEnum.knight: 0,
            PieceEnum.bishop: 0,
            PieceEnum.queen: 0,
            PieceEnum.king: 1
           }
king_bishop = {
            PieceEnum.pawn: 0,
            PieceEnum.rook: 0,
            PieceEnum.knight: 0,
            PieceEnum.bishop: 1,
            PieceEnum.queen: 0,
            PieceEnum.king: 1
           }
king_knight = {
            PieceEnum.pawn: 0,
            PieceEnum.rook: 0,
            PieceEnum.knight: 1,
            PieceEnum.bishop: 0,
            PieceEnum.queen: 0,
            PieceEnum.king: 1
           }

class ChessGame:

    NOT_STARTED = 0
    RUNNING = 1
    WHITE_WON = 2
    BLACK_WON = 3
    STALEMATE = 4
    DRAW = 5

    def __init__(self, rules):
        self.rules = rules
        self.state = self.NOT_STARTED
        self.actions = None

    def start_new(self):
        self.rules.setup_board()
        self.__update_actions()
        self.state = self.RUNNING

    def move(self, action_index):
        if self.state != self.RUNNING:
            return

        action = self.actions[action_index]
        self.rules.move(action)
        self.__update_actions()

        if not self.actions:
            if not self.rules.is_king_threaten(self.rules.state.turn):
                self.state = self.STALEMATE
            elif self.rules.state.turn == PlayerEnum.white:
                # white has no moves left and king is threaten, black won
                self.state = self.BLACK_WON
            else:
                self.state = self.WHITE_WON

        # basic draw conditions checking
        white_counts = {
            PieceEnum.pawn: 0,
            PieceEnum.rook: 0,
            PieceEnum.knight: 0,
            PieceEnum.bishop: 0,
            PieceEnum.queen: 0,
            PieceEnum.king: 0,
        }
        white_even_bishops = 0
        white_odd_bishops = 0
        black_even_bishops = 0
        black_odd_bishops = 0
        black_counts = copy.copy(white_counts)

        for file in range(8):
            for rank in range(8):
                if self.rules.state.board[file][rank].player == PlayerEnum.white:
                    white_counts[self.rules.state.board[file][rank].piece] += 1
                    if self.rules.state.board[file][rank].piece == PieceEnum.bishop:
                        if file + rank % 2 == 0:
                            white_even_bishops += 1
                        else:
                            white_odd_bishops += 1

                elif self.rules.state.board[file][rank].player == PlayerEnum.black:
                    black_counts[self.rules.state.board[file][rank].piece] += 1
                    if self.rules.state.board[file][rank].piece == PieceEnum.bishop:
                        if file + rank % 2 == 0:
                            black_even_bishops += 1
                        else:
                            black_odd_bishops += 1

        if white_counts == only_king:
            if black_counts == only_king or \
               black_counts == king_bishop or \
               black_counts == king_knight:
                self.state = self.DRAW

        if black_counts == only_king:
            if white_counts == only_king or \
               white_counts == king_bishop or \
               white_counts == king_knight:
                self.state = self.DRAW

        if black_counts == king_bishop and white_counts == king_bishop:
            if white_even_bishops == black_even_bishops and \
                white_odd_bishops == black_odd_bishops:
                self.state = self.DRAW


    def __update_actions(self):
        legal_moves = []
        for file in range(8):
            for rank in range(8):
                if self.rules.state.board[file][rank].player == self.rules.state.turn:
                    moves = self.rules.get_legal_moves(Position(file, rank))
                    legal_moves += moves
        self.actions = legal_moves
