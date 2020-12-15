from mcts.MctsNode import MctsNode
from mcts.UcbSelectPolicy import UcbSelectPolicy
import random
import numpy as np


class DefaultConfig:

    def __init__(self):
        self.leaf_iterations = 800 # 800
        self.c_init = 1.25
        self.c_base = 19652


def mcts_search(game_state, policy_value_network, config=DefaultConfig()):
    root = MctsNode(game_state=game_state)
    select_policy = UcbSelectPolicy(config.c_init, config.c_base)

    iterations = config.leaf_iterations
    # make the iterations a multiple of number of possible moves,
    # so that exploration can be evened out (no bias towards first elements)
    iterations -= iterations % len(game_state.legal_moves)

    for _ in range(iterations + 1):
        node = root
        while node.is_expanded():
            action, child_node = select_policy.select_child(node)
            node = child_node
            if node.game_state is None:
                node.game_state = node.parent.game_state.clone()
                node.game_state.apply(action)

        # reached the leaf node, expand
        if node.game_state.legal_moves:
            policy, value = policy_value_network(node.game_state)
            for action_idx, action in enumerate(node.game_state.legal_moves):
                node.children[action] = MctsNode(parent=node, prior_probability=policy[action_idx])
        else: # no more moves, terminal state -> propagate actual value
            value = node.game_state.get_winner_score()
            value *= node.was_our_turn # we are winners only if this is not our turn

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

    i = 0
    for idx in range(len(population)):
        move = population[idx]
        promote_hint = move.promote_piece.name if move.promote_piece is not None else ''
        if move.claim_draw:
            print(
                f"claim draw \t\t",
                end='')
        else:
            print(
                f"{move.move_from} -> {move.move_to} {promote_hint}: {weights[idx]:.3f}\t\t",
                end='')
        i += 1
        if i % 3 == 0:
            print("")
    print("")


    selected_action, = random.choices(population, weights)
    return selected_action
