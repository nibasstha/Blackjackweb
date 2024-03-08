from state import State
from node import MCTSNode
import random

def monte_carlo_tree_search(initial_state, num_iterations):
  root_state = State(initial_state, None)
  root_node = MCTSNode(root_state,None)

  for i in range(num_iterations):
    node = root_node

    # Selection
    while not node.is_terminal() and node.fully_expanded():
      node = node.best_child()

    # Expansion
    if not node.is_terminal():
      node.expand()
      node = random.choice(node.children)

    # Simulation
    result = node.simulate()

    # Backpropagation
    while node is not None:
      node.update(result)
      node = node.parent

  if root_node.children:
    return root_node.best_child().state.action_taken
  else:
    return root_node.state.action_taken
  

if __name__ == '__main__':
  initial_state = {
    "player_cards":[["2-S","5-H"],[]],
    "dealer_cards":["A-S"],
    "garbage_deck":["5-S","3-S"],
    "current_turn":"playerFirstHand"
  }
  final_state = monte_carlo_tree_search(initial_state,num_iterations=1000)
  print(final_state)