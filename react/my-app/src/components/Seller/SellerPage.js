import React, { useEffect, useState } from 'react';
import { Route, Router, useNavigate, withRouter } from 'react-router-dom';
import GetUserInfo from '../apiCalls/GetUserInfo';


function SellerPage() {

    const [user, setUser] = useState()

    /* useEffect(() => {
          function fetchData() {
            let user = GetUserInfo()
            if (user.role !== 'seller'){
                alert("Not a seller")
                navigate("/home")
            }
            else{
                setUser(user)
            }
        }
        fetchData();
      }); */


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
                console.log(response.msg)
            }
            else {
                console.log("Product Added")
            }
        }))
    }

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
                        <button type="submit">Submit</button>
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