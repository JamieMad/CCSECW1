import React, {useState} from "react";
import { useNavigate } from 'react-router-dom';




function ProductTile(product) {
    console.log("THis is in product TIle" + JSON.stringify(product))

    let navigate = useNavigate();


        return (
            <div className="card">
                <div className="card-content">
                    <img src='https://upload.wikimedia.org/wikipedia/commons/c/c0/Nicolas_Cage_Deauville_2013.jpg' width="200" height="200"/>
                    <h5 className="card-title">{product.name}</h5>
                    <p className="card-text">{product.description}</p>
                    <button type="text" onClick={() => navigate(`/product/${product.id}`)}> Go To Product Page </button>
                </div>
            </div>
        )
}
export default ProductTile