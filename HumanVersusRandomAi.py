from chess_backend.GameState import GameState
from chess_backend.common import PlayerEnum
from agents.HumanConsoleAgent import HumanConsoleAgent
from agents.RandomAiAgent import RandomAiAgent
from ui.console import ConsoleUi

if __name__ == '__main__':

    game = GameState()
    game.start_new()

    white = HumanConsoleAgent()
    black = RandomAiAgent()
    ui = ConsoleUi()

    idx = 1
    ui.draw_board(game.board)
    while game.state == game.RUNNING:

        if game.board.turn == PlayerEnum.white:
            selected = white.select_action(game)
        else:
            selected = black.select_action(game)

        game.apply(selected)
        ui.draw_board(game.board)
        if selected.claim_draw:
            print(f"{idx}. move chosen: claim draw")
        else:
            print(f"{idx}. move chosen: {selected.move_from} -> {selected.move_to}")

        idx += 1

    if game.state == game.WHITE_WON:
        print(f"Game finished, white won")
    elif game.state == game.BLACK_WON:
        print(f"Game finished, black won")
    elif game.state == game.STALEMATE:
        print(f"Game finished, stalemate")
    elif game.state == game.DRAW:
        print(f"Game finished, draw")
