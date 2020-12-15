from mcts.MctsNode import MctsNode
from mcts.UcbSelectPolicy import UcbSelectPolicy
import random
import numpy as np


class DefaultConfig:

    def __init__(self):
        self.leaf_iterations = 800 # 800

        # UCB formula
        self.c_init = 1.25
        self.c_base = 19652

        # Root prior exploration noise.
        self.root_dirichlet_alpha = 0.3  # for chess, 0.03 for Go and 0.15 for shogi.
        self.root_exploration_fraction = 0.25

def __expand_node(node, policy_value_network):
    if node.game_state.legal_moves:
        policy, value = policy_value_network(node.game_state)
        node.value = value
        for action_idx, action in enumerate(node.game_state.legal_moves):
            child_node = MctsNode(parent=node, prior_probability=policy[action_idx])
            node.children[action] = child_node
    else:  # no more moves, terminal state -> propagate actual value
        value = node.game_state.get_winner_score()
        value *= node.was_our_turn  # we are winners only if this is not our turn

    return value


def mcts_search(game_state, policy_value_network, config=DefaultConfig()):
    root = MctsNode(game_state=game_state)
    select_policy = UcbSelectPolicy(config.c_init, config.c_base)
    __expand_node(root, policy_value_network)

    # add exploration noise
    actions = root.children.keys()
    noise = np.random.gamma(config.root_dirichlet_alpha, 1, len(actions))
    frac = config.root_exploration_fraction
    for a, n in zip(actions, noise):
        root.children[a].prior_probability *= (1 - frac)
        root.children[a].prior_probability += n * frac

    # make the iterations a multiple of number of possible moves,
    # so that exploration can be evened out (no bias towards first elements)
    iterations = config.leaf_iterations
    iterations -= iterations % len(game_state.legal_moves)

    for _ in range(iterations):
        node = root
        while node.is_expanded():
            action, child_node = select_policy.select_child(node)
            node = child_node
            if node.game_state is None:
                node.game_state = node.parent.game_state.clone()
                node.game_state.apply(action)

        # reached the leaf node, expand
        value = __expand_node(node, policy_value_network)

        # propagate value back to the root
        while node:
            node.record_visit(value)
            node = node.parent

    # select action with the most visit counts
    population = []
    weights = []
    for action, node in root.children.items():
        population.append(action)
        weights.append(node.visit_count)

    # softmax - subtracting exponents to make numerically stable
    weights = np.exp(weights - np.max(weights))
    weights /= weights.sum(axis=0)

    selected_action, = random.choices(population, weights)
    return selected_action, root
