from chess_backend.GameState import GameState
from chess_backend.common import PlayerEnum
from agents.AiAgent import AiAgent
from ui.console import ConsoleUi
from random import random


class DummyNetwork:

    def __call__(self, game_state):
        return [random() for _ in game_state.legal_moves], 0.5

def main(do_print=True):
    game= GameState()
    game.start_new()

    net = DummyNetwork()
    white = AiAgent(net)
    black = AiAgent(net)
    ui = ConsoleUi()

    idx = 1
    while game.state == game.RUNNING:

        if game.board.turn == PlayerEnum.white:
            selected = white.select_action(game)
        else:
            selected = black.select_action(game)

        game.apply(selected)
        if do_print:
            ui.draw_board(game.board)

        idx += 1

    if do_print:
        if game.state == game.WHITE_WON:
            print(f"Game finished, white won")
        elif game.state == game.BLACK_WON:
            print(f"Game finished, black won")
        elif game.state == game.STALEMATE:
            print(f"Game finished, stalemate")
        elif game.state == game.DRAW:
            print(f"Game finished, draw")


if __name__ == '__main__':
    main()

    # import cProfile
    # cProfile.run('main(do_print=False)', sort="tottime")
