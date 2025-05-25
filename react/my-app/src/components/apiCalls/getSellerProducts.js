async function GetSellerProducts(id) {
    try {
        const response = await fetch(`/api/getsellerproducts/${id}`, {
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
        console.log("Data is ", data)
        return data || [];
    } catch (error) {
        console.error("Error fetching products:", error);
        return []; // Return empty array on failure
    }
}

export default GetSellerProducts