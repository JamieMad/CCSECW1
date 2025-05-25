import React, { useState } from "react";

// Define a functional component named UploadAndDisplayImage
const UploadAndDisplayImage = () => {
  // Define a state variable to store the selected image
  const [file, setFile] = useState(null);

  const handleUpload = async (event) => {
    event.preventDefault()
    if (file) {
      console.log('Uploading file...');
      console.log(file)
      try {
        // You can write the URL of your server or any other endpoint used for file upload
        const result = await fetch('/api/uploadimage', {
          method: 'POST',
          headers: {
            'Accept': 'application/json',
            'Content-Type': 'application/json',
        },
          body: JSON.stringify({
            file: file
        })
        });
  
        const data = await result.json();
  
        //console.log(data);
      } catch (error) {
        console.error(error);
      }
    }
  };

  // Return the JSX for rendering
  return (
    <div>
      <h1>Upload Product Image</h1>

      {/* Checks if image exists */}
      {file && ( 
        <div>
          {/* Display the selected image */}
          <img
            alt="not found"
            width={"250px"}
            src={URL.createObjectURL(file)}
          />

          {console.log(URL.createObjectURL(file))}
          {/* Button to remove the selected image */}
          <button onClick={() => setFile(null)}>Remove</button>
          <button onClick={handleUpload} className="submit" > Confirm Upload</button>
        </div>
      )}

      {/* Input element to select the image file */}
      <input
        type="file"
        name="myImage"

        onChange={(event) => {
          console.log(event.target.files[0]); // Log the selected file
          setFile(event.target.files[0]); // Update the state with the selected file
        }}
      />
    </div>
  );
};

// Export the UploadAndDisplayImage component as default
export default UploadAndDisplayImage;