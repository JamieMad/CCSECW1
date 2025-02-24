import useBasket from "./useBasket";
import "./BasketItem.css"

function BasketItem(product){
    console.log(product)
    const {  removeFromBasket } = useBasket();
    return(
        <div class="basket">
                <div class="basketImage">
                    <img src='https://upload.wikimedia.org/wikipedia/commons/c/c0/Nicolas_Cage_Deauville_2013.jpg' width="200" height="200"/>
                </div>
                <div class="productDetails">
                    <h5>{product.name}</h5>
                    <p>{product.description}</p>
                </div>
                <div class="price">
                    <h5>{product.price}</h5>
                </div>
                <div class="removeButton">
                    <button type="button" onClick={() => removeFromBasket(product)}>
                        Remove From Basket
                    </button>
                </div>
        </div>
    );
}

export default BasketItem;
