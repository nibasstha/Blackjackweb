import random
import math
import numpy as np

class MCTSNode:
  def __init__(self,state,parent=None):
    self.state = state
    self.parent = parent
    self.children = []
    self.visits = 0
    self.wins = 0
  
  def fully_expanded(self):
    # current_turn = self.state.gameState["current_turn"]
    # last_action = self.state.action_taken
    # player_first_hand = self.state.gameState["player_cards"][0]
    # player_second_hand = self.state.gameState["player_cards"][1]
    # is_fully_expanded = False

    # if current_turn == 'playerFirstHand' and len(player_second_hand) == 0:
    #   if last_action == 'stand' or last_action == 'double' or self.state.engine.hand_total(player_first_hand) >=21:
    #     is_fully_expanded = True
    # else:
    #   if (last_action == 'stand' or last_action == 'double' or self.state.engine.hand_total(player_second_hand) >=21) and current_turn == 'playerSecondHand':
    #     is_fully_expanded = True
    valid_actions = self.state.engine.get_valid_actions()
    actions_len_count = 0
    for action in valid_actions:
      if action == 'hit' or action == 'double':
        actions_len_count = actions_len_count + 10
      else:
        actions_len_count = actions_len_count + 1


    return len(self.children) == actions_len_count
  
  def is_terminal(self):
    print("insid node",self.state)
    return self.state.is_game_over()

  def best_child(self):
    print("self.children",self.children)
    if not self.children:
      return None
    unvisited = [c for c in self.children if c.visits == 0]
    if unvisited:
      return random.choice(unvisited)
    return max(self.children, key=lambda x: x.wins / x.visits)

  def expand(self):
    # how to expand a node?
    # look at the gameState
    # iterate over the valid actions
    # maintain an object of deck variation possible and deal that card
    # remove that card from the object of deck 
    # and create a child node again and again.
    valid_actions = self.state.engine.get_valid_actions()
    print("valid actions are",valid_actions)
    for action in valid_actions:
      if action == 'hit' or action == 'double':
        garbage_deck = ["1-S","2-S","3-S","4-S","5-S","6-S","7-S","8-S","9-S","10-S"]
        for card in garbage_deck:
          garbage_deck_clone = garbage_deck[:]
          garbage_deck_clone.remove(card)
          new_state = self.state.apply_moves_involving_card_addition(card,garbage_deck_clone,action)
          new_node = MCTSNode(new_state,self)
          self.children.append(new_node)
      else:
        new_state = self.state.apply_move(action)
        new_node = MCTSNode(new_state,self)
        self.children.append(new_node)

  def simulate(self):
    engine = self.state.engine
    status = engine.check_blackjack()
    while status == "continue" or status == 'bustcontinue':
      validActions = engine.get_valid_actions()
      action = np.random.choice(validActions)
      status = engine.player_action(action)
      if action == 'stand':
        if(len(engine.player_cards[1]) < 1):
          break
        else:
          if(engine.current_turn == 'playerFirstHand'):
            engine.current_turn = 'playerSecondHand'
            status = 'continue'
          else:
            break
    engine.game_result()
    print("Inside simulate")
    return self.state.get_winner()
    

  def update(self,result):
    self.visits += 1
    if result is not None:
      self.wins += int(result)

  def uct_score(self,exploration_constant=1.414):
    if self.visits == 0:
      return float('inf')
    return self.wins / self.visits + exploration_constant * math.sqrt(math.log(self.parent.visits) / self.visits)
