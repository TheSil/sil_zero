
class PlayerController:
    def select_action(self, state, actions):
        while True:
            i = 0
            try:
                for move in actions:
                    print(f"{i}: {move.move_from} -> {move.move_to} {move.promote_piece.name if move.promote_piece is not None else ''}\t\t", end='')
                    i += 1
                    if i % 3 == 0:
                        print("")
                print("")
                num = int(input("Choice: "))
                return num
            except KeyboardInterrupt:
                raise
            except Exception:
                pass
