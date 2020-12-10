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

    def move(self, pos_from, pos_to):
        if self.state != self.RUNNING:
            return

        self.rules.do_move(pos_from, pos_to)
        self.__update_actions()

        if not self.actions:
            if not self.rules.is_king_threaten(self.rules.state.turn):
                self.state = self.STALEMATE
            elif self.rules.state.turn == PlayerEnum.white:
                # white has no moves left and king is threaten, black won
                self.state = self.BLACK_WON
            else:
                self.state = self.WHITE_WON


    def get_actions(self):
        return legal_moves

    def __update_actions(self):
        legal_moves = []
        for file in range(8):
            for rank in range(8):
                if self.rules.state.board[file][rank].player == self.rules.state.turn:
                    moves = self.rules.get_legal_moves(Position(file, rank))
                    legal_moves += moves
        self.actions = legal_moves


if __name__ == '__main__':

    rules = ChessRulesDefault()
    game = ChessGame(rules)
    game.start_new()

    while True:
        legal_moves = []
        for file in range(8):
            for rank in range(8):
                if game.rules.state.board[file][rank].player == game.rules.state.turn:
                    moves = game.rules.get_legal_moves(Position(file, rank))
                    legal_moves += moves

        i = 0
        print(game.rules.state)
        for move in legal_moves:
            print(f"{i}: {move.move_from} -> {move.move_to}\t\t", end='')
            i += 1
            if i % 3 == 0:
                print("")
        print("")
        num = int(input("Choice: "))

        move = legal_moves[num]
        game.move(move.move_from, move.move_to)
