let map; // Declare the map variable globally

function initMap(latitude, longitude) {

    if (map) {
        return; // If it has, exit the function to avoid reinitialization
    }

    // Initialize the map with the given latitude and longitude
    map = L.map('map').setView([latitude, longitude], 13); 

    // Add OpenStreetMap tile layer
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);
/*
    L.marker([51.5, -0.09]).addTo(map).bindPopup('I am a Type 1 marker!').setStyle({ color: '#ff0000' });
    L.marker([51.51, -0.1]).addTo(map).bindPopup('I am a Type 2 marker!').setStyle({ color: '#00ff00' });
    L.marker([51.49, -0.08]).addTo(map).bindPopup('I am a Type 3 marker!').setStyle({ color: '#0000ff' });
*/

    // Add a marker at the given latitude and longitude
    const marker = L.marker([latitude, longitude]).addTo(map);
    marker.bindPopup('You are here!').openPopup();

     // Set up Leaflet Draw
     const drawnItems = new L.FeatureGroup();
     map.addLayer(drawnItems);
 
     const drawControl = new L.Control.Draw({
         edit: {
             featureGroup: drawnItems // Enable editing of the drawn items
         },
         draw: {
             polygon: {
                 shapeOptions: {
                     color: '#ff0000', // Optional: Set the color of the polygon
                 },
                 showArea: true // Optional: Show the area of the polygon when drawn
             },
             rectangle: true, // Disable rectangle drawing
             polyline: false,   // Disable polyline drawing
             circle: false,     // Disable circle drawing
             marker: false,     // Disable marker drawing
             circlemarker: false,
         }
     });
     map.addControl(drawControl);
 
     // Event listener for when a polygon is drawn
     map.on(L.Draw.Event.CREATED, function (event) {
         const layer = event.layer;
         drawnItems.addLayer(layer); // Add the drawn layer to the FeatureGroup
 
        // Get the coordinates of the drawn polygon
        // Get the outer ring of the polygon
        const coords = layer.getLatLngs()[0];

        // Extract the bounding box coordinates
        let minLat = Infinity, maxLat = -Infinity, minLng = Infinity, maxLng = -Infinity;
        coords.forEach(coord => {
        minLat = Math.min(minLat, coord.lat);
        maxLat = Math.max(maxLat, coord.lat);
        minLng = Math.min(minLng, coord.lng);
        maxLng = Math.max(maxLng, coord.lng);   

        });
        // Get the user's location and selected dataset type from HTML form
        // Should be useful later when we implement function to let user choose datatype,
        // or use point sample for location
        const location = document.getElementById('actualLocation').value;
        const characteristics = document.getElementById('characteristics').value;
        const date = document.getElementById('date').value;
        // Send the data to Django
        const data = {
            minLat: minLat,
            maxLat: maxLat,
            minLng: minLng,
            maxLng: maxLng,
            location: location,
            characteristics: characteristics,
            date: date
        };
        console.log(data)
        sendDataToServer(data);
        
     });
}

// Function to get the CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Check if this cookie string begins with the desired name
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Function to send data to the Django server
async function sendDataToServer(data) {
    try {
        const response = await fetch('/dashboard/', {  // Ensure this URL matches your Django view
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',  // Send data as JSON
                'X-CSRFToken': getCookie('csrftoken'), // Include the CSRF token
            },
            body: JSON.stringify(data), // Convert data object to JSON string
        });

        const responseData = await response.json(); // Parse the JSON response
        console.log('Success:', responseData); // Log the response from the server
        // You can handle the response here (e.g., show a message to the user)
        alert(responseData.message);
    } catch (error) {
        console.error('Error:', error); // Log any errors
    }
}
/*
function sendDataToServer(data) {
    fetch('/dashboard/', { 
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken') // Include the CSRF token
        },
        body: JSON.stringify(data)
    })
    .then(response => response.json()) 
    .then(data => {
        console.log('Success:', data);
        // Handle the response from the server
    })
    .catch((error) => console.error('Error:', error));
 }


 function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue; 

    
}    

*/