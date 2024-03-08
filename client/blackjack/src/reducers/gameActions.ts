import { GameState, Turn } from "../../../../types/GameState";

import { assignWinner } from "../../../../utils/assignWinner";
import { checkHandTotal } from "../../../../utils/checkHandTotal";

import { distributeCards } from "../../../../utils/distributeCards";
import { getAdditionalCards } from "../../../../utils/getAdditionalCards";

export function gameActions(
  state: GameState,
  action: { type: string; betAmount?: number }
) {
  switch (action.type) {
    case "initialGameStart": {
      const { playerCards, dealerCards, updatedDeck } = distributeCards(
        state.deck
      );

      const newGameState: GameState = {
        ...state,
        betAmount: action.betAmount ? [action.betAmount, 0] : [0, 0],
        dealersCards: dealerCards,
        playerCards: [playerCards, []],
        deck: updatedDeck,
        betPhase: false,
        showHoleCard: false,
      };
      // console.log("New game state is", JSON.stringify(newGameState, null, 2));
      return newGameState;
    }
    case "initializeNewRound": {
      const playerFirstHand = state.playerCards[0];
      const playerSecondHand = state.playerCards[1];
      const dealerHand = state.dealersCards;
      const newGameState: GameState = {
        ...state,
        garbageDeck: [
          ...state.garbageDeck,
          ...playerFirstHand,
          ...playerSecondHand,
          ...dealerHand,
        ],
        playerCards: [[], []],
        dealersCards: [],
        winner: [null, null],
        betAmount: [0, 0],
        currentTurn: Turn.playerFirstHand,
        betPhase: true,
        showHoleCard: false,
      };
      console.log(
        "Initialize new round is",
        JSON.stringify(newGameState, null, 2)
      );
      console.log("Garbage deck length ", newGameState.garbageDeck.length);
      console.log("AvailableDeck length", newGameState.deck.length);
      return newGameState;
    }

    case "hit": {
      const { newCard, newDeck } = getAdditionalCards(state.deck);
      let newGameState: GameState;
      if (state.currentTurn === Turn.playerFirstHand) {
        newGameState = {
          ...state,
          playerCards: [
            [...state.playerCards[0], newCard as string],
            [...state.playerCards[1]],
          ],
          deck: newDeck,
        };
      } else if (state.currentTurn === Turn.playerSecondHand) {
        newGameState = {
          ...state,
          playerCards: [
            [...state.playerCards[0]],
            [...state.playerCards[1], newCard as string],
          ],
          deck: newDeck,
        };
      } else {
        // does it ever reach here?
        console.log("Reached the forbidden land");
        newGameState = {
          ...state,
          dealersCards: [...state.dealersCards, newCard as string],
          deck: newDeck,
        };
      }

      // Only need to check if dealer won or not here. , stand case will handle the rest.

      // check win for first hand.
      const totalSumOfFirstHand = checkHandTotal(newGameState.playerCards[0]);
      if (
        totalSumOfFirstHand === 21 &&
        state.currentTurn === Turn.playerFirstHand
      ) {
        // need to switch turn to second hand if second hand exits
        if (newGameState.playerCards[1].length > 0) {
          newGameState = {
            ...newGameState,
            currentTurn: Turn.playerSecondHand,
          };
        } else {
          newGameState = {
            ...newGameState,
            currentTurn: Turn.dealerHand,
          };
        }
      }

      if (totalSumOfFirstHand > 21) {
        if (newGameState.playerCards[1].length > 0) {
          newGameState = {
            ...newGameState,
            winner: [Turn.dealerHand, newGameState.winner[1]],
            currentTurn: Turn.playerSecondHand,
          };
        } else {
          newGameState = {
            ...newGameState,
            winner: [Turn.dealerHand, newGameState.winner[1]],
            currentTurn: Turn.dealerHand,
          };
        }
      }

      // check win for second hand, if second hand exists.
      // greater than 1 because of split action .

      if (newGameState.playerCards[1].length > 1) {
        const totalSumOfSecondHand = checkHandTotal(
          newGameState.playerCards[1]
        );
        if (totalSumOfSecondHand === 21) {
          newGameState = {
            ...newGameState,
            currentTurn: Turn.dealerHand,
          };
        }
        if (totalSumOfSecondHand > 21) {
          newGameState = {
            ...newGameState,
            winner: [newGameState.winner[0], Turn.dealerHand],
          };
        }
      }

      console.log("Hit returns", JSON.stringify(newGameState, null, 2));
      return newGameState;
    }

    case "stand": {
      // check for second hand . if second hand exists flip turn to second hand .
      if (
        state.playerCards[1].length === 2 &&
        state.currentTurn == Turn.playerFirstHand
      ) {
        return {
          ...state,
          currentTurn: Turn.playerSecondHand,
        } as GameState;
      }

      // Repeat this loop until the sum is > playercards
      // or is > than 17 or = 17

      let newGameState: GameState = { ...state, showHoleCard: true };
      while (
        checkHandTotal(newGameState.dealersCards) < 17 &&
        (checkHandTotal(newGameState.dealersCards) <
          checkHandTotal(newGameState.playerCards[0]) ||
          (newGameState.playerCards[1].length > 0 &&
            checkHandTotal(newGameState.dealersCards) <
              checkHandTotal(newGameState.playerCards[1])))
      ) {
        console.log(
          "Game state before performing any actions is",
          JSON.stringify(state, null, 2)
        );

        const { newCard, newDeck } = getAdditionalCards(state.deck);

        newGameState = {
          ...newGameState,
          dealersCards: [...state.dealersCards, newCard as string],
          deck: newDeck,
        };
        state = newGameState;
      }

      const finalGameState = assignWinner(newGameState);
      console.log(
        "The final game state is",
        JSON.stringify(finalGameState, null, 2)
      );

      return finalGameState;
    }

    case "double": {
      console.log("Game state before doubling", JSON.stringify(state));
      const newCard = state.deck.shift();
      const newDeck = state.deck.splice(1, state.deck.length - 1);
      let newGameState: GameState;
      if (state.currentTurn === Turn.playerFirstHand) {
        newGameState = {
          ...state,
          playerCards: [
            [...state.playerCards[0], newCard as string],
            [...state.playerCards[1]],
          ],

          deck: newDeck,
          betAmount: [state.betAmount[0] * 2, state.betAmount[1]],
          currentTurn:
            state.playerCards[1].length === 2
              ? Turn.playerSecondHand
              : Turn.dealerHand,
          showHoleCard: state.playerCards[1].length === 2 ? false : true,
        };
      } else {
        newGameState = {
          ...state,
          playerCards: [
            [...state.playerCards[0]],
            [...state.playerCards[1], newCard as string],
          ],

          deck: newDeck,
          betAmount: [state.betAmount[0], state.betAmount[1] * 2],
          currentTurn: Turn.dealerHand,
          showHoleCard: true,
        };
      }
      console.log("new state after double aciton is", newGameState);
      console.log("New bet amount is", newGameState.betAmount);

      const totalSumOfFirstHand = checkHandTotal(newGameState.playerCards[0]);

      if (
        totalSumOfFirstHand === 21 &&
        state.currentTurn === Turn.playerFirstHand
      ) {
        // need to switch turn to second hand if second hand exits
        if (newGameState.playerCards[1].length > 0) {
          newGameState = {
            ...newGameState,
            currentTurn: Turn.playerSecondHand,
          };
        } else {
          newGameState = {
            ...newGameState,
            currentTurn: Turn.dealerHand,
          };
        }
      }

      if (totalSumOfFirstHand > 21) {
        if (newGameState.playerCards[1].length > 0) {
          newGameState = {
            ...newGameState,
            winner: [Turn.dealerHand, newGameState.winner[1]],
            currentTurn: Turn.playerSecondHand,
          };
        } else {
          newGameState = {
            ...newGameState,
            winner: [Turn.dealerHand, newGameState.winner[1]],
            currentTurn: Turn.dealerHand,
          };
        }
      }

      // check win for second hand, if second hand exists.
      // greater than 1 because of split action .

      if (newGameState.playerCards[1].length > 1) {
        const totalSumOfSecondHand = checkHandTotal(
          newGameState.playerCards[1]
        );
        if (totalSumOfSecondHand === 21) {
          return {
            ...newGameState,
            showHoleCard: true,
            currentTurn: Turn.dealerHand,
          } as GameState;
        }
        if (totalSumOfSecondHand > 21) {
          return {
            ...newGameState,
            winner: [newGameState.winner[0], Turn.dealerHand],
          } as GameState;
        }
      }

      console.log("Game state after doubling");
      return newGameState;
    }
    case "split": {
      const firstHand = state.playerCards[0][0];
      const secondHand = state.playerCards[0][1];

      const drawCard = getAdditionalCards(state.deck);

      const drawNewCard = getAdditionalCards(drawCard.newDeck);

      return {
        ...state,
        playerCards: [
          [firstHand, drawCard.newCard],
          [secondHand, drawNewCard.newCard],
        ],
        currentTurn: Turn.playerFirstHand,
        showHoleCard: false,
        deck: drawNewCard.newDeck,
      } as GameState;
    }
  }
  return state;
}
