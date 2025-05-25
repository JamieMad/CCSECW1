import { useState, useEffect } from "react";

async function GetProducts() {
    try {
        const response = await fetch("http://balls/getproducts", {
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
        
        console.log(data.products)
        return data.products || [];
    } catch (error) {
        console.error("Error fetching products:", error);
        return []; // Return empty array on failure
    }
}

export default GetProducts;
