from chess_backend.GameState import GameState
from chess_backend.common import PlayerEnum
from agents.RandomAiAgent import RandomAiAgent
from ui.console import ConsoleUi


def main(do_print=True):
    game = GameState()
    game.start_new()

    white = RandomAiAgent(prefer_takes=True)
    black = RandomAiAgent(prefer_takes=True)
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
