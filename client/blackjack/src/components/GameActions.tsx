import { useEffect, useState } from "react";

import chip5 from "../assets/chip5.png";
import chip20 from "../assets/chip20.png";
import chip50 from "../assets/chip50.png";
import chip100 from "../assets/chip100.png";

import dealBtn from "../assets/dealBtn.png";
import clearBtn from "../assets/clearBtn.png";

import qlearningHintBtn from "../assets/qlearningHint.png";
import mctsHintBtn from "../assets/mctsHint.png";

import standBtn from "../assets/stand.png";
import hitBtn from "../assets/hit.png";
import doubleBtn from "../assets/double.png";
import splitBtn from "../assets/split.png";

import arrow from "../assets/arrow.png";
import mctsArrow from "../assets/mctsArrow.png";

import mctsWinRate from "../assets/mctsWinRate.png";
import qlearningWinRate from "../assets/qWinRate.png";

import { GameState } from "../../../../types";
import { getValidActions } from "../../../../utils/getValidActions";

import { notification } from "antd";

type GameActionProps = {
  dispatch: React.Dispatch<{
    type: string;
    betAmount?: number | undefined;
  }>;
  betAmount: Array<number>;
  showBetArea: boolean;
  state: GameState;
  qlearningHint: string | null;
  triggerQlearningHint: () => Promise<void>;
  mctsHint: string | null;
  triggerMctsHint: () => Promise<void>;
  localStorageCoins: any;
  setLocalStorageCoins: any;
};

export function GameActions({
  dispatch,
  betAmount,
  showBetArea,
  state,
  qlearningHint,
  triggerQlearningHint,
  mctsHint,
  triggerMctsHint,
  localStorageCoins,
  setLocalStorageCoins,
}: GameActionProps) {
  console.log("Inside game action", betAmount);
  console.log("Hint is", qlearningHint);
  const [bet, setBet] = useState(
    betAmount.reduce((acc, amount) => acc + amount)
  );

  console.log("localStorageCoins is", localStorageCoins);

  const validActions = getValidActions(state);

  const [coins, setCoins] = useState({
    five: 0,
    twenty: 0,
    fifty: 0,
    hundred: 0,
  });

  useEffect(() => {
    setBet(betAmount.reduce((acc, amount) => acc + amount));
    setCoins({ five: 0, twenty: 0, fifty: 0, hundred: 0 });
  }, [betAmount]);

  return (
    <div
      style={{
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      {showBetArea ? (
        <div
          style={{
            display: "flex",
            flexDirection: "column",
            justifyContent: "center",
            alignItems: "center",
            position: "relative",
          }}
        >
          <p
            style={{ fontSize: "150px", color: "white", marginBottom: "40px" }}
          >
            Place your bet
          </p>

          <span
            style={{
              position: "absolute",
              bottom: 90,
              right: -10,
              color: "white",
              border: "1px solid white",
              padding: "10px",
              borderRadius: "10px",
            }}
          >
            Total bet is {bet}
          </span>
          <div
            style={{
              height: 100,
              width: "60%",
              marginLeft: 20,
              display: "flex",
              justifyContent: "space-around",
              alignContent: "center",
              alignItems: "center",
              marginBottom: "70px",
            }}
          >
            <BetChips
              coinImg={chip5}
              coinCount={coins.five}
              setCoins={() =>
                setCoins((prev) => ({
                  ...prev,
                  five: prev.five + 1,
                }))
              }
              setBet={() => setBet((prev) => prev + 5)}
            />
            <BetChips
              coinImg={chip20}
              coinCount={coins.twenty}
              setCoins={() =>
                setCoins((prev) => ({
                  ...prev,
                  twenty: prev.twenty + 1,
                }))
              }
              setBet={() => setBet((prev) => prev + 20)}
            />
            <BetChips
              coinImg={chip50}
              coinCount={coins.fifty}
              setCoins={() =>
                setCoins((prev) => ({
                  ...prev,
                  fifty: prev.fifty + 1,
                }))
              }
              setBet={() => setBet((prev) => prev + 50)}
            />
            <BetChips
              coinImg={chip100}
              coinCount={coins.hundred}
              setCoins={() =>
                setCoins((prev) => ({
                  ...prev,
                  hundred: prev.hundred + 1,
                }))
              }
              setBet={() => setBet((prev) => prev + 100)}
            />
          </div>
          {bet > 0 ? (
            <div>
              <img
                style={{
                  width: "197px",
                  height: "69px",
                  marginRight: "20px",
                  cursor: "pointer",
                }}
                src={dealBtn}
                onClick={() => {
                  if (bet * 2 > localStorageCoins) {
                    notification.open({
                      type: "error",
                      message: "Insufficient balance.",
                      description:
                        "Your balance should be twice the bet amount.",
                    });
                  } else {
                    setLocalStorageCoins(localStorageCoins - bet);
                    dispatch({ type: "initialGameStart", betAmount: bet });
                  }
                }}
              />
              <img
                style={{ width: "197px", height: "69px", cursor: "pointer" }}
                src={clearBtn}
                onClick={() => {
                  setCoins({ five: 0, twenty: 0, fifty: 0, hundred: 0 });
                  setBet(0);
                }}
              />
            </div>
          ) : (
            <div style={{ height: "69px", width: "100%" }}></div>
          )}
        </div>
      ) : (
        <div
          style={{
            textAlign: "center",
            height: 100,
            width: 600,
            marginRight: 40,
            display: "flex",
            justifyContent: "center",
            alignContent: "center",
            alignItems: "center",
            gap: "20px",
          }}
        >
          {validActions.includes("hit") && (
            <div style={{ position: "relative" }}>
              {qlearningHint === "hit" && (
                <img
                  src={arrow}
                  style={{
                    position: "absolute",
                    top: -50,
                    right: 90,
                  }}
                />
              )}
              {mctsHint === "hit" && (
                <img
                  src={mctsArrow}
                  style={{ position: "absolute", top: -50, right: 20 }}
                />
              )}
              <img
                src={hitBtn}
                onClick={() => dispatch({ type: "hit" })}
                style={{ width: "197px", height: "69px", cursor: "pointer" }}
              />
            </div>
          )}
          {validActions.includes("stand") && (
            <div style={{ position: "relative" }}>
              {qlearningHint === "stand" && (
                <img
                  src={arrow}
                  style={{
                    position: "absolute",
                    top: -50,
                    right: 90,
                  }}
                />
              )}
              {mctsHint === "stand" && (
                <img
                  src={mctsArrow}
                  style={{
                    position: "absolute",
                    top: -50,
                    right: 20,
                  }}
                />
              )}
              <img
                src={standBtn}
                onClick={() => dispatch({ type: "stand" })}
                style={{ width: "197px", height: "69px", cursor: "pointer" }}
              />
            </div>
          )}
          {validActions.includes("double") && (
            <div style={{ position: "relative" }}>
              {qlearningHint === "double" && (
                <img
                  src={arrow}
                  style={{
                    position: "absolute",
                    top: -50,
                    right: 90,
                  }}
                />
              )}
              {mctsHint === "double" && (
                <img
                  src={mctsArrow}
                  style={{ position: "absolute", top: -50, right: 20 }}
                />
              )}
              <img
                src={doubleBtn}
                onClick={() => {
                  setLocalStorageCoins(localStorageCoins - state.betAmount[0]);
                  dispatch({ type: "double" });
                }}
                style={{ width: "197px", height: "69px", cursor: "pointer" }}
              />
            </div>
          )}
          {validActions.includes("split") && (
            <div style={{ position: "relative" }}>
              {qlearningHint === "split" && (
                <img
                  src={arrow}
                  style={{
                    position: "absolute",
                    top: -50,
                    right: 90,
                  }}
                />
              )}
              {mctsHint === "split" && (
                <img
                  src={mctsArrow}
                  style={{ position: "absolute", top: -50, right: 20 }}
                />
              )}
              <img
                src={splitBtn}
                onClick={() => {
                  setLocalStorageCoins(localStorageCoins - state.betAmount[0]);
                  dispatch({ type: "split" });
                }}
                style={{ width: "197px", height: "69px", cursor: "pointer" }}
              />
            </div>
          )}
          <img
            src={qlearningHintBtn}
            style={{
              position: "absolute",
              right: -130,
              bottom: 20,
              cursor: "pointer",
            }}
            onClick={triggerQlearningHint}
          />
          <img
            src={qlearningWinRate}
            style={{ position: "absolute", right: -130, bottom: 120 }}
          />
          <img
            src={mctsWinRate}
            style={{ position: "absolute", left: -130, bottom: 120 }}
          />
          <img
            src={mctsHintBtn}
            style={{
              position: "absolute",
              left: -130,
              bottom: 20,
              cursor: "pointer",
            }}
            onClick={triggerMctsHint}
          />
        </div>
      )}
    </div>
  );
}

type BetChipsProps = {
  coinCount: number;
  setCoins: any;
  setBet: any;
  coinImg: string;
};

function BetChips({ coinCount, setCoins, setBet, coinImg }: BetChipsProps) {
  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: 10,
      }}
    >
      <div
        style={{
          border: "1px solid white",
          height: "24px",
          width: "24px",
          borderRadius: "5px",
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
        }}
      >
        <span style={{ color: "white" }}>x{coinCount}</span>
      </div>
      <img
        src={coinImg}
        style={{ height: "90px", width: "90px" }}
        onClick={() => {
          setCoins();
          setBet();
        }}
      />
    </div>
  );
}
