from ChessRulesDefault import ChessRulesDefault
from common import Position, PlayerEnum

class ChessGame:

    NOT_STARTED = 0
    RUNNING = 1
    WHITE_WON = 2
    BLACK_WON = 3
    STALEMATE = 4

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

    def __update_actions(self):
        legal_moves = []
        for file in range(8):
            for rank in range(8):
                if self.rules.state.board[file][rank].player == self.rules.state.turn:
                    moves = self.rules.get_legal_moves(Position(file, rank))
                    legal_moves += moves
        self.actions = legal_moves
