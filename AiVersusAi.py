from random import random

from agents.AiAgent import AiAgent
from chess_backend.GameState import GameState
from ui.console import ConsoleUi
import numpy as np


class DummyNetwork:

    def __call__(self, game_state):
        count = len(game_state.legal_moves)
        policy = [1/count] * count
        value = 0
        return policy, value


def main(do_print=True):
    game = GameState()
    game.start_new()

    net = DummyNetwork()
    agent = AiAgent(net)
    ui = ConsoleUi()

    idx = 1
    while game.state == game.RUNNING:
        selected = agent.select_action(game)
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
