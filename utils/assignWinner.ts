import { GameState, Turn } from "../types";
import { checkHandTotal } from "./checkHandTotal";

// use this function only for
export function assignWinner(gameState: GameState) {
  const winnersInfo = gameState.winner;
  const dealerCards = gameState.dealersCards;
  const playerFirstHand = gameState.playerCards[0];
  const playerSecondHand = gameState.playerCards[1];

  const playerFirstHandSum = checkHandTotal(playerFirstHand);
  const playerSecondHandSum = checkHandTotal(playerSecondHand);
  const dealerHandSum = checkHandTotal(dealerCards);

  let firstHandWinner = null;
  let secondHandWinner = null;

  // for player first hand.
  // evaluation of first hand.
  if (winnersInfo[0] !== Turn.dealerHand) {
    if (playerFirstHandSum === dealerHandSum) {
      firstHandWinner = Turn.none;
    } else {
      if (dealerHandSum > 21) {
        firstHandWinner = Turn.playerFirstHand;
      } else {
        if (playerFirstHandSum > dealerHandSum) {
          firstHandWinner = Turn.playerFirstHand;
        } else {
          firstHandWinner = Turn.dealerHand;
        }
      }
    }
  } else {
    firstHandWinner = Turn.dealerHand;
  }
  // end of evaluation of second hand.

  // evaluation of second hand , if second hand exists.
  if (winnersInfo[1] !== Turn.dealerHand) {
    if (playerSecondHand.length > 0) {
      if (playerSecondHandSum === dealerHandSum) {
        secondHandWinner = Turn.none;
      } else {
        if (dealerHandSum > 21) {
          secondHandWinner = Turn.playerSecondHand;
        } else {
          if (playerSecondHandSum > dealerHandSum) {
            secondHandWinner = Turn.playerSecondHand;
          } else {
            secondHandWinner = Turn.dealerHand;
          }
        }
      }
    }
  } else {
    if (winnersInfo[1] !== null) {
      secondHandWinner = Turn.dealerHand;
    }
  }
  // end of second hand evaluation.

  return {
    ...gameState,
    winner: [firstHandWinner, secondHandWinner],
  } as GameState;
}
