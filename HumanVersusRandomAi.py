from chess_backend.GameState import GameState
from chess_backend.common import PlayerEnum
from chess_backend.Session import Session
from agents.HumanConsoleAgent import HumanConsoleAgent
from agents.RandomAiAgent import RandomAiAgent
from ui.console import ConsoleUi

if __name__ == '__main__':

    game = GameState()
    game.start_new()

    white = HumanConsoleAgent()
    black = RandomAiAgent()
    ui = ConsoleUi()

    session = Session(game, white, black)
    session.before_move(lambda : ui.draw_board(game.board))

    def report_move():
        last_move = session.history[-1][1]
        if last_move.claim_draw:
            print(f"move chosen: claim draw")
        else:
            print(f"move chosen: {last_move.move_from} -> {last_move.move_to}")
    session.after_move(report_move)

    session.play()

    if game.state == game.WHITE_WON:
        print(f"Game finished, white won")
    elif game.state == game.BLACK_WON:
        print(f"Game finished, black won")
    elif game.state == game.STALEMATE:
        print(f"Game finished, stalemate")
    elif game.state == game.DRAW:
        print(f"Game finished, draw")
