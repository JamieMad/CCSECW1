import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css'; // Optional: For styling the counter
import ProductCatalogue from '../products/productCatalogue';
import GetProducts from '../apiCalls/getProducts';

function Home() {
  let navigate = useNavigate();
  const [products, setProducts] = useState([]);

  useEffect(() => {
      async function fetchData() {
          const data = await GetProducts(); // Fetch only the products array
          setProducts(data);
      }
      fetchData();
  }, []);
    return(
      <div className="Home">
        <h1>Home Page</h1>
        <div className='ProductCatalogue'>
          <ProductCatalogue products={products}/>
        </div>
        <button type="text" onClick={() => navigate("/login")}> Login </button>
        </div>
      );
  }
  export default Home;