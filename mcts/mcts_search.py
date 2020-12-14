from mcts.MctsNode import MctsNode
from mcts.UcbSelectPolicy import UcbSelectPolicy


class DefaultConfig:

    def __init__(self):
        self.leaf_iterations = 800
        self.c_init = 1.25
        self.c_base = 19652


def mcts_search(game_state, policy_value_network, config=DefaultConfig()):
    root = MctsNode()
    select_policy = UcbSelectPolicy(config.c_init, config.c_base)

    for _ in range(config.leaf_iterations + 1):
        node = root
        sim_game_state = game_state.clone()
        while node.is_expanded():
            action, child_node = select_policy.select_child(node)
            sim_game_state.apply(action)
            node = child_node

        # reached the leaf node, expand
        policy, value = policy_value_network(sim_game_state)
        for action_idx, action in enumerate(sim_game_state.legal_moves):
            node.children[action] = MctsNode(node, policy[action_idx])

        # propagate value back to the root
        while node:
            node.record_visit(value)
            node = node.parent

    # select action with the most visit counts
    selected = max(((action, node)
                    for action, node in root.children.items()),
                   key=lambda x: x[1].visit_count)
    return selected[0]
