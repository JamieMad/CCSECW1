import { useState, useEffect } from "react";

export default function useBasket() {
  const getBasket = () => JSON.parse(localStorage.getItem("basket")) || [];
  const [basket, setBasket] = useState(getBasket());

  // Optional: Sync localStorage when basket changes
  useEffect(() => {
    localStorage.setItem("basket", JSON.stringify(basket));
  }, [basket]);

  // Functions to add and remove products
  const addToBasket = (product) => {
    setBasket((prevBasket) => {
      // Avoid duplications or add logic as needed
      if (!prevBasket.includes(product)) {
        return [...prevBasket, product];
      }
      return prevBasket;
    });
  };

  const removeFromBasket = (product) => {
    setBasket((prevBasket) => {
      return prevBasket.filter((item) => item !== product);
    });
  };

  return { basket, addToBasket, removeFromBasket };
}