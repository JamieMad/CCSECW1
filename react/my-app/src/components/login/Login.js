import React, { useState } from 'react';
import './Login.css'; // Optional: For styling the counter

function Login() {
    // Declare a state variable 'count' and a function to update it 'setCount'
    const [count, setCount] = useState(0);

    // Function to handle incrementing the counter
    const increment = () => {
        setCount(count + 1);
        };

    // Function to handle decrementing the counter
    const decrement = () => {
        setCount(count - 1);
    };

return (
    <div className="Login">
        <h1>Log In</h1>
            <form>
                <p>Username:</p>
                <input type="text" />
                <p>Password:</p>
                <input type="text" />
            </form>
            <button onClick={increment}>Log In</button>
        </div>
    );

}

export default Login;