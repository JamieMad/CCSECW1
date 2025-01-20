import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './components/login/Login';
import Home from './components/home/Home';
import Register from './components/register/Register'

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
          </Routes>
      </div>
    );
}
export default App;