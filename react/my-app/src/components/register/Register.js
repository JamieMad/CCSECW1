import React, { useEffect, useState } from 'react';
import './Register.css'; // Optional: For styling the counter
import { Route, Router, useNavigate, withRouter } from 'react-router-dom';


function Register() {
    // Make API call to flask server including username and hashed password
    //Take API response and do the appropriate thing:
        // E.g. Wrong password or log them in

    const [data, setData] = useState([{}])
    useEffect(() => {
        fetch("/hello").then(
            res => res.json()
        ).then(
            data => {
                setData(data)
                console.log(data)
            }
        )
    }, [])


    let navigate = useNavigate();
return (
    <div className="Login">
        <h1>Register</h1>
            <form>  
                <p>Username:</p>
                <input type="text" />
                <p>Password:</p>
                <input type="Password" />
            </form>
            <div>
                <button type="submit">Register</button> {/*add onCLick run login function */}
                <button type="text" onClick={() => {navigate("/home");}}>Home</button>
            </div>
            
        </div>
    );
}

export default Register;