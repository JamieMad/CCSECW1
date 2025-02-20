import React from 'react';
import { BrowserRouter, Route, Routes, useParams } from 'react-router-dom';
import Login from './components/login/Login';
import Home from './components/home/Home';
import Register from './components/register/Register'
import ProductPage from './components/products/productpage';
import BasketPage from './components/Basket/BasketPage';

let Token; //Figure out auth tokens

function App() {
  /*if(!Token) {
    return <Login /> 
  }*/ //TODO Implement API call to check the session cookie
    return (
      <div className="wrapper">
        <h1>Ecommerce</h1>
          <Routes>
            <Route path = "/home" element={<Home />}/>
            <Route path = "/login" element={<Login />}/>
            <Route path = "/register" element={<Register />}/>
            <Route path = "/product/:id" element={<ProductPage />}/>
            <Route path = "/basket" element={<BasketPage/>}/>
          </Routes>
      </div>
    );
}
export default App;
  
