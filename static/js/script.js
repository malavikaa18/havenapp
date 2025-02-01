document.getElementById('emergency-call-btn').addEventListener('click', function() {
    window.location.href = 'tel:112'; // Use a generic emergency number or predefined contact
});

document.getElementById('alert-btn').addEventListener('click', function() {
    // Get the user's location using geolocation
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        // Send SOS alert to backend
        fetch('/send_sos', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                user_email: 'user@example.com', // Example user email, replace with actual login system
                latitude: latitude,
                longitude: longitude
            })
        })
        .then(response => response.json())
        .then(data => {
            document.getElementById('status').innerText = data.message;
        })
        .catch(error => {
            console.error('Error:', error);
        });
    });
});

document.getElementById('get-location-btn').addEventListener('click', function() {
    // Get the current location
    navigator.geolocation.getCurrentPosition(function(position) {
        const latitude = position.coords.latitude;
        const longitude = position.coords.longitude;

        document.getElementById('location').innerText = `${latitude}, ${longitude}`;
    });
});
