import sys
sys.path.insert(1,'/Users/manjeet/Documents/workspaces/college/blackjack/qlearning_v2')
from blackjack import Blackjack


# gameState = {
#   player_cards:None,
#   dealer_cards:None,
#   garbage_deck:None,
#   current_turn:None
# }

class State:
  def __init__(self,gameState,action_taken):
    self.gameState = gameState
    self.action_taken = action_taken # make sure to reset action_taken after forfeiting your turn in split mode. i.e when the turn changes to playerSecondHand, the last action taken should be None
    self.engine = Blackjack(3,190,gameState['dealer_cards'],gameState['player_cards'],gameState['current_turn'])
  
  def is_game_over(self):
    # while condition of dealer hands.
    dealer_hand_total = self.engine.hand_total(self.gameState['dealer_cards'])
    player_first_hand_total = self.engine.hand_total(self.gameState["player_cards"][0])
    player_second_hand_total = self.engine.hand_total(self.gameState["player_cards"][1])

    dealer_first_hand_play =  dealer_hand_total <= player_first_hand_total
    dealer_second_hand_play = len(self.gameState["player_cards"][1]) > 0 and dealer_hand_total <= player_second_hand_total

    return dealer_hand_total < 17 and player_first_hand_total <=21 and (dealer_first_hand_play or dealer_second_hand_play)


  def get_legal_moves(self):
    return self.engine.get_valid_actions()
  
  def apply_moves_involving_card_addition(self,card,deck,move):
    new_current_turn = self.gameState['current_turn']
    if self.gameState['current_turn'] == 'playerFirstHand':
      new_player_cards = [self.gameState["player_cards"][0]+[card],self.gameState["player_cards"][1]]
      if move == 'double' and len(self.gameState["player_cards"][1]) > 0:
        new_current_turn = 'playerSecondHand'
    else:
      new_player_cards = [self.gameState["player_cards"][0],self.gameState["player_cards"][1]+[card]]

    new_game_state = {
      "player_cards":new_player_cards,
      "dealer_cards":self.gameState["dealer_cards"],
      "current_turn":new_current_turn,
      "deck":deck
    }

    return State(new_game_state,move)


  def apply_move(self,move):
    self.engine.player_action(move)
    if (self.engine.current_turn == 'playerFirstHand' and move == 'stand' and len(self.engine.player_cards[1]) > 1):
      current_turn = 'playerSecondHand'
    elif (move == 'stand'):
      current_turn = 'dealer'
    
    new_game_state = {
      "player_cards":self.engine.player_cards,
      "dealer_cards":self.engine.dealers_cards,
      "current_turn":current_turn,
      "deck":self.engine.deck
    }
    return State(new_game_state,move)


  def get_winner(self):
    game_result = self.engine.iterable_game_result()
    result_idx = 0 # 1 = win , 0 = non win.

    if game_result[1] == 'win' or game_result[0] == 'win':
      result_idx = 1
    else:
      result_idx = 0
    
    return result_idx


    
   