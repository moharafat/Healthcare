
document.addEventListener('DOMContentLoaded', function () {
    const form = document.getElementById('application-form');
    const locationButton = document.getElementById('location-button');
    const locationInput = document.getElementById('location');

    // Function to handle form submission
    form.addEventListener('submit', function (event) {
        event.preventDefault(); // Prevent the form from submitting the default way

        const formData = {
            firstname: document.getElementById('firstname').value,
            lastname: document.getElementById('lastname').value,
            email: document.getElementById('email').value,
            specialty: document.getElementById('specialty').value,
            location: document.getElementById('location').value
        };

        console.log('Form Data:', formData);

        // Example of sending formData to your server here using fetch or any other method

        fetch('/submit-application', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => response.json())
        .then(data => {
            console.log('Success:', data);
            // Handle success actions here
        })
        .catch((error) => {
            console.error('Error:', error);
            // Handle error actions here
        });

    });
});



document.getElementById('location-button').addEventListener('click', function() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
        alert("Geolocation is not supported by this browser.");
    }
});

function showPosition(position) {
    const lat = position.coords.latitude;
    const lon = position.coords.longitude;
    document.getElementById('location').value = `Latitude: ${lat}, Longitude: ${lon}`;
}

function showError(error) {
    switch(error.code) {
        case error.PERMISSION_DENIED:
            alert("User denied the request for Geolocation.");
            break;
        case error.POSITION_UNAVAILABLE:
            alert("Location information is unavailable.");
            break;
        case error.TIMEOUT:
            alert("The request to get user location timed out.");
            break;
        case error.UNKNOWN_ERROR:
            alert("An unknown error occurred.");
            break;
    }
}

document.getElementById('application-form').addEventListener('submit', function(event) {
    event.preventDefault();
    alert('Application submitted successfully!');
    // Here you can add code to handle form submission
    // send the data to a server.
});
