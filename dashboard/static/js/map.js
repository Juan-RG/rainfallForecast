let map; // Declare the map variable globally
let lastDrawnLayer = null; // Variable to hold the last drawn shape

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
         lastDrawnLayer = layer; // Store the last drawn layer
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
        //const characteristics = document.getElementById('characteristics').value;
        const date = document.getElementById('date').value;
        // Send the data to Django
        const data = {
            minLat: minLat,
            maxLat: maxLat,
            minLng: minLng,
            maxLng: maxLng,
            location: location,
            characteristics: '',
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
        modifyMap(responseData)
    } catch (error) {
        console.error('Error:', error); // Log any errors
    }
}

// Function to get the CSRF token from cookies
function modifyMap(responseData) {
    newColor = ''
    labelText = ""
    
    if (responseData.result < 1){
        newColor = '#00ff00'
        labelText = "Low probability"
    } else if (responseData.result < 2){
        newColor = '#ffff00'
        labelText = "Average probability"
    }else{
        newColor = '#ff0000'
        labelText = "High probability"
    }

    if (lastDrawnLayer) {
        // Change the color of the last drawn layer
        lastDrawnLayer.setStyle({ color: newColor });

        // Calculate the center of the polygon for placing the label
        const latLngs = lastDrawnLayer.getLatLngs()[0];
        const center = getPolygonCenter(latLngs);
        // Create a custom div icon for the label
        const labelIcon = L.divIcon({
            className: 'text-label', // Custom class for styling
            html: '<div style="color: black; font-weight: bold;">' + labelText + '</div>', // Your text
            iconSize: [100, 40], // Adjust the size as needed
            iconAnchor: [50, 20] // Center the icon on the label position
        });

        // Create a marker with the custom icon at the polygon center
        L.marker(center, { icon: labelIcon }).addTo(map);
        /*
        // Create a marker with the label
        const labelMarker = L.marker(center).addTo(map);
        labelMarker.bindPopup(labelText).openPopup(); // Add a popup with the text
*/
    } else {
        console.log("No shape has been drawn yet.");
    }
}

// Function to calculate the centroid of a polygon
function getPolygonCenter(latLngs) {
    let latSum = 0, lngSum = 0;

    latLngs.forEach(latLng => {
        latSum += latLng.lat;
        lngSum += latLng.lng;
    });

    return L.latLng(latSum / latLngs.length, lngSum / latLngs.length);
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