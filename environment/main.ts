import { deckBuilder, initialGameState } from "../utils/index";

function Main() {
  const deck = deckBuilder(3);
  // TODO: add bet amount from outside.
  const betAmount = 100;
  const gameState = initialGameState(deck, betAmount);

  // generate a deck.
  // shuffle.
  // single game loop (player and dealer will switch turns)
  // getValidActions for player or dealer and perform it.
  // only switch turns if stand.
  //
}
