type DeckProps = {
  availableCards: string[];
};

export function Deck({ availableCards }: DeckProps) {
  if (availableCards.length > 0) {
    return (
      <div
        style={{
          position: "absolute",
          right: 50,
          top: 100,
          height: 100,
          width: 70,
          border: "1px solid black",
        }}
      >
        I am deck
      </div>
    );
  }
  return <p>No cards here</p>;
}
