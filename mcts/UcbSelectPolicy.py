import math


class UcbSelectPolicy:
    def __init__(self, c_init, c_base):
        self.c_init = c_init
        self.c_base = c_base

    def select_child(self, node):
        return max(((action, node)
                    for action, node in node.children.items()),
                   key=lambda x: self.evaluate(x[1]))

    def evaluate(self, node):
        exploration_rate = self.c_init
        exploration_rate += math.log((1 + node.parent.visit_count + self.c_base) / self.c_base)
        exploration_rate *= math.sqrt(node.parent.visit_count) / (1 + node.visit_count)

        return node.mean_action_value \
               + exploration_rate * node.prior_probability