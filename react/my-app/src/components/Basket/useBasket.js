import { useState, useEffect } from "react";

export default function useBasket() {
  const getBasket = () => JSON.parse(localStorage.getItem("basket")) || []; // Gets what the basket value currently is
  const [basket, setBasket] = useState(getBasket()); // Assigns the value basket to the current basket state

  // Sync localStorage when basket changes
  useEffect(() => {
    localStorage.setItem("basket", JSON.stringify(basket)); // Everytime this hook is loaded the saved basket will be set the current basket value
  }, [basket]); // Runs every time the basket value is changed

  // Functions to add and remove products
  const addToBasket = (product) => { // Add to basket function, requires product passed in
    setBasket((prevBasket) => { // Sets the basket to the returned value
      if (!prevBasket.some((item) => item.id === product.id)) {  // Avoid duplicate items in basket
        alert("ERROR: you can only add 1 of each item to the basket")
        return [...prevBasket, product];
      }
      return prevBasket;
    });
  };

  const removeFromBasket = (product) => {
    setBasket((prevBasket) => {
      console.log("Removing item", prevBasket, product)
      return prevBasket.filter((item) => item.id !== product.id); // Returns prevBasket but without the product being removed
    });
  };

  return { basket, addToBasket, removeFromBasket }; // So can be accessed from other components
}