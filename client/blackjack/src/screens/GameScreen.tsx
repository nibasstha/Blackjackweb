import { useEffect, useReducer, useState } from "react";
import { DealersHands } from "../components/DealersHands";
import { GameActions } from "../components/GameActions";
import { PlayerHands } from "../components/PlayerHands";
import {
  checkRoundEnd,
  deckBuilder,
  initialGameState,
} from "../../../../utils/index";

import { GameState, Turn } from "../../../../types";
import { gameActions } from "../reducers/gameActions";
import "../styles/gameScreen.css";

type GameScreenProps = {
  localStorageCoins: any;
  setLocalStorageCoins: any;
};

export function GameScreen({
  localStorageCoins,
  setLocalStorageCoins,
}: GameScreenProps) {
  const [state, dispatch] = useReducer(
    gameActions,
    initialGameState(deckBuilder(3), 0)
  );

  const [qlearningHint, setQlearningHint] = useState(null);
  const [mctsHint, setMctsHint] = useState(null);

  async function getQlearningAgent() {
    const res = await fetch("http://localhost:8000/qlearning", {
      method: "POST",
      headers: {
        "Access-Control-Allow-Origin": "http://localhost:8001",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state: state }),
    });
    const jsoned = await res.json();
    setQlearningHint(jsoned.action);
    setTimeout(() => {
      setQlearningHint(null);
    }, 2000);
  }

  async function getMctsAgent() {
    const res = await fetch("http://localhost:8000/mcts", {
      method: "POST",
      headers: {
        // "Access-Control-Allow-Origin": "http://localhost:8001",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state: state }),
    });
    const jsoned = await res.json();
    setTimeout(() => {
      setMctsHint(jsoned.action);
    }, 2500);
    setTimeout(() => {
      setMctsHint(null);
    }, 4000);
  }

  async function writeHistory(state: GameState) {
    await fetch("http://localhost:8000/history", {
      method: "POST",
      headers: {
        // "Access-Control-Allow-Origin": "http://localhost:8001",
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ state: state }),
    });
  }

  useEffect(() => {
    if (
      state.currentTurn === Turn.dealerHand &&
      checkRoundEnd(state.winner, state.playerCards) === false
    ) {
      console.log("Dispatching stand when currentTurn changes");
      dispatch({ type: "stand" });
    }
    if (checkRoundEnd(state.winner, state.playerCards)) {
      console.log(
        "For some reason this is true",
        checkRoundEnd(state.winner, state.playerCards)
      );
      setTimeout(() => {
        console.log(
          "dispatching newGame Starttt",
          checkRoundEnd(state.winner, state.playerCards)
        );

        let currencyToAdd = 0;
        state.betAmount.forEach((bet, idx) => {
          if (idx === 0) {
            if (
              state.winner[0] === Turn.playerFirstHand ||
              state.winner[0] === Turn.none
            ) {
              currencyToAdd = bet;
            }
          } else {
            if (
              state.winner[1] === Turn.playerSecondHand ||
              state.winner[1] === Turn.none
            ) {
              currencyToAdd = bet;
            }
          }
        });

        setLocalStorageCoins(localStorageCoins + currencyToAdd);

        writeHistory(state);

        dispatch({ type: "initializeNewRound" });
      }, 5000);
    }
  }, [
    localStorageCoins,
    setLocalStorageCoins,
    state,
    state.currentTurn,
    state.playerCards,
    state.winner,
  ]);

  return (
    <div className="canvas">
      <div
        style={{
          width: "100%",
          marginTop: "50px",
          marginBottom: "250px",
        }}
      >
        <DealersHands
          dealerCards={state.dealersCards}
          isVisible={!state.betPhase}
          showHoleCard={state.showHoleCard}
          winner={state.winner}
        />
      </div>
      <div style={{ width: "100%", marginTop: "30px" }}>
        <PlayerHands
          playerCards={state.playerCards}
          isVisible={!state.betPhase}
          currentTurn={state.currentTurn}
          bet={state.betAmount}
        />
      </div>

      <div
        style={{
          position: "absolute",
          bottom: -20,
          width: "100%",
        }}
      >
        <GameActions
          dispatch={dispatch}
          betAmount={state.betAmount}
          showBetArea={state.betPhase}
          state={state}
          qlearningHint={qlearningHint}
          triggerQlearningHint={getQlearningAgent}
          mctsHint={mctsHint}
          triggerMctsHint={getMctsAgent}
          localStorageCoins={localStorageCoins}
          setLocalStorageCoins={setLocalStorageCoins}
        />
      </div>
    </div>
  );
}
