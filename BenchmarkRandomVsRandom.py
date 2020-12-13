from chess_backend.ChessRulesDefault import ChessRulesDefault
from chess_backend.common import PlayerEnum
from agents.RandomAiAgent import RandomAiAgent
from chess_backend.ChessGame import ChessGame


def main(do_print=True):
    white = RandomAiAgent(prefer_takes=True)
    black = RandomAiAgent(prefer_takes=True)

    game_number = 1
    white_wins = 0
    black_wins = 0
    draws = 0
    all = 0
    while True:

        rules = ChessRulesDefault()
        game = ChessGame(rules)
        game.start_new()

        idx = 1
        while game.state == game.RUNNING:

            legal_moves = game.actions
            if game.rules.state.turn == PlayerEnum.white:
                selected = white.select_action(game.rules.state, legal_moves)
            else:
                selected = black.select_action(game.rules.state, legal_moves)

            action = legal_moves[selected]
            game.move(selected)
            idx += 1

        if game.state == game.WHITE_WON:
            white_wins += 1
        elif game.state == game.BLACK_WON:
            black_wins += 1
        elif game.state == game.STALEMATE:
            draws += 1
        elif game.state == game.DRAW:
            draws += 1
        all += 1

        print(f"{game_number:4d}: "
              f"white_wins:{(100*white_wins)/all:3.2f}%\t"
              f"black_wins:{(100*black_wins)/all:3.2f}%\t"
              f"draws:{(100*draws)/all:3.2f}%")
        game_number += 1


if __name__ == '__main__':
    main()

    # import cProfile
    # cProfile.run('main(do_print=False)', sort="tottime")
