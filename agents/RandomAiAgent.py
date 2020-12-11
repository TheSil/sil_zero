import random


class RandomAiAgent:
    def select_action(self, state, actions):
        return random.randint(0, len(actions) - 1)
