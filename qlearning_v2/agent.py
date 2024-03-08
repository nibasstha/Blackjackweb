import numpy as np

class Agent:
  def __init__(self,epsilon=1,decay_rate=0.99999999):
    self.epsilon = epsilon
    self.decay_rate = decay_rate
  
  def choose_action(self,state,normal_table,usable_ace_table,same_value_table):
    valid_actions = state['valid_actions']
    dealer_idx = state['dealer_idx']
    split_hand_player_idx = state['split_hand_player_idx']
    usable_ace_player_idx = state['usable_ace_player_idx']
    normal_hand_player_idx = state['normal_hand_player_idx']
    split_hand_possible = state['split_hand_possible']
    has_usable_ace = state['has_usable_ace']
    true_count = state['true_count']
    play_idx = state['play_idx']

    if np.random.uniform(0,1) < self.epsilon:
      # biasness on random valid split actions
      if 'split' in valid_actions:
        return "split"
      else:
        return np.random.choice(valid_actions)
    else:
      if split_hand_possible and 'split' in valid_actions:
        action_idx = same_value_table[split_hand_player_idx,dealer_idx,true_count].argmax()
      elif has_usable_ace:
        action_idx = usable_ace_table[usable_ace_player_idx,dealer_idx,true_count,play_idx].argmax()
      else:
        action_idx = normal_table[normal_hand_player_idx,dealer_idx,true_count,play_idx].argmax()

      action = self.action_idx_to_action(action_idx)

      if action == 'double' and action not in valid_actions:
        return np.random.choice(['hit','stand'])

      return self.action_idx_to_action(action_idx)
    
  def decay_epsilon(self):
    self.epsilon *= self.decay_rate
    if self.epsilon <= 0:
      self.epsilon = 0

  def action_idx_to_action(self,action_idx):
    action_idx_to_action = {
      0:"stand",
      1:"hit",
      2:"double",
      3:"split"
    }
    return action_idx_to_action[action_idx]

  def action_to_action_idx(self,action):
    action_to_action_idx = {
      "stand":0,
      "hit":1,
      "double":2,
      "split":3
    }
    return action_to_action_idx[action]

  def get_reward(self,reward_for):
    reward_map = {
      "WIN":1,
      "DOUBLE_WIN":1.5,
      "LOSS":-1,
      "DOUBLE_LOSS":-1.5,
      "DOUBLE_DRAW":0.5,
      "DRAW":0.25,
      "BUST":-1.1,
      "DOUBLE_BUST":-2.1,
      "NO_BUST":0.001
    }
    return reward_map[reward_for]

  def get_future_max(self,state,normal_table,usable_ace_table,same_value_table):
    dealer_idx = state['dealer_idx']
    usable_ace_player_idx = state['usable_ace_player_idx']
    has_usable_ace = state['has_usable_ace']
    normal_hand_player_idx = state['normal_hand_player_idx']
    true_count = state['true_count']
    play_idx = state['play_idx']

    # print("normalhandplayer",normal_hand_player_idx)
    # print("dealer-idx",dealer_idx)
    # print("play idx",play_idx)
    # print("true coutn",true_count)
    # same pairs won't exist for future actions.
    # even if it does, let's not refer to the same_value_table. split action is possible there.
    # which is not possible inside another spliited hands.
    if has_usable_ace:
      future_reward = usable_ace_table[usable_ace_player_idx,dealer_idx,true_count,play_idx].max()
    else:
      future_reward = normal_table[normal_hand_player_idx,dealer_idx,true_count,play_idx].max()
    
    return future_reward


  



