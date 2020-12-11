from chess_backend.ChessRulesDefault import ChessRulesDefault
from chess_backend.common import Position, PlayerEnum
from PlayerController import PlayerController
from RandomAiController import RandomAiController
from chess_backend.ChessGame import ChessGame

def main(do_print=True):

    game_idx = 0
    min_moves = 999
    while True:
        rules = ChessRulesDefault()
        game = ChessGame(rules)
        game.start_new()

        white = RandomAiController()
        black = RandomAiController()

        idx = 1
        while game.state == game.RUNNING:

            legal_moves = game.actions
            if game.rules.state.turn == PlayerEnum.white:
                selected = white.select_action(game.rules.state, legal_moves)
            else:
                selected = black.select_action(game.rules.state, legal_moves)

            action = legal_moves[selected]
            game.move(selected)
            if do_print:
                print(f"{idx}. move chosen: {action.move_from} -> {action.move_to}")
                print(game.rules.state)

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

        if idx < min_moves:
            min_moves = idx
            print(f"new minimal game found: {min_moves} moves")
            print(game.rules.state)
            if game.state == game.WHITE_WON:
                print(f"Game finished, white won")
            elif game.state == game.BLACK_WON:
                print(f"Game finished, black won")
            elif game.state == game.STALEMATE:
                print(f"Game finished, stalemate")
            elif game.state == game.DRAW:
                print(f"Game finished, draw")
            print("")

        game_idx += 1

if __name__ == '__main__':
    main(do_print=False)

    #import cProfile
    #cProfile.run('main(do_print=False)', sort="tottime")





