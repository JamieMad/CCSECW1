import { useState, useEffect } from "react";

async function GetSingleProduct(id) {
    console.log("in function")
    try {
        const response = await fetch(`/api/getsingleproduct/${id}`, {
            method: "GET",
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json",
            },
        });

        if (!response.ok) {
            throw new Error(`HTTP error! Status: ${response.status}`);
        }

        const data = await response.json();
        console.log(data)
        
        console.log(data.product)
        return data.product;
    } catch (error) {
        console.error("Error fetching product:", error);
        return null;
    }
}

export default GetSingleProduct;
