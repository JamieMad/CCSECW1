import React, {useState} from "react";
import './ProductCatalogue.css';
import ProductTile from "./productTile";

function renderTile(current_item) {
    console.log("rendertile product = " + JSON.stringify(current_item))
    return(
        ProductTile(current_item)
    )
}

function ProductCatalogue(props) {
    let tiles = []
        console.log("props are " + JSON.stringify(props.products))
        for (let i = 0; i < props.products.length; i++) {
            const current_item = props.products[i];
            console.log("current item is" + JSON.stringify(current_item))
            tiles.push(renderTile(current_item));
        }
    console.log(tiles)
    return tiles
}

export default ProductCatalogue