document.addEventListener("DOMContentLoaded", function() {
    const form = document.getElementById("application-form");
    // const locationButton = document.getElementById("location-button");
    // const locationInput = document.getElementById("location");

    // locationButton.addEventListener("click", function() {
    //     if (navigator.geolocation) {
    //         navigator.geolocation.getCurrentPosition(showPosition, showError);
    //     } else {
    //         alert("Geolocation is not supported by this browser.");
    //     }
    // });

    // function showPosition(position) {
    //     locationInput.value = `Latitude: ${position.coords.latitude}, Longitude: ${position.coords.longitude}`;
    // }

    // function showError(error) {
    //     switch(error.code) {
    //         case error.PERMISSION_DENIED:
    //             alert("User denied the request for Geolocation.");
    //             break;
    //         case error.POSITION_UNAVAILABLE:
    //             alert("Location information is unavailable.");
    //             break;
    //         case error.TIMEOUT:
    //             alert("The request to get user location timed out.");
    //             break;
    //         case error.UNKNOWN_ERROR:
    //             alert("An unknown error occurred.");
    //             break;
    //     }
    // }

    form.addEventListener("submit", function(event) {
        event.preventDefault();

        const specialty = document.getElementById("specialty").value;

        fetch(`/api/v1/filter_doctors?specialty=${specialty}`)
            .then(response => response.json())
            .then(doctors => {
                displayDoctors(doctors);
            })
            .catch(error => {
                console.error('Error:', error);
                alert("Failed to retrieve doctors.");
            });
    });

    function displayDoctors(doctors) {
        const doctorsContainer = document.createElement('div');
        doctorsContainer.classList.add('doctors-container');

        doctors.forEach(doctor => {
            const doctorDiv = document.createElement('div');
            doctorDiv.classList.add('doctor');

            doctorDiv.innerHTML = `
                <h3>${doctor.firstname} ${doctor.lastname}</h3>
                <p>Email: ${doctor.email}</p>
                <p>Specialty: ${doctor.specialty}</p>
                <p>Location: ${doctor.location}</p>
            `;

            doctorsContainer.appendChild(doctorDiv);
        });

        document.body.appendChild(doctorsContainer);
    }
});
