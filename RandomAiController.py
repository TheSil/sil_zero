import random

class RandomAiController:
    def select_action(self, state, actions):
        return random.randint(0, len(actions) - 1)

