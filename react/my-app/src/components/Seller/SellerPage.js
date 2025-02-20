import React, { useEffect, useState } from 'react';
import { Route, Router, useNavigate, withRouter } from 'react-router-dom';


function SellerPage() {
    // Make API call to flask server including username and hashed password
    //Take API response and do the appropriate thing:
        // E.g. Wrong password or log them in
    let navigate = useNavigate();
    const [name, setName] = useState("");
    const [description, setDescription] = useState("");
    const [cost, setCost] = useState(0);

    const handleSubmit = (event) => {
        event.preventDefault()
        fetch('http://localhost:5000/addproduct', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                name: name,
                description: description,
                cost : cost,
                seller : 1,
            })
        }).then((res) =>
        res.json().then((response) => {
            if (response.msg !== "Success"){
                console.log("AAAH")
            }
            else {
                console.log("Product Added")
            }
        }))
    } //TODO should then zero the values i think

return (
    <div className='SellerWrapper'>
        <div className="AddProduct">
            <h1>Add A Product</h1>
                <form onSubmit={handleSubmit}>  
                    <p>Name:</p>
                    <input type="text" onChange={(event) => setName(event.target.value)}/>
                    <p>Description:</p>
                    <input type="text" onChange={(event) => setDescription(event.target.value)}/>
                    <p>Cost:</p>
                    <input type="text" onChange={(event) => setCost(Number(event.target.value))}/>
                    <div>
                        <button type="submit">Register</button>
                        <button type="text" onClick={() => {navigate("/home");}}>Home</button>
                    </div>
                </form>
        </div>

        <div className='SellersProducts'>
            <button type="text" onClick={() => navigate("/seller/products")}>
                View My Products
            </button>
        </div>
    </div>
    
    );
}

export default SellerPage;