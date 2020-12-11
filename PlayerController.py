class PlayerController:
    def select_action(self, state, actions):
        while True:
            i = 0
            try:
                for move in actions:
                    promote_hint = move.promote_piece.name if move.promote_piece is not None else ''
                    print(
                        f"{i}: {move.move_from} -> {move.move_to} {promote_hint}\t\t",
                        end='')
                    i += 1
                    if i % 3 == 0:
                        print("")
                print("")
                num = int(input("Choice: "))
                if not (0 <= num < len(actions)):
                    raise IndexError
                return num
            except ValueError:
                print("Input in incorrect form")
            except IndexError:
                print("Input out of bounds")
