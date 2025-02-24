import React, {useState, useEffect} from "react";
import { useNavigate, useParams } from 'react-router-dom';
import GetSingleProduct from "../apiCalls/getSingleProduct";
import UploadAndDisplayImage from "../images/UploadandDisplay";
import useBasket from "../Basket/useBasket";


function ProductPage() {
    let { id } = useParams();
    const [product, setProduct] = useState(null);
    let navigate = useNavigate();

    const { addToBasket } = useBasket();
  
    console.log("Product ID:", id);
  
    useEffect(() => {
      async function fetchData() {
        const data = await GetSingleProduct(id);
        console.log("Fetched product:", data);
        setProduct(data);
      }
      fetchData();
    }, [id]);
  
    // Show a loading state until product is available
    if (!product) {
      return <div>Loading...</div>;
    }
  
    return (
      <div className="card">
        <div className="card-content">
          <img
            src="https://upload.wikimedia.org/wikipedia/commons/c/c0/Nicolas_Cage_Deauville_2013.jpg"
            width="200"
            height="200"
            alt="Product"
          />
          <h5 className="card-title">{product.name}</h5>
          <p className="card-text">{product.description}</p>
          <button type="button" onClick={() => addToBasket(product)}>
            Add to basket
          </button>
        </div>
        <UploadAndDisplayImage></UploadAndDisplayImage>
      </div>
    );
  }
  
export default ProductPage