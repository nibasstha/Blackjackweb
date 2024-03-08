import { GameState, Turn } from "../types";
import { deckBuilder, initialGameState, distributeCards } from "../utils";
import { shuffle } from "../utils/shuffle";

export class Blackjack {
  gameState: GameState;
  betAmount: number;
  deckCount: number;

  constructor(betAmount: number, deckCount: number) {
    this.gameState = this.getInitialGameState(betAmount, deckCount);
    this.betAmount = betAmount;
  }

  getInitialGameState(betAmount: number, deckCount: number) {
    const deck = deckBuilder(deckCount);
    const gameState = initialGameState(deck, betAmount);
    return gameState;
  }

  setFirstPhaseCardDistribution() {
    // add a condition to check if deck is empty .
    //  handle cases where there is only 3 or 2 or 1 cards available atm.
    const firstFourDistribution = this.gameState.deck.splice(0, 3);

    const { playerCards, dealerCards } = distributeCards(firstFourDistribution);

    // assigning dealer his cards.
    this.gameState.dealersCards.revealed = dealerCards[0];
    this.gameState.dealersCards.unrevealed = dealerCards[1];

    // assigning player his cards.
    this.gameState.player.playerCards[0] = playerCards[0];
    this.gameState.player.playerCards[0] = playerCards[1];
  }

  standAction() {
    // stand action will change the currentTurn only.
    // call this to filp turns.

    // we don't need to add the firstPlayer here because, the turn won't switch back to the first player unless the game ends that is.

    if (this.gameState.currentTurn === Turn.dealerHand) {
      // add game end function here when the dealer stands because the game ends .
      // also add exit condition here.
    }

    if (this.gameState.player.playerCards[1].length > 0) {
      this.gameState.currentTurn === Turn.playerSecondHand;
      // add break condition here
    }

    if (this.gameState.currentTurn === Turn.playerSecondHand) {
      this.gameState.currentTurn = Turn.dealerHand;
    }
  }

  hitAction() {
    if (this.gameState.currentTurn === Turn.playerFirstHand) {
      // draw card
      // check gameState deck as well . It could be empty
      // if empty , first add cards to the deck
      const newCard = this.gameState.deck.shift();
      // remove if statement later .
      if (newCard) {
        this.gameState.player.playerCards[0].push(newCard);
      }
    }

    if (this.gameState.currentTurn === Turn.playerSecondHand) {
      const newCard = this.gameState.deck.shift();
      if (newCard) {
        this.gameState.player.playerCards[1].push(newCard);
      }
    }

    if (this.gameState.currentTurn === Turn.dealerHand) {
      const newCard = this.gameState.deck.shift();
      if (newCard) {
        this.gameState.dealersCards.revealed.push(newCard);
      }
    }
  }

  doubleAction() {
    // this action can only be initiated by player.
  }
}
