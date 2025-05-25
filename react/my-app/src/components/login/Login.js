import React, { useState, useEffect } from 'react';
import './Login.css'; // Optional: For styling the counter
import { Route, Router, useNavigate, withRouter } from 'react-router-dom';


function Login() {
    // Make API call to flask server including username and hashed password
    //Take API response and do the appropriate thing:
        // E.g. Wrong password or log them in
        let navigate = useNavigate();
        const [username, setUsername] = useState("");
        const [password, setPassword] = useState("");
    
        const handleSubmit = (event) => {
            event.preventDefault()
            fetch('https://api:5000/login', {
                method: 'POST',
                headers: {
                    'Accept': 'application/json',
                    'Content-Type': 'application/json',
                },
            body: JSON.stringify({
                username: username,
                password: password,
            })
        }).then((res) =>
        res.json().then((response) => {
            if (response.msg !== "Login Success"){
                alert(response.msg)
            }
            else {
                navigate("/home")
            }
        }))
    }
    
return (
    <div className="Login">
        <h1>Log In</h1>
        <form onSubmit={handleSubmit}>  
                <p>Username:</p>
                <input type="text" onChange={(event) => setUsername(event.target.value)}/>
                <p>Password:</p>
                <input type="Password" onChange={(event) => setPassword(event.target.value)}/>
            <div>
                <button type="submit">Log In</button>
                <button type="text" onClick={() => {navigate("/home");}}>Home</button>
            </div>
            </form>
            
        </div>
    );
}

export default Login;