import "./SetOfBasket.css"
import React, {useState} from "react";
import BasketItem from "./BasketItem";

function renderTile(current_item) {
    console.log("basketitem product = " + JSON.stringify(current_item))
    return(
        BasketItem(current_item)
    )
}

function SetOfBasketItems(props) {
    let tiles = []
        console.log("props are " + JSON.stringify(props.products))
        for (let i = 0; i < props.products.length; i++) {
            const current_item = props.products[i];
            console.log("current item is" + JSON.stringify(current_item))
            tiles.push(renderTile(current_item));
        }
    console.log(tiles)
    return <div className="completeBasket">{tiles}</div>;
}

export default SetOfBasketItems