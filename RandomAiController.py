import random

class RandomAiController:
    def request_move(self, state, moves):
        return random.randint(0, len(moves) - 1)

