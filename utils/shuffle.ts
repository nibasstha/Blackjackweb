/*
Fisher-Yates shuffle
https://en.wikipedia.org/wiki/Fisher%E2%80%93Yates_shuffle
*/

export function shuffle(deck: string[]) {
  for (let i = deck.length - 1; i > 0; i -= 1) {
    const randomIndex = Math.floor(Math.random() * (i + 1));
    [deck[i], deck[randomIndex]] = [deck[randomIndex], deck[i]];
  }
  return deck;
}
