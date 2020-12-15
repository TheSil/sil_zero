from chess_backend.GameState import GameState
from chess_backend.common import PlayerEnum
from agents.RandomAiAgent import RandomAiAgent
from agents.AiAgent import AiAgent

class DummyNetwork:

    def __call__(self, game_state):
        count = len(game_state.legal_moves)
        policy = [1/count] * count
        value = 0
        return policy, value

def main(do_print=True):
    net = DummyNetwork()
    white = RandomAiAgent()
    black = AiAgent(net)

    game_number = 1
    white_wins = 0
    black_wins = 0
    draws = 0
    all = 0
    while True:

        game = GameState()
        game.start_new()

        idx = 1
        while game.state == game.RUNNING:

            if game.board.turn == PlayerEnum.white:
                selected = white.select_action(game)
            else:
                selected = black.select_action(game)

            game.apply(selected)
            idx += 1

        if game.state == game.WHITE_WON:
            white_wins += 1
        elif game.state == game.BLACK_WON:
            black_wins += 1
        elif game.state == game.STALEMATE:
            draws += 1
        elif game.state == game.DRAW:
            draws += 1
        all += 1

        print(f"{game_number:4d}: "
              f"white_wins:{(100 * white_wins) / all:3.2f}%\t"
              f"black_wins:{(100 * black_wins) / all:3.2f}%\t"
              f"draws:{(100 * draws) / all:3.2f}%")
        game_number += 1


if __name__ == '__main__':
    main()

    # import cProfile
    # cProfile.run('main(do_print=False)', sort="tottime")
