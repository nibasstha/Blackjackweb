import random
import math

class Blackjack:
  def __init__(self,deck_count,seed=190,dealers_cards=[],player_cards=[[],[]],current_turn="playerFirstHand",running_count=0,last_action_taken=None,count_adjust=0):
    self.seed = seed
    self.deck = self.generate_deck(self,deck_count)
    self.deck_count = deck_count
    self.dealers_cards = dealers_cards
    self.player_cards = player_cards
    self.current_turn = current_turn
    self.running_count = running_count
    self.last_action_taken = last_action_taken
    self.count_adjust = count_adjust

  @staticmethod
  def generate_deck(self,deck_count):
    numbers=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
    suits=['H','D','C','S']
    deck = [number+"-"+suit for count in range(deck_count) for suit in suits for number in numbers]
    random.Random(self.seed).shuffle(deck)
    self.seed = self.seed + 1
    return deck

  def deal_card(self,idx,update_runnning_count=True):
    if len(self.deck) > idx:
      card_to_deal = self.deck.pop(idx)
      if update_runnning_count:
        self.update_running_count(card_to_deal)
      return card_to_deal
    else:
      self.deck = self.generate_deck(self,self.deck_count)
      card_to_deal = self.deck.pop(idx)
      if update_runnning_count:
        self.update_running_count(card_to_deal)
      return card_to_deal

  def start_game(self):
    self.count_adjust = -1
    self.player_cards = [[self.deal_card(0),self.deal_card(2)],[]]
    self.dealers_cards = [self.deal_card(1),self.deal_card(3,False)]
    self.current_turn = 'playerFirstHand'
    self.last_action_taken = None

  def check_blackjack(self):
    print("player cars is",self.player_cards)
    if (self.hand_total(self.player_cards[0]) == 21 ):
      return "player_blackjack"
    else:
      return "continue"
    
  @staticmethod
  def hand_total(cards):
    value = 0
    aces = 0
    for card in cards:
      cardValue = card.split("-")[0]
      if cardValue in ['J','Q','K']:
        value +=10
      elif cardValue == "A":
        if value + 11 > 21:
          value = value + 1
        else:
          aces +=1
          value = value + 11
      else:
        value = value + int(cardValue)

    while value > 21 and aces:
      value -=10
      aces -=1

    return value
    
  def check_split_possible(self,cards):
    if len(cards) < 1:
      return False
    elif len(cards) == 2:
      first_card = cards[0].split("-")[0]
      second_card = cards[1].split("-")[0]
      if first_card == second_card:
        return True
      elif first_card in ["10","J","Q","K"] and second_card in ["10","J","Q","K"]:
        return True
      else:
        return False
    else:
      return False

  def player_action(self,action):
    if action == 'stand':
      self.last_action_taken = 'stand'

    if action == 'hit':
      self.last_action_taken = 'hit'
      if(self.current_turn == "playerFirstHand"):
        self.player_cards[0].append(self.deal_card(0))
        return self.game_status(action)
      if(self.current_turn == "playerSecondHand"):
        self.player_cards[1].append(self.deal_card(0))
        return self.game_status(action)
      
    if action == 'split':
      self.last_action_taken = 'split'
      firstHand = self.player_cards[0][0]
      secondHand = self.player_cards[0][1]
      self.player_cards = [[firstHand],[secondHand]]
      self.current_turn = "playerFirstHand"
      return self.game_status(action)  
    
    if action == 'double':
      self.last_action_taken = 'double'
      if(self.current_turn == 'playerFirstHand'):
        self.player_cards[0].append(self.deal_card(0))
        return self.game_status(action) 
      if(self.current_turn == 'playerSecondHand'):
        self.player_cards[1].append(self.deal_card(0))
        return self.game_status(action)

  def get_valid_actions(self):
    print('playercards',self.player_cards)
    validActions = ["stand","hit"]
    firstCardValue = self.player_cards[0][0].split("-")[0]

    if(firstCardValue in ["J","Q","K"]):
      firstCardValue = 10

    if(len(self.player_cards[0]) > 1):
      secondCardValue = self.player_cards[0][1].split("-")[0]
      if(secondCardValue in ["J","Q","K"]):
        secondCardValue = 10
    else:
         secondCardValue = 0

    if len(self.player_cards[1])>0:
      if self.current_turn == 'playerFirstHand' and len(self.player_cards[0]) == 1:
        validActions.append("double")
      if self.current_turn == 'playerSecondHand' and len(self.player_cards[1]) == 1:
        validActions.append("double")
    else:
      if self.current_turn == 'playerFirstHand' and len(self.player_cards[0]) == 2:
        validActions.append("double")
      
    if((self.current_turn == "playerFirstHand") and len(self.player_cards[0]) == 2 and firstCardValue == secondCardValue and len(self.player_cards[1]) == 0):
      validActions.append("split")
      
    return validActions

  def dealer_action(self):
    while self.hand_total(self.dealers_cards) < 17 \
              and self.hand_total(self.player_cards[0]) <=21 \
              and (self.hand_total(self.dealers_cards)<=self.hand_total(self.player_cards[0]) \
              or (len(self.player_cards[1])>0 and self.hand_total(self.dealers_cards) <= self.hand_total(self.player_cards[1]))):
              self.dealers_cards.append(self.deal_card(0))

  def has_usable_ace(self,cards):
    value = 0
    aces = 0

    for card in cards:
      card_value = card.split("-")[0]
      if card_value in ["J","Q","K"]:
        value +=10
      elif card_value == "A":
        aces = aces + 1
        value = value + 1
      else: 
        value = value +int(card_value)
    
    if(aces == 0):
      return False
    else:
      if value + 10 <=21 :
        return True
      else:
        return False

  def game_status(self,action):
    if(action=="double" and self.hand_total(self.player_cards[1]) >= 1 and self.current_turn == "playerFirstHand"):
      self.current_turn = "playerSecondHand"
      return "continue"
    if(action=="double" and self.hand_total(self.player_cards[1])<1):
      return "continueDealer"
    if(action == "double" and self.current_turn == "playerSecondHand"):
      return "continueDealer"

    playerFirstHand = self.player_cards[0]
    playerSecondHand = self.player_cards[1]


    if(len(playerSecondHand) < 1):
      if self.hand_total(playerFirstHand) > 21:
        return "bust"
      elif self.hand_total(playerFirstHand) == 21:
        return "end"
      else:
        return "continue"
    else:
      if self.current_turn == 'playerFirstHand':
        if self.hand_total(playerFirstHand) > 21:
          self.current_turn = 'playerSecondHand'
          return "continue"
        elif self.hand_total(playerFirstHand) == 21:
          self.current_turn = 'playerSecondHand'
          return "continue"
        else:
          return "continue"
      else:
        if self.hand_total(playerSecondHand) > 21:
          return "continueDealer"
        elif self.hand_total(playerSecondHand) == 21:
          return "continueDealer"
        else:
          return "continue"
  
  def update_running_count(self,card):
    face_value = card.split("-")[0]
    if face_value in ["10","J","Q","K","A"]:
      self.running_count = self.running_count - 1
    if face_value in ["2","3","4","5","6"]:
      self.running_count = self.running_count + 1

  def get_true_count(self):
    #0=0 , 1= +ve , 2= -ve
    deck_remaining = math.ceil(len(self.deck) + self.count_adjust /53)
    true_count = None
    if deck_remaining == 0 or deck_remaining == 1:
      true_count = self.running_count
    else:
      true_count = self.running_count/deck_remaining

    if true_count == 0 :
      return 0
    elif true_count > 0 :
      return 1
    else:
      return 2

  def game_result(self):
    # print("Dealer_cards is",self.dealers_cards[1])
    self.count_adjust = 0
    if(len(self.dealers_cards)) > 1:
      self.update_running_count(self.dealers_cards[1])
    self.dealer_action()
    dealerTotal = self.hand_total(self.dealers_cards)
    playerFirsthand_total = self.hand_total(self.player_cards[0])
    playerSecondhand_total = self.hand_total(self.player_cards[1])
    print("D F S",dealerTotal,playerFirsthand_total,playerSecondhand_total)
    if(playerFirsthand_total <=21):
      # Blackjack win condition for single hand only. Doesn't apply to split conditions
      if(playerFirsthand_total == 21 and playerSecondhand_total < 1 and dealerTotal < 21):
        firstHandResult = "PlayerFirstHand win"
      elif(dealerTotal>21):
        firstHandResult = "PlayerFirstHand win"
      elif(playerFirsthand_total > dealerTotal):
        firstHandResult = "PlayerFirstHand win"
      elif(playerFirsthand_total == dealerTotal):
        firstHandResult = "PlayerFirstHand draw"
      else:
        firstHandResult = "PlayerFirstHand loss"
    else:
      firstHandResult = "PlayerFirstHand loss"
        
    if(playerSecondhand_total >= 1):
      if(playerSecondhand_total > 21):
        secondHandResult = "PlayerSecondHand loss"
      elif(dealerTotal >21):
        secondHandResult = "PlayerSecondHand win"
      elif(dealerTotal > playerSecondhand_total):
        secondHandResult = "PlayerSecondHand loss"
      elif(dealerTotal < playerSecondhand_total):
        secondHandResult = "PlayerSecondHand win"
      else:
        secondHandResult = "PlayerSecondHand draw"
    else:
        secondHandResult = "No hands played"

    return firstHandResult + "," + secondHandResult

  def iterable_game_result(self):
    dealer_total = self.hand_total(self.dealers_cards)
    player_first_hand_total = self.hand_total(self.player_cards[0])
    player_second_hand_total = self.hand_total(self.player_cards[1])
    results = [None,None]

    if player_first_hand_total > 21:
      results[0] = "bust"
    else:
      if dealer_total > 21:
        results[0] = 'win'
      elif player_first_hand_total > dealer_total:
        results[0] = 'win'
      elif dealer_total > player_first_hand_total:
        results[0] = 'loss'
      else:
        results[0] = 'draw'
    
    if player_second_hand_total >= 1:
      if player_second_hand_total > 21:
        results[1] = "bust"
      else:
        if dealer_total > 21:
          results[1] = 'win'
        elif player_second_hand_total > dealer_total:
          results[1] = 'win'
        elif dealer_total > player_second_hand_total:
          results[1] = 'loss'
        else:
          results[1] = 'draw'
    
    return results

  def get_current_state(self,current_turn='playerFirstHand',action_to_take=None):
    print("inside blackjack",self.player_cards)
    if current_turn == 'playerFirstHand':
      current_hand_player_card = self.player_cards[0]
      hand_total = self.hand_total(current_hand_player_card)
      if len(self.player_cards[1]) > 0:
        if(len(self.player_cards[0]) == 1):
          play_idx = 0
        else:
          play_idx = 1
      else:
        if (len(self.player_cards[0]) == 2):
          play_idx = 0
        else:
          play_idx = 1
    else:
      current_hand_player_card = self.player_cards[1]
      hand_total = self.hand_total(current_hand_player_card)
      if(len(self.player_cards[1]) == 1):
        play_idx = 0
      else:
        play_idx = 1

    last_action_taken = action_to_take if action_to_take else self.last_action_taken
    return {
      "current_hand_player_card": current_hand_player_card,
      "dealer_card":[self.dealers_cards[0]],
      "dealer_idx":self.get_dealer_idx(self.dealers_cards[0]),
      "normal_hand_player_idx":self.get_normal_hand_player_idx(current_hand_player_card),
      "usable_ace_player_idx":self.get_usable_ace_player_idx(current_hand_player_card),
      "has_usable_ace":self.has_usable_ace(current_hand_player_card),
      "split_hand_player_idx":self.get_split_hand_player_idx(current_hand_player_card),
      "split_hand_possible":self.check_split_possible(current_hand_player_card),
      "valid_actions":self.get_valid_actions(),
      "last_action_taken":last_action_taken,
      "true_count":self.get_true_count(),
      "play_idx":play_idx,
      "hand_total":hand_total
    }

  def get_normal_hand_player_idx(self,cards):
    value = 0
    aces = 0
    for card in cards:
      cardValue = card.split("-")[0]
      if cardValue in ['J','Q','K']:
        value +=10
      elif cardValue == "A":
        if value + 11 > 21:
          value = value + 1
        else:
          aces +=1
          value = value + 11
      else:
        value = value + int(cardValue)

    while value > 21 and aces:
      value -=10
      aces -=1

    return value - 1

  def get_split_hand_player_idx(self,cards):
    face_value = cards[0].split('-')[0]
    if face_value in ["10","K","J","Q"]:
      return 10 - 1
    if face_value == "A":
      return 1 - 1
    return int(face_value) - 1

  def get_usable_ace_player_idx(self,cards):
    usable_ace_ommited = []
    if len(cards) < 1:
      return 0
    else:
      ace_count = 0
      for card in cards:
        card_value = card.split("-")[0]
        if card_value == 'A':
          ace_count = ace_count + 1  
        if card_value == 'A' and ace_count == 1:
          pass
        else:
          usable_ace_ommited.append(card)
      
    value = 0
    for card in usable_ace_ommited:
      cardValue = card.split("-")[0]
      if cardValue in ["J","Q","K"]:
        value +=10
      elif cardValue == "A":
        value += 1
      else:
        value = value + int(cardValue)
    
    return value - 1

  def get_dealer_idx(self,card):
    face_value = card.split("-")[0]
    if face_value in ["10","J","Q","K"]:
      return 10 - 1
    if face_value == 'A':
      return 11 - 1    
    return int(face_value) - 1


def main():
    game = Blackjack(1)
    for _ in range(53):
      game.start_game()
      status = game.check_blackjack()
      while status == "continue" or status == 'bustcontinue':
          # print("Player hands is",game.player_cards,game.hand_total(game.player_cards[0]),game.hand_total(game.player_cards[1]))
          # print("Dealer hand is",game.dealers_cards,game.hand_total(game.dealers_cards))
          # print(game.get_valid_actions())
          # print("true count is",game.get_true_count())
          validActions = game.get_valid_actions()
          action = input(f"Enter an action : {validActions}")
          status = game.player_action(action)
          if action == "stand":
              if(len(game.player_cards[1]) < 1):
                  break
              else:
                  if(game.current_turn == 'playerFirstHand'):
                      game.current_turn = 'playerSecondHand'
                      status = "continue"
                  else:
                      break
                  
      # print('Status is',status)
      # game.current_turn = 'playerFirstHand'
      # if status == "continue" or status == "continueDealer" or status == "bustcontinueDealer":
      #     # if dealer_action doesn't get called here, it get called on game_result if action is needed.
      #     game.dealer_action()
      
      print("Player cards and sum is",game.player_cards,game.hand_total(game.player_cards[0]),game.hand_total(game.player_cards[1]))
      print("Dealer cards and sum is",game.dealers_cards,game.hand_total(game.dealers_cards))

      print("Game result is",game.game_result())

      print("Player cards and sum is",game.player_cards,game.hand_total(game.player_cards[0]),game.hand_total(game.player_cards[1]))
      print("Dealer cards and sum is",game.dealers_cards,game.hand_total(game.dealers_cards))
    

if __name__ == "__main__":
    main()
