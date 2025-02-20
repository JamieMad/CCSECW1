import "./BasketItem.css";
import useBasket from "./useBasket"; 
import { useEffect, useState } from "react";
import SetOfBasketItems from "./SetOfBasketItems";

function BasketPage() {
  const { basket, addToBasket, removeFromBasket } = useBasket();
  const [products, setProducts] = useState([]);

  useEffect(() => {
      // Directly use the basket from the custom hook
      setProducts(basket);
  }, [basket]);

  return (
    <div className="Home">
      <h1>Home Page</h1>
      <div className="ProductCatalogue">
        <SetOfBasketItems products={products} />
      </div>
    </div>
  );
}

export default BasketPage;