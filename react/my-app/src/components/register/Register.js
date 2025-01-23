import React, { useEffect, useState } from 'react';
import './Register.css'; // Optional: For styling the counter
import { Route, Router, useNavigate, withRouter } from 'react-router-dom';


function Register() {
    // Make API call to flask server including username and hashed password
    //Take API response and do the appropriate thing:
        // E.g. Wrong password or log them in
    let navigate = useNavigate();
    const [username, setUsername] = useState("");
    const [password, setPassword] = useState("");

    const handleSubmit = (event) => {
        event.preventDefault()
        fetch('http://localhost:5000/register', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: username,
                password: password,
            })
        })
    } //TODO should then zero the values i think

return (
    <div className="Register">
        <h1>Register</h1>
            <form onSubmit={handleSubmit}>  
                <p>Username:</p>
                <input type="text" onChange={(event) => setUsername(event.target.value)}/>
                <p>Password:</p>
                <input type="Password" onChange={(event) => setPassword(event.target.value)}/>
            <div>
                <button type="submit">Register</button> {/*add onCLick run login function */}
                <button type="text" onClick={() => {navigate("/home");}}>Home</button>
            </div>
            </form>
            
        </div>
    );
}

export default Register;