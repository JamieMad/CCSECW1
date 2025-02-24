import React, {useState} from "react";
import { useNavigate } from 'react-router-dom';
import DeleteProduct from "../apiCalls/DeleteProduct";


export default function RenderTile(){
    function BuyerTile(product) {
        console.log("This is in product TIle" + JSON.stringify(product))
    
        let navigate = useNavigate();
    
    
            return (
                <div className="card">
                    <div className="card-content">
                        <img src= {product.image} width="200" height="200"/>
                        <h5 className="card-title">{product.name}</h5>
                        <p className="card-text">{product.description}</p>
                        <button type="text" onClick={() => navigate(`/product/${product.id}`)}> Go To Product Page </button>
                    </div>
                </div>
            )
    }
    
    function SellerTile(product) {
        console.log("This is in product TIle" + JSON.stringify(product))
    
            return (
                <div className="card">
                    <div className="card-content">
                        <img src= {product.image} width="200" height="200"/>
                        <h5 className="card-title">{product.name}</h5>
                        <p className="card-text">{product.description}</p>
                        <button type="text" onClick={() => DeleteProduct(product.id)}> Delete Product Forever </button>
                    </div>
                </div>
            )
    }
    return {BuyerTile, SellerTile}
}

