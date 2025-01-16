import React from 'react';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import Login from './components/login/Login';
import Home from './components/home/Home';

let Token;

function App() {
  if(!Token) {
    return <Login />
  }

    return (
      <div className="wrapper">
        <h1>Simple Counter Application</h1>
        <BrowserRouter>
          <Routes>
            <Route path = "/home" element={<Home />}/>
            <Route path = "/login" element={<Login />}/>
          </Routes>
        </BrowserRouter>
      </div>
    );
}
export default App;