from chess_backend.ChessRulesDefault import ChessRulesDefault
from chess_backend.common import Position, PlayerEnum
from PlayerController import PlayerController
from RandomAiController import RandomAiController
from chess_backend.ChessGame import ChessGame
from os import system
from ui.console import draw_board

if __name__ == '__main__':

    rules = ChessRulesDefault()
    game = ChessGame(rules)
    game.start_new()

    white = PlayerController()
    black = RandomAiController()

    idx = 1
    draw_board(game.rules.state)
    while game.state == game.RUNNING:

        legal_moves = game.actions
        if game.rules.state.turn == PlayerEnum.white:
            selected = white.select_action(game.rules.state, legal_moves)
        else:
            selected = black.select_action(game.rules.state, legal_moves)

        action = legal_moves[selected]

        game.move(selected)
        system('cls')
        draw_board(game.rules.state)
        print(f"{idx}. move chosen: {action.move_from} -> {action.move_to}")
        idx += 1

    if game.state == game.WHITE_WON:
        print(f"Game finished, white won")
    elif game.state == game.BLACK_WON:
        print(f"Game finished, black won")
    elif game.state == game.STALEMATE:
        print(f"Game finished, stalemate")
    elif game.state == game.DRAW:
        print(f"Game finished, draw")
