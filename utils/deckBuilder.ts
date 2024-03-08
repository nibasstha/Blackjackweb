/**
 * Function to build a deck of card/cards.
 * @param [deckCount] to specify the number of deck of cards . A deck contains 52 cards.
 *
 */

export function deckBuilder(deckCount = 1) {
  const cardValues: string[] = [
    "A",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "10",
    "J",
    "Q",
    "K",
  ];
  const cardFaces: string[] = ["H", "D", "C", "S"]; // H -> heart , D -> diamond , C -> cub , S -> spade

  const deckOfCards: string[] = [];
  let tempCard;

  for (let deck = 0; deck < deckCount; deck++) {
    for (let cardFace of cardFaces) {
      for (let cardValue of cardValues) {
        tempCard = cardValue + "-" + cardFace;
        deckOfCards.push(tempCard);
      }
    }
  }

  return deckOfCards;
}
