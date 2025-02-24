import React, {useState} from "react";
import './ProductCatalogue.css';
import RenderTile from "./productTile";

const {BuyerTile, SellerTile} = RenderTile()

function renderBuyer(current_item) {
    console.log("rendertile product = " + JSON.stringify(current_item))
    return(
        BuyerTile(current_item) // Loads function that actually does the rendering
    )
}
function renderSeller(current_item) {
    console.log("rendertile product = " + JSON.stringify(current_item))
    return(
        SellerTile(current_item) // Loads function that actually does the rendering
    )
}

function ProductCatalogue(props) { 
    let tiles = []
        console.log("props are " + JSON.stringify(props.products))
        for (let i = 0; i < props.products.length; i++) { // Goes through every item passed through
            const current_item = props.products[i];
            console.log("current item is" + JSON.stringify(current_item))
            if (props.pageUser == 'Buyer'){
                tiles.push(renderBuyer(current_item)); // Renders each item and adds them to the tiles array
            }

            else{
                tiles.push(renderSeller(current_item));
            }
            
        }
    console.log(tiles)
    return tiles
}

export default ProductCatalogue