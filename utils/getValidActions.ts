import { GameState, Turn } from "../types";

export function getValidActions(state: GameState) {
  if (state.betPhase) {
    return [];
  }

  const validActions = ["stand", "hit"];
  let firstCardValue = state.playerCards[0][0].split("-")[0];
  let secondCardValue = "0";

  if (["J", "Q", "K"].includes(firstCardValue)) {
    firstCardValue = "10";
  }

  secondCardValue = state.playerCards[0][1].split("-")[0];
  if (["J", "Q", "K"].includes(secondCardValue)) {
    secondCardValue = "10";
  }

  if (state.playerCards[1].length > 0) {
    if (
      state.currentTurn == Turn.playerFirstHand &&
      state.playerCards[0].length == 2
    ) {
      validActions.push("double");
    }
    if (
      state.currentTurn == Turn.playerSecondHand &&
      state.playerCards[1].length == 2
    ) {
      validActions.push("double");
    }
  } else {
    if (
      state.currentTurn == Turn.playerFirstHand &&
      state.playerCards[0].length == 2
    ) {
      validActions.push("double");
    }
  }

  console.log(
    "currentTurn,playerCards[0],",
    state.currentTurn == Turn.playerFirstHand,
    state.playerCards[0].length == 2,
    parseInt(firstCardValue) == parseInt(secondCardValue),
    firstCardValue,
    secondCardValue,
    state.playerCards[0]
  );
  if (
    state.currentTurn == Turn.playerFirstHand &&
    state.playerCards[0].length == 2 &&
    parseInt(firstCardValue) == parseInt(secondCardValue) &&
    state.playerCards[1].length == 0
  ) {
    validActions.push("split");
  }

  console.log(
    "valid actions returning",
    validActions,
    state.currentTurn,
    state.playerCards
  );

  return validActions;
}
