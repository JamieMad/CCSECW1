import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import './Home.css'; // Optional: For styling the counter

function Home() {
  let navigate = useNavigate();
      return (
        <div className="Home">
          <h1>Home Page</h1>
          <button type="text" onClick={() => navigate("/login")}> Login </button>
        </div>
      );
  }
  export default Home;