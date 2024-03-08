/**
 * Initializes the game state of blackjack.
 * @param deck Deck of cards
 */

import { shuffle } from "./shuffle";
import { GameState, Turn } from "../types/index";

export function initialGameState(deck: string[], betAmount: number) {
  const shuffledCards = shuffle(deck);

  const gameState: GameState = {
    currentTurn: Turn.playerFirstHand,
    deck: shuffledCards,
    garbageDeck: [],
    dealersCards: [],
    playerCards: [[], []],
    betAmount: [0, 0],
    winner: [null, null],
    betPhase: true,
    showHoleCard: false,
  };

  return gameState;
}
