
    // Get references to HTML elements
    const imageInput = document.getElementById('image');
    const imageContainer = document.getElementById('imageContainer');
    const uploadButton = document.getElementById('uploadButton');

    // Event listener for the file input change event
    imageInput.addEventListener('change', function () {
        // Check if a file is selected
        if (imageInput.files.length > 0) {
            const selectedImage = imageInput.files[0];
            // Create a FileReader to read and display the selected image
            const reader = new FileReader();
            reader.onload = function (e) {
                // Create an image element and set its source
                const imgElement = document.createElement('img');
                imgElement.src = e.target.result;

                // Set the width and height of the displayed image
                imgElement.style.width = '200px'; // Change to your desired width
                imgElement.style.height = 'auto'; // Maintain aspect ratio

                // Add the image element to the container
                imageContainer.innerHTML = '';
                imageContainer.appendChild(imgElement);
            };
            // Read the selected image as a data URL
            reader.readAsDataURL(selectedImage);
        }
    });

    // Optional: Add functionality to upload the selected image to the server
    uploadButton.addEventListener('click', function () {
        // Implement your upload logic here, e.g., send the selected image to the server
    });

    // Get references to HTML elements
// const imageInput = document.getElementById('image');
const predictButton = document.getElementById('predictButton');
const predictionResult = document.getElementById('predictionResult');

// Event listener for the predict button click
predictButton.addEventListener('click', () => {
    // Check if an image is selected
    if (imageInput.files.length > 0) {
        const selectedImage = imageInput.files[0];
        const formData = new FormData();
        formData.append('image', selectedImage);

        // Send the image to the server for prediction
        fetch('/predict', {
            method: 'POST',
            body: formData,
        })
        .then(response => response.json())
        .then(data => {
            // Display prediction results in the result container
            predictionResult.textContent = `Predicted Class: ${data.predicted_class}`;
        })
        .catch(error => {
            console.error('Prediction error:', error);
            predictionResult.textContent = 'Prediction failed.';
        });
    } else {
        predictionResult.textContent = 'Please select an image.';
    }
});

function predictImage() {
    var formData = new FormData();
    var imageInput = document.getElementById('image-input'); // Add an ID to your file input element
    formData.append('image', imageInput.files[0]);

    fetch('/predict/', {
      method: 'POST',
      body: formData,
    })
      .then(response => response.text())
      .then(data => {
        // Update the content of the response-container with the prediction result
        document.getElementById('response-container').textContent = data;
      })
      .catch(error => {
        // Handle any errors here
        console.error('Error:', error);
      });
  }





