// Function to fetch location details based on pincode
function fetchLocationDetails(pincode, districtField, stateField) {
    fetch(`https://api.postalpincode.in/pincode/${pincode}`)
        .then(response => response.json())
        .then(data => {
            if (data[0].Status === "Success") {
                const postOffice = data[0].PostOffice[0];
                districtField.value = postOffice.District;
                stateField.value = postOffice.State;
            } else {
                alert('Invalid Pincode');
            }
        })
        .catch(error => {
            console.error('Error fetching location details:', error);
            alert('Error fetching location details');
        });
}

// Event listener for permanent pincode
document.getElementById('permanent_pincode').addEventListener('blur', function () {
    const pincode = this.value;
    const districtField = document.getElementById('permanent_district');
    const stateField = document.getElementById('permanent_state');
    fetchLocationDetails(pincode, districtField, stateField);
});

// Event listener for present pincode
document.getElementById('present_pincode').addEventListener('blur', function () {
    const pincode = this.value;
    const districtField = document.getElementById('present_district');
    const stateField = document.getElementById('present_state');
    fetchLocationDetails(pincode, districtField, stateField);
});
