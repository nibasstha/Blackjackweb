import { checkHandTotal } from "./checkHandTotal";
import { deckBuilder } from "./deckBuilder";

export function distributeCards(cards: string[]) {
  let dealerCards;
  let playerCards;
  let updatedDeck;

  if (cards.length >= 4) {
    playerCards = [cards[0], cards[2]];
    dealerCards = [cards[1], cards[3]];
    if (checkHandTotal(playerCards) == 21) {
      playerCards = [cards[0], cards[4]];
      if (checkHandTotal(playerCards) == 21) {
        playerCards = [cards[0], cards[5]];
      }
    }

    updatedDeck = cards.slice(4, cards.length);
  } else {
    const deck = deckBuilder(3);
    playerCards = [deck[0], deck[2]];
    dealerCards = [deck[1], deck[3]];
    updatedDeck = deck.slice(4, deck.length);
  }
  return { playerCards, dealerCards, updatedDeck };
}
