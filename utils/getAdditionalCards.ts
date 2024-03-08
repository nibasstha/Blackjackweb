import { deckBuilder } from "./deckBuilder";

export function getAdditionalCards(deck: string[]) {
  let newCard;
  let newDeck;
  let newGarbageDeck;
  if (deck.length !== 0) {
    newCard = deck.shift();
    newDeck = deck;
  } else {
    const deck = deckBuilder(3);
    newCard = deck.shift();
    newDeck = deck;
  }

  return { newCard, newDeck };
}
