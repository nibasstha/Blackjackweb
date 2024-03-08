import { useEffect, useState } from "react";

function getStorageValue(defaultValue: number) {
  const saved = localStorage.getItem("coin");
  let initialValue = null;

  try {
    initialValue = JSON.parse(saved ? saved : defaultValue.toString());
  } catch {
    initialValue = defaultValue;
  }

  return initialValue;
}

export function useCoinValue(defaultValue: number) {
  const [value, setValue] = useState(() => getStorageValue(defaultValue));

  function setValueStorage(newValue: number) {
    console.log("received new value", newValue);
    localStorage.setItem("coin", newValue.toString());
    setValue(newValue);
  }

  return [value, setValueStorage];
}
