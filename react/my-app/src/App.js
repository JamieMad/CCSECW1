import React from 'react';
import { BrowserRouter, Route, Routes, useNavigate, useParams } from 'react-router-dom';
import Login from './components/login/Login';
import Home from './components/home/Home';
import Register from './components/register/Register'
import ProductPage from './components/products/productpage';
import BasketPage from './components/Basket/BasketPage';
import SellerPage from './components/Seller/SellerPage';
import SellerProducts from './components/Seller/SellerProducts';
import Banner from './components/Banner/Banner';


function App() {
    return (
      <div className="wrapper">
        <Banner/>
          <Routes>
            <Route path = "/" element={<Home />}/>
            <Route path = "/login" element={<Login />}/>
            <Route path = "/register" element={<Register />}/>
            <Route path = "/product/:id" element={<ProductPage />}/>
            <Route path = "/basket" element={<BasketPage/>}/>
            <Route path = "/seller" element={<SellerPage/>}/>
            <Route path = "/seller/products" element={<SellerProducts/>}/>
          </Routes>

      </div>
    );
}
export default App;
  
