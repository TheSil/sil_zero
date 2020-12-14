from mcts.mcts_search import mcts_search


class AiAgent:
    def __init__(self, net):
        self.net = net

    def select_action(self, game_state):
        return mcts_search(game_state, self.net)
