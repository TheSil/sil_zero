
class PlayerController:
    def request_move(self, state, moves):
        i = 0
        for move in moves:
            print(f"{i}: {move.move_from} -> {move.move_to} {move.promote_piece.name if move.promote_piece is not None else ''}\t\t", end='')
            i += 1
            if i % 3 == 0:
                print("")
        print("")
        num = int(input("Choice: "))
        return num
