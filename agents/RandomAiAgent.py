import random


class RandomAiAgent:
    def __init__(self, prefer_takes=False):
        self.prefer_takes = prefer_takes

    def select_action(self, state, actions):
        if not self.prefer_takes:
            return random.randint(0, len(actions) - 1)

        preferred_idx = []
        for idx, action in enumerate(actions):
            if action.to_take is not None:
                preferred_idx.append(idx)

        if preferred_idx:
            return preferred_idx[random.randint(0, len(preferred_idx) - 1)]

        return random.randint(0, len(actions) - 1)
