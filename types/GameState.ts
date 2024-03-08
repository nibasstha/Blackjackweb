export type GameState = {
  deck: string[];
  garbageDeck: string[];

  dealersCards: string[];

  playerCards: [string[], string[]];

  currentTurn: Turn;

  betAmount: Array<number>;

  winner: [Winners, Winners];

  // winner:
  //   | null
  //   | Turn.playerFirstHand
  //   | Turn.playerSecondHand
  //   | Turn.dealerHand
  //   | Turn.none;

  /**
   * player encapsulates the betAmount and playerCards.
   * playersCards is an array of array because of features like split. In such cases , player gets to play 2 seperate hands.
   * to add cards to players hand, if it is a game without split , push the cards to the zero index of the array.
   * else push it to the playerCards array directly.
   *
   **/

  betPhase: boolean; // for ui only
  showHoleCard: boolean;
};

export type Winners =
  | Turn.playerFirstHand
  | Turn.playerSecondHand
  | Turn.dealerHand
  | Turn.none
  | null;

export enum Turn {
  playerFirstHand = 1,
  playerSecondHand = 2,
  dealerHand = 3,
  none = 4,
}

export const playerMap = {
  1: "PlayerFirstHand",
  2: "PlayerSecondHand",
  3: "Dealer",
  4: "None",
};
