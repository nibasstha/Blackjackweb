type GarbageDeckProps = {
  garbageDeck: string[];
};
export function GarbageDeck({ garbageDeck }: GarbageDeckProps) {
  if (garbageDeck.length > 0) {
    return (
      <div
        style={{
          position: "absolute",
          left: 50,
          top: 100,
          height: 100,
          width: 70,
          border: "1px solid black",
        }}
      >
        Garbage deck
      </div>
    );
  }
  return <p>no decks</p>;
}
