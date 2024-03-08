import { Turn } from "../../../../types";
import { checkHandTotal } from "../../../../utils/checkHandTotal";
import arrow from "../assets/arrow.png";
import universalChip from "../assets/universalChip.png";
import { Card } from "./Card";

type PlayerHandsProps = {
  playerCards: [string[], string[]];
  isVisible: boolean;
  currentTurn: Turn;
  bet: number[];
};

export function PlayerHands({
  playerCards,
  bet,
  isVisible,
  currentTurn,
}: PlayerHandsProps) {
  let firstHandTotalScore = 0;
  let secondHandTotalScore = 0;

  firstHandTotalScore = checkHandTotal(playerCards[0]);
  secondHandTotalScore = checkHandTotal(playerCards[1]);

  if (!isVisible) return <></>;

  return (
    <div
      style={{
        gap: 400,
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        width: "100%",
      }}
    >
      <div>
        <br />
        <div style={{ position: "relative", width: "250px" }}>
          <div
            style={{
              position: "absolute",
              left: -50,
              top: 60,
              height: "40px",
              width: "40px",
              border: "3px solid white",
              borderRadius: 40,
              display: "flex",
              justifyContent: "center",
              alignItems: "center",
              color: "white",
              fontWeight: "bold",
            }}
          >
            <span style={{ fontSize: "24px" }}>{firstHandTotalScore}</span>
          </div>
          {playerCards[0].map((c, idx) => (
            <div key={idx} style={{ position: "absolute", left: idx * 75 }}>
              <Card card={c} />
            </div>
          ))}
          <div
            style={{
              position: "absolute",
              top: 180,
              left: 20,
              textAlign: "center",
            }}
          >
            <div
              style={{
                display: "flex",
                flexDirection: "column",
                justifyContent: "center",
                alignItems: "center",
                width: "200px",
              }}
            >
              <img src={universalChip} height={70} width={70} />
              <div
                style={{
                  textAlign: "center",
                  marginTop: "15px",
                }}
              >
                <span
                  style={{
                    border: "5px solid grey",
                    borderRadius: "5px",
                    paddingLeft: "28px",
                    paddingRight: "28px",
                    paddingTop: "5px",
                    paddingBottom: "5px",
                    color: "white",
                    fontSize: "20px",
                    background:
                      "linear-gradient(180deg, #000000 0%, rgba(0, 0, 0, 0) 100%)",
                  }}
                >
                  {bet[0]}
                </span>
              </div>
            </div>
          </div>
          <div
            style={{
              position: "absolute",
              bottom: 0,
              right: "50%",
            }}
          >
            {currentTurn === Turn.playerFirstHand && <img src={arrow} />}
          </div>
        </div>
      </div>
      {secondHandTotalScore > 0 && (
        <div>
          <br />
          <div style={{ position: "relative", width: "250px" }}>
            <div
              style={{
                position: "absolute",
                left: -50,
                top: 60,
                height: "40px",
                width: "40px",
                border: "3px solid white",
                borderRadius: 40,
                display: "flex",
                justifyContent: "center",
                alignItems: "center",
                color: "white",
                fontWeight: "bold",
              }}
            >
              <span style={{ fontSize: "24px" }}>{secondHandTotalScore}</span>
            </div>
            {playerCards[1].map((c, idx) => (
              <div style={{ position: "absolute", left: idx * 75 }}>
                <Card card={c} />
              </div>
            ))}
            <div
              style={{
                position: "absolute",
                top: 180,
                left: 20,
                textAlign: "center",
              }}
            >
              <div
                style={{
                  display: "flex",
                  flexDirection: "column",
                  justifyContent: "center",
                  alignItems: "center",
                  width: "200px",
                }}
              >
                <img src={universalChip} height={70} width={70} />
                <div
                  style={{
                    textAlign: "center",
                    marginTop: "15px",
                  }}
                >
                  <span
                    style={{
                      border: "5px solid grey",
                      borderRadius: "5px",
                      paddingLeft: "28px",
                      paddingRight: "28px",
                      paddingTop: "5px",
                      paddingBottom: "5px",
                      color: "white",
                      fontSize: "20px",
                      background:
                        "linear-gradient(180deg, #000000 0%, rgba(0, 0, 0, 0) 100%)",
                    }}
                  >
                    {bet[0]}
                  </span>
                </div>
              </div>
            </div>
            <div
              style={{
                position: "absolute",
                bottom: 0,
                right: "50%",
              }}
            >
              {currentTurn === Turn.playerSecondHand && <img src={arrow} />}
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
