from mcts.mcts_search import mcts_search


class AiAgent:
    def __init__(self, net):
        self.net = net

    def select_action(self, game_state):
        selected, root = mcts_search(game_state, self.net)
        sum_visits =sum(child.visit_count for child in root.children.values())
        visit_stats = {}
        for action, child in root.children.items():
            visit_stats[action] = child.visit_count / sum_visits
        self.last_root = root
        return selected, visit_stats
