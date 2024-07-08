// // Function to fetch doctors based on specialty
// function fetchDoctorsBySpecialty(specialty) {
//     const url = `http://yourapi.com/api/v1/views/filter_doctors?specialty=${encodeURIComponent(specialty)}`;
  
//     fetch(url)
//       .then(response => {
//         if (!response.ok) {
//           throw new Error(`Network response was not ok: ${response.statusText}`);
//         }
//         return response.json();
//       })
//       .then(data => {
//         console.log(data); // Handle the data, e.g., update the UI
//       })
//       .catch(error => {
//         console.error('There was a problem with the fetch operation:', error);
//       });
//   }
  
//   // Example usage
//   fetchDoctorsBySpecialty('Cardiology');


$(document).ready(function () {
    const api = 'http://' + window.location.hostname;

    // Check API status
    $.get(api + ':5001/api/v1/status/', function (response) {
        if (response.status === 'OK') {
            $('DIV#api_status').addClass('available');
        } else {
            $('DIV#api_status').removeClass('available');
        }
    });

    // Initial search for all doctors
    $.ajax({
        url: api + ':5001/api/v1/doctors/',
        type: 'GET',
        dataType: 'json',
        success: appendDoctors
    });

    let specializations = {};
    $('.specializations INPUT[type="checkbox"]').change(function () {
        if ($(this).is(':checked')) {
            specializations[$(this).attr('data-id')] = $(this).attr('data-name');
        } else {
            delete specializations[$(this).attr('data-id')];
        }
        if (Object.values(specializations).length === 0) {
            $('.specializations H4').html('&nbsp;');
        } else {
            $('.specializations H4').text(Object.values(specializations).join(', '));
        }
    });

    $('BUTTON').click(function () {
        $.ajax({
            url: api + ':5001/api/v1/doctors_search/',
            type: 'POST',
            data: JSON.stringify({
                'specializations': Object.keys(specializations)
            }),
            contentType: 'application/json',
            dataType: 'json',
            success: appendDoctors
        });
    });
});

function appendDoctors(data) {
    $('SECTION.places').empty();
    $('SECTION.places').append(data.map(doctor => {
        return `<ARTICLE>
                  <DIV class="title">
                    <H2>${doctor.name}</H2>
                    <DIV class="specialization">
                      ${doctor.specialization}
                    </DIV>
                  </DIV>
                  <DIV class="information">
                    <DIV class="experience">
                      <I class="fa fa-briefcase fa-3x" aria-hidden="true"></I>
                      </BR>
                      ${doctor.years_experience} Years Experience
                    </DIV>
                    <DIV class="availability">
                      <I class="fa fa-calendar fa-3x" aria-hidden="true"></I>
                      </BR>
                      Available: ${doctor.availability}
                    </DIV>
                  </DIV>
                  <DIV class="description">
                    ${doctor.description}
                  </DIV>
                </ARTICLE>`;
    }));
}
