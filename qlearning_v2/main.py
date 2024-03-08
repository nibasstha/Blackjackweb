import copy
import numpy as np
from blackjack import Blackjack
from agent import Agent
from normal_hands_table import NormalHandsTable
from usable_ace_hands_table import UsableAceHandsTable
from same_value_hands_table import SameValueHandsTable

def train(episodes):
  training_ran_for = 0
  game = Blackjack(3)
  agent = Agent()
  normal_hands_table = NormalHandsTable()
  usable_ace_hands_table = UsableAceHandsTable()
  same_value_hands_table = SameValueHandsTable()
  
  hit_c = 0
  stand_c = 0
  double_c = 0
  split_c = 0
  none_c=0
  decayed_at = 0

  for episode in range(episodes):
    training_ran_for = training_ran_for + 1
    print('Training ran for',training_ran_for)
    if episode > 0:
      agent.decay_epsilon()
      if agent.epsilon == 0.01 and decayed_at == 0:
        decayed_at = episode


    game.start_game()
    status = game.check_blackjack()
    final_states = [None,None]

    if status == 'player_blackjack':
      pass
    else:
      while status == 'continue':
        current_player_turn = copy.deepcopy(game.current_turn)
        state = copy.deepcopy(game.get_current_state(current_player_turn))

        action = agent.choose_action(state,normal_hands_table.q,usable_ace_hands_table.q,same_value_hands_table.q)

        if action == 'hit':
          hit_c +=1
        elif action == 'stand':
          stand_c+=1
        elif action == 'double':
          double_c+=1
        elif action == 'split':
          split_c +=1
        else:
          none_c +=1


        state_with_action = copy.deepcopy(game.get_current_state(current_player_turn,action))

        if game.current_turn == 'playerFirstHand':
          final_states[0] = state_with_action
        else:
          final_states[1] = state_with_action

        status = game.player_action(action)
 
        new_state = copy.deepcopy(game.get_current_state(current_player_turn))

   

        # print("--------------")
        # print("state before action",state)
        # print("state with action included",state_with_action)
        # print("state after action",new_state)
        # print("--------------")

        if game.hand_total(new_state['current_hand_player_card']) < 21 and (action != 'double' and action != 'stand'):
          # no small rewards for double because it will lead to terminal state
          # terminal state rewards will happen at the end.
          # reward = agent.get_reward("NO_BUST")


          #only giving future reward.
          reward = 0
          future_max = agent.get_future_max(new_state,normal_hands_table.q,usable_ace_hands_table.q,same_value_hands_table.q)

          action_idx = agent.action_to_action_idx(action)
          new_true_count = new_state['true_count'] # new true count because we are looking in future state.
          play_idx = state['play_idx'] # old play idx -> 0 -> double possible | 1-> no double.

          if state['split_hand_possible'] and "split" in state['valid_actions']:
            same_value_hands_table.update([state["split_hand_player_idx"],state["dealer_idx"],state['true_count'],action_idx],reward,future_max,False)
          elif state['has_usable_ace']:
            usable_ace_hands_table.update([state["usable_ace_player_idx"],state["dealer_idx"],state['true_count'],play_idx,action_idx],reward,future_max,False)
          else:
            normal_hands_table.update([state["normal_hand_player_idx"],state["dealer_idx"],state['true_count'],play_idx,action_idx],reward,future_max,False)
        
        if action == 'stand':
          if(len(game.player_cards[1]) == 0):
            break
          else:
            if(game.current_turn == 'playerFirstHand'):
              game.current_turn = 'playerSecondHand'
              status = 'continue'
            else:
              break
        
      final_result = game.game_result()
      iterable_game_result = game.iterable_game_result()
      final_dealer_cards = game.dealers_cards
        
      for index,state in enumerate(final_states):
          if state is not None:
            # print("Final reward updating::")
            # print("state is",state)
            # print("--------------")

            dealer_idx = state['dealer_idx']

            normal_hand_player_idx = state['normal_hand_player_idx']
            split_hand_player_idx = state['split_hand_player_idx']
            usable_ace_player_idx = state['usable_ace_player_idx']

            play_idx = state['play_idx']

            last_action = state['last_action_taken']
            last_action_idx = agent.action_to_action_idx(last_action)

            usable_ace = state['has_usable_ace']
            split_hand_possible = state['split_hand_possible']

            true_count = state['true_count']

            if iterable_game_result[index] == 'bust':
              if last_action == 'double':
                reward = agent.get_reward('DOUBLE_BUST')
              else:
                reward = agent.get_reward('BUST')
            elif iterable_game_result[index] == 'win':
              if last_action == 'double':
                reward = agent.get_reward('DOUBLE_WIN')
              else:
                reward = agent.get_reward('WIN')
            elif iterable_game_result[index] == 'loss':
              if last_action == 'double':
                reward = agent.get_reward('DOUBLE_LOSS')
              else:
                reward = agent.get_reward('LOSS')
            elif iterable_game_result[index] == 'draw':
              if last_action == 'double':
                reward = agent.get_reward('DOUBLE_DRAW')
              else:
                reward = agent.get_reward('DRAW')
            
            # print("reward got is",reward)
            # print("---------")
            if split_hand_possible or last_action_idx == 3:
              same_value_hands_table.update([split_hand_player_idx,dealer_idx,true_count,last_action_idx],reward,None,True)
            elif usable_ace:
              usable_ace_hands_table.update([usable_ace_player_idx,dealer_idx,true_count,play_idx,last_action_idx],reward,None,True)
            else:
              normal_hands_table.update([normal_hand_player_idx,dealer_idx,true_count,play_idx,last_action_idx],reward,None,True)

  print('Training ran for',training_ran_for)
  print('Final epsilon value',agent.epsilon)
  print('epsilon decayed at',decayed_at)
  print("hit perfomed",hit_c)
  print("stand performed",stand_c)
  print("double performed",double_c)
  print("split performed",split_c)

  np.save('normal_hands_table_v4.npy',normal_hands_table.q)
  np.save('usable_ace_hands_table_v4.npy',usable_ace_hands_table.q)
  np.save('same_value_hands_table_v4.npy',same_value_hands_table.q)

if __name__ == '__main__':
  train(1000000000)
          

          

          









        