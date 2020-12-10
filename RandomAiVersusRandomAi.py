from ChessRulesDefault import ChessRulesDefault
from common import Position, PlayerEnum
from PlayerController import PlayerController
from RandomAiController import RandomAiController
from ChessGame import ChessGame

if __name__ == '__main__':

    rules = ChessRulesDefault()
    game = ChessGame(rules)
    game.start_new()

    white = RandomAiController()
    black = RandomAiController()

    idx = 1
    while game.state == game.RUNNING:

        print(game.rules.state)

        legal_moves = game.actions

        if game.rules.state.turn == PlayerEnum.white:
            num = white.request_move(game.rules.state, legal_moves)
        else:
            num = black.request_move(game.rules.state, legal_moves)

        move = legal_moves[num]
        print(f"{idx}. move chosen: {move.move_from} -> {move.move_to}")
        idx += 1
        game.move(move.move_from, move.move_to, promote_piece=move.promote_piece)


    if game.state == game.WHITE_WON:
        print(f"Game finished, white won")
    elif game.state == game.BLACK_WON:
        print(f"Game finished, black won")
    elif game.state == game.STALEMATE:
        print(f"Game finished, stalemate")


