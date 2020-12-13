from chess_backend.ChessRulesDefault import ChessRulesDefault
from chess_backend.common import PlayerEnum
from agents.RandomAiAgent import RandomAiAgent
from chess_backend.ChessGame import ChessGame
from ui.console import ConsoleUi


def main(do_print=True):
    rules = ChessRulesDefault()
    game = ChessGame(rules)
    game.start_new()

    white = RandomAiAgent(prefer_takes=True)
    black = RandomAiAgent(prefer_takes=True)
    ui = ConsoleUi()

    idx = 1
    while game.state == game.RUNNING:

        legal_moves = rules.legal_moves
        if game.rules.state.turn == PlayerEnum.white:
            selected = white.select_action(game.rules.state, legal_moves)
        else:
            selected = black.select_action(game.rules.state, legal_moves)

        game.move(selected)
        if do_print:
            ui.draw_board(game.rules.state)

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
