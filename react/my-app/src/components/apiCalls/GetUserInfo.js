async function GetUserInfo() {
    try {
        const response = await fetch(`http://localhost:5000/userinfo`, {
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
        return data.user;
    } catch (error) {
        console.error("Error getting user info:", error);
        return error;
    }
}

export default GetUserInfo