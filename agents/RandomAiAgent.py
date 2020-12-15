import random


class RandomAiAgent:
    def __init__(self, prefer_takes=False):
        self.prefer_takes = prefer_takes

    def select_action(self, game_state):
        if not self.prefer_takes:
            return random.choice(game_state.legal_moves), None

        preferred_idx = []
        for idx, action in enumerate(game_state.legal_moves):
            if action.to_take is not None:
                preferred_idx.append(idx)

        if preferred_idx:
            return game_state.legal_moves[random.choice(preferred_idx)], None

        return random.choice(game_state.legal_moves), None
