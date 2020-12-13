from chess_backend.ChessRulesDefault import ChessRulesDefault
from chess_backend.common import Position, PlayerEnum
from agents.HumanConsoleAgent import HumanConsoleAgent
from agents.RandomAiAgent import RandomAiAgent
from chess_backend.ChessGame import ChessGame
from ui.console import ConsoleUi

if __name__ == '__main__':

    rules = ChessRulesDefault()
    game = ChessGame(rules)
    game.start_new()

    white = HumanConsoleAgent()
    black = RandomAiAgent()
    ui = ConsoleUi()

    idx = 1
    ui.draw_board(game.rules.state)
    while game.state == game.RUNNING:

        legal_moves = rules.legal_moves
        if game.rules.state.turn == PlayerEnum.white:
            selected = white.select_action(game.rules.state, legal_moves)
        else:
            selected = black.select_action(game.rules.state, legal_moves)

        action = legal_moves[selected]

        game.move(selected)
        ui.draw_board(game.rules.state)
        if action.claim_draw:
            print(f"{idx}. move chosen: claim draw")
        else:
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
