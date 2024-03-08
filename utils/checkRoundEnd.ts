import { Winners } from "../types/GameState";

export function checkRoundEnd(
  winner: [Winners, Winners],
  playerCards: [string[], string[]]
) {
  if (winner[1] === null && winner[0] == null) {
    return false;
  }
  if (playerCards[1].length === 0 && winner[0] !== null) {
    console.log(
      "TrueLog playerCards[1].length === 0 && winner[0] !== null",
      winner,
      playerCards
    );
    return true;
  }
  if (winner[0] !== null && winner[1] !== null) {
    console.log(
      "TrueLog winner[0] !== null && winner[1] !== null",
      winner,
      playerCards
    );
    return true;
  }
  return false;
}
