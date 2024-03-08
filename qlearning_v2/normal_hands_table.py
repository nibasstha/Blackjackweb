import numpy as np

class NormalHandsTable:
  def __init__(self,alpha=0.1,gamma=0.9):
    self.alpha = alpha
    self.gamma = gamma
    # player_sum,dealer_sum,true_count,play_idx,action_idx
    self.q = np.zeros((21,11,3,2,3))
  
  def update(self,table_idx,reward,future_max,is_terminal):
    player_idx = table_idx[0]
    dealer_idx = table_idx[1]
    true_count_idx = table_idx[2]
    play_idx = table_idx[3]
    action_idx = table_idx[4]
    # print("Normal hands updated")
    # print('index received:')
    # print('player_idx',player_idx)
    # print('dealer_idx',dealer_idx)
    # print('true_count_idx',true_count_idx)
    # print('action_idx',action_idx)
    # print('reward is',reward)
    # print("play_idx",play_idx)
    # print('future_max',future_max)
    old_value = self.q[player_idx,dealer_idx,true_count_idx,play_idx,action_idx]
    if is_terminal:
      self.q[player_idx,dealer_idx,true_count_idx,play_idx,action_idx] = old_value + self.alpha * (reward - old_value)
    else:
      self.q[player_idx,dealer_idx,true_count_idx,play_idx,action_idx] = old_value + self.alpha * (reward + self.gamma * future_max - old_value)