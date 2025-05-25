async function DeleteProduct(id) {
    try {
        const response = await fetch(`/api/deleteproduct/${id}`, {
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
        return data;
    } catch (error) {
        console.error("Error deleting product:", error);
        return error;
    }
}

export default DeleteProduct