export function checkHandTotal(cards: string[]) {
  let sum = 0;
  let aces = 0;
  for (let card of cards) {
    const faceValue = card.split("-")[0];
    if (faceValue === "K" || faceValue === "J" || faceValue === "Q") {
      sum = sum + 10;
    } else if (faceValue === "A") {
      if (sum + 11 > 21) {
        sum = sum + 1;
      } else {
        aces += 1;
        sum = sum + 11;
      }
    } else {
      sum = sum + parseInt(faceValue);
    }
  }

  while (sum > 21 && aces > 0) {
    sum = sum - 10;
    aces -= 1;
  }

  console.log("Inside checkhand total, sum of cards is", sum);
  return sum;
}
