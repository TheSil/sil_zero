class HumanConsoleAgent:
    def select_action(self, game_state):
        while True:
            i = 0
            try:
                for move in game_state.legal_moves:
                    promote_hint = move.promote_piece.name if move.promote_piece is not None else ''
                    if move.claim_draw:
                        print(
                            f"{i}: claim draw \t\t",
                            end='')
                    else:
                        print(
                            f"{i}: {move.move_from} -> {move.move_to} {promote_hint}\t\t",
                            end='')

                    i += 1
                    if i % 3 == 0:
                        print("")
                print("")
                num = int(input("Choice: "))
                if not (0 <= num < len(game_state.legal_moves)):
                    raise IndexError
                return game_state.legal_moves[num], None
            except ValueError:
                print("Input in incorrect form")
            except IndexError:
                print("Input out of bounds")
