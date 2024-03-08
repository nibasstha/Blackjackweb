import random
class BlackjackGame:
    def __init__(self,deck_count):
        self.deck = self.generate_deck(deck_count)
        random.shuffle(self.deck)
        self.deck_count = deck_count
        self.dealers_cards = []
        self.player_cards = [[],[]]
        self.current_turn = "playerFirstHand"
    
    @staticmethod
    def generate_deck(deck_count):
        numbers=['A','2','3','4','5','6','7','8','9','10','J','Q','K']
        suits=['H','D','C','S']
        deck = [number+"-"+suit for count in range(deck_count) for suit in suits for number in numbers]
        return deck
    
    def deal_card(self,idx):
        if len(self.deck) > idx:
            return self.deck.pop(idx)
        else:
            self.deck = self.generate_deck(self.deck_count)
            random.shuffle(self.deck)
            print("new deck is",self.deck)
            return self.deck.pop(idx)
    
    def start_game(self):
        self.player_cards = [[self.deal_card(0),self.deal_card(2)],[]]
        self.dealers_cards = [self.deal_card(1),self.deal_card(3)]

    def check_blackjack(self):
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
    
    def player_action(self,action):
        if action == 'hit':
            if(self.current_turn == "playerFirstHand"):
                self.player_cards[0].append(self.deal_card(0))
                return self.game_status(action)
            if(self.current_turn == "playerSecondHand"):
                self.player_cards[1].append(self.deal_card(0))
                return self.game_status(action)
        if action == 'split':
            firstHand = self.player_cards[0][0]
            secondHand = self.player_cards[0][1]
            self.player_cards = [[firstHand],[secondHand]]
            self.current_turn = "playerFirstHand"
            return self.game_status(action)  
        if action == 'double':
            if(self.current_turn == 'playerFirstHand'):
                self.player_cards[0].append(self.deal_card(0))
                return self.game_status(action) 
            if(self.current_turn == 'playerSecondHand'):
                self.player_cards[1].append(self.deal_card(0))
                return self.game_status(action)
      
    def get_valid_actions(self):
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

      if((self.current_turn == "playerFirstHand" and len(self.player_cards[0]) in range(1,3) ) or (self.current_turn == "playerSecondHand" and len(self.player_cards[1]) in range(1,2))  ):
          validActions.append("double")
      
      if((self.current_turn == "playerFirstHand") and len(self.player_cards[0]) in range(1,3) and firstCardValue == secondCardValue):
          validActions.append("split")
      
      return validActions
       
    def dealer_action(self):
        while self.hand_total(self.dealers_cards) < 17 \
              and self.hand_total(self.player_cards[0]) <=21 \
              and (self.hand_total(self.dealers_cards)<=self.hand_total(self.player_cards[0]) \
              or (len(self.player_cards[1])>0 and self.hand_total(self.dealers_cards) <= self.hand_total(self.player_cards[1]))):
              self.dealers_cards.append(self.deal_card(0))
    
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
            if (self.current_turn!="playerSecondHand" and self.hand_total(playerFirstHand) >= 21):
              self.current_turn = "playerSecondHand"
              return "bustcontinue"
            if (self.current_turn == 'playerSecondHand' and self.hand_total(playerSecondHand) <21):
              return "continue"
            if self.hand_total(playerFirstHand) >= 21 and self.hand_total(playerSecondHand) < 21:
                self.current_turn = 'playerSecondHand'
                return "continue"
            if self.hand_total(playerFirstHand) < 21 and self.hand_total(playerSecondHand) > 21:
                print('BUST CONITNUE DEALER from engine')
                return "bustcontinueDealer"
            if self.hand_total(playerFirstHand) > 21 and self.hand_total(playerSecondHand) > 21:
                return "bust"
            if self.hand_total(playerFirstHand) < 21 and self.hand_total(playerSecondHand) == 21:
                return "continueDealer"
            if self.hand_total(playerFirstHand) <= 21 and self.hand_total(playerSecondHand) >=21:
               return "continueDealer"
            else:
                return "continue"
    
    def game_result(self):
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


def main():
    game = BlackjackGame(1)
    for _ in range(53):
      game.start_game()
      status = game.check_blackjack()
      while status == "continue" or status == 'bustcontinue':
          print("Player hands is",game.player_cards,game.hand_total(game.player_cards[0]),game.hand_total(game.player_cards[1]))
          print("Dealer hand is",game.dealers_cards,game.hand_total(game.dealers_cards))
          print(game.get_valid_actions())
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
                  
      print('Status is',status)
      if status == "continue" or status == "continueDealer" or status == "bustcontinueDealer":
          # if dealer_action doesn't get called here, it get called on game_result if action is needed.
          game.dealer_action()
      
      print("Player cards and sum is",game.player_cards,game.hand_total(game.player_cards[0]),game.hand_total(game.player_cards[1]))
      print("Dealer cards and sum is",game.dealers_cards,game.hand_total(game.dealers_cards))

      print("Game result is",game.game_result())

      print("Player cards and sum is",game.player_cards,game.hand_total(game.player_cards[0]),game.hand_total(game.player_cards[1]))
      print("Dealer cards and sum is",game.dealers_cards,game.hand_total(game.dealers_cards))
    

if __name__ == "__main__":
    main()