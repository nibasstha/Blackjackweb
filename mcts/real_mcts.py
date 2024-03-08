import random
from enum import IntEnum
import sys
import argparse
# used for MCTS:
from math import sqrt
from numpy import log as ln # natural log

class Card:
    def __init__(self, color, rank, value):
        self.color = color
        self.rank = rank
        self.value = value
        
    def __str__(self):
        return self.rank + " of " + self.color
        
    def __eq__(self, other):
        return self.color == other.color and self.rank == other.rank

def generate_deck(suits=["Hearts", "Spades", "Clubs", "Diamonds"], 
                  ranks=[("2",2), ("3",3), ("4",4), ("5",5), ("6",6), ("7",7), ("8",8), ("9",9), ("10",10), ("Jack",10), ("Queen",10), ("King",10), ("Ace",11)]):
    result = []
    for suit in suits:
        for (rank,value) in ranks:
            result.append(Card(suit,rank,value))
    return result
    
def format(cards):
    if isinstance(cards, Card):
        return str(cards)
    return ", ".join(map(str, cards))
    
def get_value(cards):
    """
    Calculate the value of a set of cards. Aces may be counted as 11 or 1, to avoid going over 21
    """
    result = 0
    aces = 0
    for c in cards:
        result += c.value
        if c.rank == "Ace":
            aces += 1
    while result > 21 and aces > 0:
        result -= 10
        aces -= 1
    return result
    

class PlayerType(IntEnum):
    PLAYER = 1
    DEALER = 2
    
class Action(IntEnum):
    HIT = 1
    STAND = 2
    DOUBLE_DOWN = 3
    SPLIT = 4

class Player:
    """
    The basic player just chooses a random action
    """
    def __init__(self, name, deck):
        self.name = name
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards):
        return random.choice(actions)
    def reset(self):
        pass
    
class TimidPlayer(Player):
    """
    The timid player always stands, and never takes additional cards.
    """
    def get_action(self, cards, actions, dealer_cards):
        return Action.STAND
    
class BasicStrategyPlayer(Player):
    """
    Basic strategy: If the dealer has a card lower than a 7 open, we hit if we have less than 12. 
    Otherwise, we hit if we have less than 17.
    The idea being: If the dealer has a low card open, they are more likely to bust, if they have a high card open they are more likely to stand with a high score that we need to beat.
    """
    def get_action(self, cards, actions, dealer_cards):
        pval = get_value(cards)
        if dealer_cards[0].value < 7:
            if pval < 12:
                return Action.HIT 
            return Action.STAND 
        if pval < 17:
            return Action.HIT
        return Action.STAND


MCTS_N = 100


class MCTSPlayer():
    def __init__(self, name, deck):
        self.name = name
        self.bet = 2
        self.deck = deck
    def get_action(self, cards, actions, dealer_cards): 
        deck = self.deck[:]
        for p in cards:
            deck.remove(p)
        for p in dealer_cards:
            deck.remove(p)
        p = RolloutPlayer("Rollout", deck)
        g1 = Game(deck, p, verbose=False)
        results = {}
        for i in range(MCTS_N):
            p.reset()
            res = p.monte_carlo_tree_search(g1, cards, dealer_cards, self.bet)
            act = p.actions[0]
            if act not in results:
                results[act] = []
            results[act].append(res)
        act = p.getBestAction() 
        if act == Action.DOUBLE_DOWN:
            self.bet *= 2
        return act
    def reset(self):
        self.bet = 2
        
class RolloutPlayer(Player):
    def __init__(self, name, deck):
        self.name = name
        self.actions = []
        self.deck = deck
        self.root = Node(None) 
        self.listOfActions = [] 
        self.curr = self.root
        self.split_flag = False 
        self.iteration = 0 

    def get_action(self, cards, actions, dealer_cards):
        act = random.choice(actions)
        self.actions.append(act)
        return act

    def add_action(self, actionType):
        self.actions.append(actionType)

    def monte_carlo_tree_search(self, game, cards, dealer_cards, bet):
        leafNode = self.traverse(self.root)
        self.curr = leafNode
        simulation_reward = game.continue_round(cards, dealer_cards, bet) 
        self.backtrackExpectations(self.curr, simulation_reward) 

    def getBest_MCTS_Action(self, cards): 
        if(len(self.listOfActions)>1 and self.listOfActions[0] == Action.SPLIT and self.split_flag):
            temp = None
            if(len(cards)==1): 
                self.iteration = 1
            if(self.iteration < len(self.listOfActions)):
                temp = self.listOfActions[self.iteration]
            self.iteration += 1
            return temp
        elif(self.iteration < len(self.listOfActions) and self.iteration > -1):
            temp = self.listOfActions[self.iteration]
            self.iteration += 1
            return temp

        return None 

    def isLeafNode(self):
        return len(self.curr.children) == 0 or self.curr == self.root 

    def best_UCB(self, node):
        maxChild = None
        maxUCB = -100000
        for action, childNode in node.children.items():
            currUCB = float("inf") # initially never been visited
            if(childNode.visitations > 0):
                currUCB = childNode.expected_value*1.0/childNode.visitations + 2*sqrt(ln(childNode.parent.visitations)/childNode.visitations)
            if(currUCB > maxUCB):
                maxChild = childNode
                maxUCB = currUCB
        return maxChild

    def notTerminalState(self, node):
        return (node.actionType == Action.HIT.value or node.actionType == Action.SPLIT.value or self.root == node)

    def traverse(self, root):
        currNode = root
        while(len(currNode.children)!=0 and self.notTerminalState(currNode)):
            currNode = self.best_UCB(currNode) 
            self.listOfActions.append(Action(currNode.actionType))

        return currNode

    def checkIfExpansionNeeded(self, act, cards, splitPossibleBool, dealer_cards):
        if(act):
            self.add_action(act)
        if(self.isLeafNode() and self.curr.visitations > 0 and self.notTerminalState(self.curr)):
            self.curr.addAllChildren(self.curr, self.root, splitPossibleBool)
            if(self.curr==self.root and splitPossibleBool):
                self.split_flag = True
            tempActions = [Action.HIT, Action.STAND, Action.DOUBLE_DOWN] # add if(self.curr == self.root): actions.append(Action.SPLIT)
            newAct = self.get_action(cards, tempActions, dealer_cards[:1]) # random choice of actions array
            self.curr = self.curr.children[newAct.value] # new leaf node
            self.listOfActions.append(newAct) # append the new action
            act = newAct
            self.add_action(act)

    def backtrackExpectations(self, leafNode, reward):
        currNode = leafNode
        while(currNode): # while (currNode != None)
            currNode.visitations += 1
            currNode.expected_value += reward
            currNode = currNode.parent # go up the tree!
        # after updates, reset!
        self.listOfActions = []
        self.curr = self.root

    def reset(self):
        self.curr = self.root
        self.actions = []
        self.listOfActions = []
        self.iteration = 0 # new simulation for new picks
        self.split_flag = False # CHANGE: check if redundant

    def getBestAction(self):
        best_Exp_Value = -10000
        best_Exp_Action = Action.STAND
        # check all possibile actions
        # check each child node from root and select the one with best average expected value!
        for actType, actionNode in self.root.children.items():
            curr_avg = actionNode.expected_value*1.0/actionNode.visitations
            if curr_avg > best_Exp_Value:
                best_Exp_Value = curr_avg
                best_Exp_Action = Action(actType)
        return best_Exp_Action

class ConsolePlayer(Player):
    def get_action(self, cards, actions, dealer_cards):
        print()
        print("  Your cards:", format(cards), "(%.1f points)"%get_value(cards))
        print("  Dealer's visible card:", format(dealer_cards), "(%.1f points)"%get_value(dealer_cards))
        while True:
            print("  Which action do you want to take?")
            for i, a in enumerate(actions):
                print(" ", i+1, a.name)
            x = input()
            try:
                x = int(x)
                return actions[x-1]
            except Exception:
                print(" >>> Please enter a valid action number <<<")
    def reset(self):
        pass

class Dealer(Player):
    """
    The dealer has a fixed strategy: Hit when he has fewer than 17 points, otherwise stand.
    """
    def __init__(self):
        self.name = "Dealer"
    def get_action(self, cards, actions, dealer_cards):
        if get_value(cards) < 17:
            return Action.HIT
        return Action.STAND

def same_rank(a, b):
    return a.rank == b.rank
    
def same_value(a, b):
    return a.value == b.value


#################################################
# class node to build the tree for Rollout Player
class Node:
    def __init__(self, actionType, parent=None):
        self.actionType = actionType # Action.HIT, etc.. to get to the current node
        self.parent = parent                  # ref to parent, root is None
        self.children = {}                  # dictionary
        self.expected_value = 0             # initialize
        self.visitations = 0             # visits incremented upon back propagation!
    def addAllChildren(self, curr, root, rootAddSplitBool):
        if(curr==root and rootAddSplitBool): # only add all 4 children if we are able to!
            for actionObj in Action: # 1-4 inclusive                                            # root node, expand all 4
                self.children[actionObj.value] = Node(actionObj.value, parent=curr)
        elif(curr==root or curr.actionType == Action.HIT.value or curr.actionType == Action.SPLIT.value): # else: root, Split or Hit action, expand 3
            actions = [Action.HIT, Action.STAND, Action.DOUBLE_DOWN]
            for actionObj in actions: # 1-3 inclusive (exclude the Action.SPLIT==4)
                self.children[actionObj.value] = Node(actionObj.value, parent=curr)


class Game:
    def __init__(self, cards, player, split_rule=same_value, verbose=True):
        self.cards = cards
        self.player = player
        self.dealer = Dealer()
        self.dealer_cards = []
        self.player_cards = []
        self.split_cards = []
        self.verbose = verbose
        self.split_rule = split_rule


    def round(self): # sets up the game for dealer and player, sets up only initial, we call 'continue_round' thereafter.
        """
        Play one round of black jack. First, the player is asked to take actions until they
        either stand or have more than 21 points. The return value of this function is the 
        amount of money the player won.
        """
        self.deck = self.cards[:]
        random.shuffle(self.deck)
        self.dealer_cards = []
        self.player_cards = []
        self.bet = 2
        self.player.reset()
        self.dealer.reset()
        for i in range(2):
            self.deal(self.player_cards, self.player.name)
            self.deal(self.dealer_cards, self.dealer.name, i < 1)
        return self.play_round()
        
        
    def continue_round(self, player_cards, dealer_cards, bet):
        """
        Like round, but allows passing an initial game state in order to finish a partially played game.
       
        player_cards are the cards the player has in their hand
        dealer_cards are the visible cards (typically 1) of the dealer 
        bet is the current bet of the player 
        
        Note: For best results create a *new* Game object with a deck that has player_cards and dealer_cards removed.
        """
        self.deck = self.cards[:]
        random.shuffle(self.deck)
        self.bet = bet
        self.player_cards = player_cards[:]
        self.dealer_cards = dealer_cards[:]
        while len(self.dealer_cards) < 2:
            self.deal(self.dealer_cards, self.dealer.name)
        
        return self.play_round()
    

    def play_round(self):
        """
        Function used to actually play a round of blackjack after the initial setup done in round or continue_round.
        
        Will first let the player take their actions and then proceed with the dealer.
        """
        
        cards = self.play(self.player, self.player_cards)
        
        if self.verbose:
            print("Dealer reveals: ", format(self.dealer_cards[-1]))
            print("Dealer has:", format(self.dealer_cards), "(%.1f points)"%get_value(self.dealer_cards))
        self.play(self.dealer, self.dealer_cards)

        reward = sum(self.reward(c) for c in cards) # net reward if split or no split
        if self.verbose:
            print("Bet:", self.bet, "won:", reward, "\n")
        
        return reward

    def deal(self, cards, name, public=True):
        """
        Deal the next card to the given hand
        """
        card = self.deck[0]
        if self.verbose and public: 
            print(name, "draws", format(card))
        self.deck = self.deck[1:]
        cards.append(card)

    def play(self, player, cards, cansplit=True, postfix=""):
        """
        Play a round of blackjack for *one* participant (player or dealer).
        
        Note that a player may only split once, and only if the split_rule is satisfied (either two cards of the same rank, or of the same value)
        """
        
        while get_value(cards) < 21:
            actions = [Action.HIT, Action.STAND, Action.DOUBLE_DOWN]
            splitPossibleBool = (len(cards) == 2 and cansplit and self.split_rule(cards[0], cards[1])) # used by MCTS also

            if(splitPossibleBool): # this needs to be included when exploring children of Root, whether 3 or 4 children
                actions.append(Action.SPLIT)
            
            act = None # initially

            if(isinstance(player, RolloutPlayer)): # MCTS player
                act = player.getBest_MCTS_Action(cards) # if childNode return None, else: return best action from the given tree
                player.checkIfExpansionNeeded(act, cards, splitPossibleBool, self.dealer_cards)
            
            if(not act): # == None
                act = player.get_action(cards, actions, self.dealer_cards[:1]) # random choice of actions array


            if act in actions:
                if self.verbose:
                    print(player.name, "does", act.name)
                if act == Action.STAND:
                    break
                if act == Action.HIT or act == Action.DOUBLE_DOWN:
                    self.deal(cards, player.name)
                if act == Action.DOUBLE_DOWN:
                    self.bet *= 2
                    break
                if act == Action.SPLIT:
                    pilea = cards[:1]
                    pileb = cards[1:]
                    if self.verbose:
                        print(player.name, "now has 2 hands")
                        print("Hand 1:", format(pilea))
                        print("Hand 2:", format(pileb))
                    
                    self.play(player, pilea, cansplit=False, postfix=" (hand 1)")
                    self.play(player, pileb, cansplit=False, postfix=" (hand 2)")
                    return [pilea, pileb]

        # end while
        if self.verbose:
            print(player.name, "ends with%s"%(postfix), format(cards), "with value", get_value(cards), "\n")
        return [cards]

    def reward(self, player_cards):
        """
        Calculate amount of money won by the player. Blackjack pays 3:2.
        """
        pscore = get_value(player_cards)
        dscore = get_value(self.dealer_cards)
        if self.verbose:
            print(self.player.name + ":", format(player_cards), "(%.1f points)"%(pscore))
            print(self.dealer.name + ":", format(self.dealer_cards), "(%.1f points)"%(dscore))
        
        if pscore > 21:
            return -self.bet
        result = -self.bet
        if pscore > dscore or dscore > 21:
            if pscore == 21 and len(self.player_cards) == 2:
                result = 3*self.bet/2
            result = self.bet
        if pscore == dscore and (pscore != 21 or len(self.player_cards) != 2):
            result = 0
        return result


player_types = {"default": Player, "timid": TimidPlayer, "basic": BasicStrategyPlayer, "mcts": MCTSPlayer, "console": ConsolePlayer}

# Our implementation allows us to define different deck "types", such as only even cards, 
# or even use made-up card values like "1.5"

deck_types = {"default": generate_deck(), 
              "high": generate_deck(ranks=[("2", 2), ("10", 10), ("Ace", 11), ("Fool", 12)]),
              "low": generate_deck(ranks=[("1.5", 1.5), ("2", 2),("2.2", 2.2), ("3", 3), ("3", 4), ("Ace", 11)], suits=["Hearts", "Spades", "Clubs", "Diamonds", "Swords", "Wands", "Bows"]),
              "even": generate_deck(ranks=[("2",2), ("4",4), ("6",6), ("8",8), ("10",10), ("Jack",10), ("Queen",10), ("King",10)]),
              "odd": generate_deck(ranks=[("3",3), ("5",5), ("7",7), ("9",9), ("Ace",11)]),
              "red": generate_deck(suits=["Diamonds", "Hearts"]),
              "random": generate_deck(ranks=random.sample([("2",2), ("3",3), ("4",4), ("5",5), ("6",6), ("7",7), ("8",8), ("9",9), ("10",10), ("Jack",10), ("Queen",10), ("King",10), ("Ace",11)], random.randint(5,13)))}

def main(ptype="default", dtype="default", n=10000, split_rule=same_value, verbose=True):
    deck = deck_types[dtype]
    g = Game(deck, player_types[ptype]("The Prime Gladiator", deck[:]), split_rule, verbose)
    points = []
    for i in range(n):
        points.append(g.round())
    avg = sum(points)*1.0/n
    print("Average points: ", avg)


# run `python blackjack.py --help` for usage information
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Run a simulation of a Blackjack agent.')
    parser.add_argument('player', nargs="?", default="default", 
                        help='the player type (available values: %s)'%(", ".join(player_types.keys())))
    parser.add_argument('-n', '--count', dest='count', action='store', default=100,
                        help='How many games to run')
    parser.add_argument('-s', '-q', '--silent', '--quiet', dest='verbose', action='store_const', default=True, const=False,
                        help='Do not print game output (only average score at the end is printed)')
    parser.add_argument('-r', '--rank', '--rank-split', dest='split', action='store_const', default=same_value, const=same_rank,
                        help="Only allow split when the player's cards have the same rank (default: allow split when they have the same value)")
    parser.add_argument('-d', "--deck", metavar='D', dest="deck", nargs=1, default=["default"], 
                        help='the deck type to use (available values: %s)'%(", ".join(deck_types.keys())))
    args = parser.parse_args()
    if args.player not in player_types:
        print("Invalid player type: %s. Available options are: \n%s"%(args.player, ", ".join(player_types.keys())))
        sys.exit(-1)
    if args.deck[0] not in deck_types:
        print("Invalid deck type: %s. Available options are: \n%s"%(args.deck, ", ".join(deck_types.keys())))
        sys.exit(-1)
    main(args.player, args.deck[0], int(args.count), args.split, args.verbose)