import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import ProductCatalogue from '../products/productCatalogue';
import GetSellerProducts from '../apiCalls/getSellerProducts';

function SellerProducts() {
  let navigate = useNavigate();
  const [products, setProducts] = useState([]);

  useEffect(() => {
      async function fetchData() {
          const data = await GetSellerProducts(1); // Fetch only the products array
          console.log("The data is ", data)
          setProducts(data);
      }
      fetchData();
  }, []);
    return(
      <div className="Home">
        <h1>Home Page</h1>
        <div className='ProductCatalogue'>
          <ProductCatalogue products={products} pageUser={"seller"}/>
        </div>
        <button type="text" onClick={() => navigate("/login")}> Login </button>
        </div>
      );
  }
  export default SellerProducts;