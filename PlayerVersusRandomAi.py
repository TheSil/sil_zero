from ChessRulesDefault import ChessRulesDefault
from common import Position, PlayerEnum
from PlayerController import PlayerController
from RandomAiController import RandomAiController

class ChessGame:
    def __init__(self, rules):
        self.rules = rules

    def start_new(self):
        self.rules.setup_board()

    def move(self, pos_from, pos_to):
        self.rules.do_move(pos_from, pos_to)


def pos(str):
    return Position(ord(str[0]) - ord('a'), ord(str[1]) - ord('1'))

if __name__ == '__main__':

    rules = ChessRulesDefault()
    game = ChessGame(rules)
    game.start_new()

    white = PlayerController()
    black = RandomAiController()

    while True:
        legal_moves = []
        for file in range(8):
            for rank in range(8):
                if game.rules.state.board[file][rank].player == game.rules.state.turn:
                    moves = game.rules.get_legal_moves(Position(file, rank))
                    legal_moves += moves

        if not legal_moves:
            break

        print(game.rules.state)

        if game.rules.state.turn == PlayerEnum.white:
            num = white.request_move(game.rules.state, legal_moves)
        else:
            num = black.request_move(game.rules.state, legal_moves)

        move = legal_moves[num]
        print(f"chosen: {move.move_from} -> {move.move_to}")
        game.move(move.move_from, move.move_to)

    print("Game finished")
