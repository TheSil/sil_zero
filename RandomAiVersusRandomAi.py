from chess_backend.GameState import GameState
from chess_backend.Session import Session
from agents.RandomAiAgent import RandomAiAgent
from ui.console import ConsoleUi


def main(do_print=True):
    game = GameState()
    game.start_new()

    white = RandomAiAgent(prefer_takes=True)
    black = RandomAiAgent(prefer_takes=True)
    ui = ConsoleUi()

    session = Session(game, white, black)
    session.before_move(lambda: ui.draw_board(game.board))
    session.play()

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
