import { checkHandTotal } from "../../../../utils/checkHandTotal";
import { Card } from "./Card";

import firstHandDealerWin from "../assets/firstHandDealerWin.png";
import firstHandPlayerWin from "../assets/firstHandPlayerWin.png";
import firstHandDraw from "../assets/firstHandDraw.png";

import secondHandDealerWin from "../assets/secondHandDealerWin.png";
import secondHandPlayerWin from "../assets/secondHandPlayerWin.png";
import secondHandDraw from "../assets/secondHandDraw.png";
import dealerFrame from "../assets/dealerFrame.png";

import { Winners, playerMap } from "../../../../types";

type DealerHands = {
  dealerCards: string[];
  isVisible: boolean;
  showHoleCard: boolean;
  winner: [Winners, Winners];
};
export function DealersHands({
  dealerCards,
  isVisible,
  showHoleCard,
  winner,
}: DealerHands) {
  console.log("winners are", winner);
  console.log("show hole card", showHoleCard);
  const dealerVisibleCard = dealerCards.length === 0 ? [] : [dealerCards[0]];
  const handTotal = checkHandTotal(
    showHoleCard ? dealerCards : (dealerVisibleCard as string[])
  );

  if (!isVisible) return <></>;

  return (
    <div
      style={{
        width: "100%",
        display: "flex",
        flexDirection: "row",
        justifyContent: "center",
        alignItems: "center",
      }}
    >
      <div
        style={{
          position: "absolute",
          top: "-30px",
          color: "white",
        }}
      >
        <img src={dealerFrame} />
      </div>
      <div
        style={{
          position: "relative",
          width: "250px",
        }}
      >
        {winner[0] !== null && (
          <div
            style={{
              position: "absolute",
              left: "-530px",
              top: "100px",
              zIndex: 1000,
            }}
          >
            {playerMap[winner[0]] === "PlayerFirstHand" && (
              <img
                src={firstHandPlayerWin}
                style={{ height: "148px", width: "450px" }}
              />
            )}
            {playerMap[winner[0]] === "Dealer" && (
              <img
                src={firstHandDealerWin}
                style={{ height: "148px", width: "450px" }}
              />
            )}
            {playerMap[winner[0]] === "None" && (
              <img
                src={firstHandDraw}
                style={{ height: "148px", width: "450px" }}
              />
            )}
          </div>
        )}
        {winner[1] !== null && (
          <div
            style={{
              position: "absolute",
              right: "-530px",
              top: "100px",
              zIndex: 1000,
            }}
          >
            {playerMap[winner[1]] === "PlayerSecondHand" && (
              <img
                src={secondHandPlayerWin}
                style={{ height: "148px", width: "450px" }}
              />
            )}
            {playerMap[winner[1]] === "Dealer" && (
              <img
                src={secondHandDealerWin}
                style={{ height: "148px", width: "450px" }}
              />
            )}
            {playerMap[winner[1]] === "None" && (
              <img
                src={secondHandDraw}
                style={{ height: "148px", width: "450px" }}
              />
            )}
          </div>
        )}
        {/* {
          <div style={{ position: "absolute", right: "-530px", top: "100px" }}>
            <img
              src={firstHandDealerWin}
              style={{ height: "148px", width: "450px" }}
            />
          </div>
        } */}
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
          <span style={{ fontSize: "24px" }}>{handTotal}</span>
        </div>

        <RenderVisibleDealerHands
          dealerCards={dealerCards}
          showHoleCard={showHoleCard}
        />
      </div>
    </div>
  );
}

type RVDHProps = {
  dealerCards: string[];
  showHoleCard: boolean;
};

function RenderVisibleDealerHands({ dealerCards, showHoleCard }: RVDHProps) {
  return (
    <>
      {dealerCards.map((d, idx) => {
        return (
          <div style={{ position: "absolute", left: idx * 75 }} key={idx}>
            <Card card={d} showBack={idx === 0 ? false : !showHoleCard} />
          </div>
        );
      })}
    </>
  );
}
