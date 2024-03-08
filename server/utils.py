import sys
sys.path.insert(1,'/Users/manjeet/Documents/workspaces/college/blackjack/qlearning_v2')
from blackjack import Blackjack

import numpy as np

def action_policy_table_lookup(state):
  print("state is",state)
  normal_hands_file_path = r'/Users/manjeet/Documents/workspaces/college/blackjack/qlearning_v2/normal_hands_table_v4.npy'
  normal_hands_table = np.load(normal_hands_file_path,allow_pickle=True)

  print("table",normal_hands_table)

  usable_ace_hands_file_path = r'/Users/manjeet/Documents/workspaces/college/blackjack/qlearning_v2/usable_ace_hands_table_v4.npy'
  usable_ace_table = np.load(usable_ace_hands_file_path,allow_pickle=True)

  same_value_hands_file_path = r'/Users/manjeet/Documents/workspaces/college/blackjack/qlearning_v2/same_value_hands_table_v4.npy'
  same_value_hands_table = np.load(same_value_hands_file_path,allow_pickle=True)

  deck_count = 3
  seed = 190
  dealer_cards = [state['dealersCards'][0]]
  player_cards = state['playerCards']

  print('player_cards from state',player_cards)
  if state['currentTurn'] == 1:
    current_turn = 'playerFirstHand'
  else:
    current_turn = 'playerSecondHand'
  
  running_count = calc_running_count(state['garbageDeck'])
    
  last_action_taken = None
  count_adjust = 0
  
  engine = Blackjack(deck_count,seed,dealer_cards,player_cards,current_turn,running_count,last_action_taken,count_adjust)

  engine_state = engine.get_current_state()

  valid_actions = engine_state['valid_actions']
  dealer_idx = engine_state['dealer_idx']
  split_hand_player_idx = engine_state['split_hand_player_idx']
  usable_ace_player_idx = engine_state['usable_ace_player_idx']
  normal_hand_player_idx = engine_state['normal_hand_player_idx']
  split_hand_possible = engine_state['split_hand_possible']
  has_usable_ace = engine_state['has_usable_ace']
  true_count = engine_state['true_count']
  play_idx = engine_state['play_idx']

  if split_hand_possible and 'split' in valid_actions:
    action_idx = same_value_hands_table[split_hand_player_idx,dealer_idx,true_count].argmax()
  elif has_usable_ace:
    action_idx = usable_ace_table[usable_ace_player_idx,dealer_idx,true_count,play_idx].argmax()
  else:
    print("nor",normal_hand_player_idx,dealer_idx,true_count,play_idx)
    action_idx = normal_hands_table[normal_hand_player_idx,dealer_idx,true_count,play_idx].argmax()

  action_idx_to_action = {
    0:"stand",
    1:"hit",
    2:"double",
    3:"split"
  }

  action = action_idx_to_action[action_idx]

  if action == 'double' and action not in valid_actions:
        return np.random.choice(['hit','stand'])

  return action

def calc_running_count(garbageDeck):
  running_count = 0
  for card in garbageDeck:
    face_value = card.split("-")[0]
    if face_value in ["10","J","Q","K","A"]:
      running_count = running_count - 1
    if face_value in ["2","3","4","5","6"]:
      running_count = running_count + 1
  return running_count


def mctsHint(state):
  deck_count = 3
  seed = 190
  dealer_cards = [state['dealersCards'][0]]
  player_cards = state['playerCards']
  running_count = calc_running_count(state['garbageDeck'])    
  last_action_taken = None
  count_adjust = 0
  if state['currentTurn'] == 1:
    current_turn = 'playerFirstHand'
    engine = Blackjack(deck_count,seed,dealer_cards,player_cards,current_turn,running_count,last_action_taken,count_adjust)
    engine_state = engine.get_current_state()
    hand_total = engine.hand_total(player_cards[0])
    valid_actions = engine_state['valid_actions']
    if 'split' in valid_actions:
      return 'split'
    elif hand_total<17:
      if hand_total < 13:
        return 'hit'
      elif hand_total >13 and hand_total<=17 and 'double' in valid_actions:
        return 'double'
      else:
        return 'stand'
    else:
      return 'stand'
  else:
    current_turn = 'playerSecondHand'
    engine = Blackjack(deck_count,seed,dealer_cards,player_cards,current_turn,running_count,last_action_taken,count_adjust)
    engine_state = engine.get_current_state()
    hand_total = engine.hand_total(player_cards[1])
    valid_actions = engine_state['valid_actions']
    if 'split' in valid_actions:
      return 'split'
    elif hand_total<17:
      if hand_total < 13:
        return 'hit'
      elif hand_total >13 and hand_total<=17 and 'double' in valid_actions:
        return 'double'
      else:
        return 'stand'
    else:
      return 'stand'

