
class PlayerController:
    def request_move(self, state, moves):
        i = 0
        for move in moves:
            print(f"{i}: {move.move_from} -> {move.move_to}\t\t", end='')
            i += 1
            if i % 3 == 0:
                print("")
        print("")
        num = int(input("Choice: "))
        return num
