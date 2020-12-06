from ChessRulesDefault import ChessRulesDefault
from common import Position

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

    # moves = [
    #     (pos('a2'), pos('a4')),
    #     (pos('d7'), pos('d6')),
    #     (pos('a4'), pos('a5')),
    #     (pos('b7'), pos('b5')),
    #     (pos('a5'), pos('b6'))
    # ]

    moves = [
        (pos('e2'), pos('e4')),
        (pos('e7'), pos('e5')),
        (pos('g1'), pos('f3')),
        (pos('b8'), pos('c6')),
        (pos('f1'), pos('c4')),
        (pos('f8'), pos('c5')),
        (pos('c2'), pos('c3')),
        (pos('g8'), pos('f6')),
        (pos('d2'), pos('d4')),
        (pos('e5'), pos('d4')),
        (pos('e4'), pos('e5')),
        (pos('f6'), pos('e4')),
        (pos('c4'), pos('d5')),
        (pos('e4'), pos('f2')),
        (pos('e1'), pos('f2')),
        (pos('d4'), pos('c3')),
        (pos('f2'), pos('g3')),
        (pos('c3'), pos('b2')),
        (pos('c1'), pos('b2')),
        (pos('c6'), pos('e7')),
        (pos('f3'), pos('g5')),
        (pos('e7'), pos('d5')),
        (pos('g5'), pos('f7')),
        (pos('e8'), pos('g8')),
        (pos('f7'), pos('d8')),
        (pos('c5'), pos('f2')),
        (pos('g3'), pos('h3')),
        (pos('d7'), pos('d6')),
        (pos('e5'), pos('e6')),
        (pos('d5'), pos('f4')),
        (pos('h3'), pos('g4')),
        (pos('f4'), pos('e6')),
        (pos('d8'), pos('e6')),
        (pos('c8'), pos('e6')),
        (pos('g4'), pos('g5')),
        (pos('f8'), pos('f5')),
        (pos('g5'), pos('g4')),
        (pos('h7'), pos('h5')),
        (pos('g4'), pos('g3')),
        (pos('f5'), pos('f3')),
    ]

    for move in moves:
        game.move(*move)
        print(game.rules.state)
