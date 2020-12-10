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
