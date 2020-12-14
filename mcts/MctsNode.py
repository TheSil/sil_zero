
class MctsNode:

    def __init__(self, game_state=None, parent=None, prior_probability=0 ):
        self.parent = parent
        self.children = {}
        self.player_turn = 1 if parent is None else -parent.player_turn
        self.game_state = game_state

        self.visit_count = 0  # N(s,a)
        self.total_action_value = 0  # W(s,a)
        self.mean_action_value = 0  # Q(s,a)
        self.prior_probability = prior_probability  # P(s,a)

    def is_expanded(self):
        return self.children

    def record_visit(self, value):
        self.visit_count += 1
        self.total_action_value += value * self.player_turn
        self.mean_action_value = self.total_action_value / self.visit_count
