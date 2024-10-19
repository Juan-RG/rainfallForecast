let map; // Declare the map variable globally
let lastDrawnLayer = null; // Variable to hold the last drawn shape
let drawnLayers = []; // Array to hold all the drawn layers
let idLayer = 0;

function initMap(latitude, longitude) {
    // Prevent reinitialization of the map
    if (map) {
        return;
    }

    // Create and set the map's view 
    map = L.map('map').setView([latitude, longitude], 13); 
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', { maxZoom: 19 }).addTo(map);

    // Add a custom legend to the map
    addLegendToMap();

    // Add a marker at the given location
    const marker = L.marker([latitude, longitude]).addTo(map);
    marker.bindPopup('Your location').openPopup();

    // Initialize the drawing feature for polygons
    initializeDrawFeature();
}

function addLegendToMap() {
    const legend = L.control({ position: 'topright' });

    legend.onAdd = function () {
        const div = L.DomUtil.create('div', 'info legend');
        div.innerHTML =
         `
            <h4>Rainfall Probability</h4>
            <div class="legend-item"><span class="legend-color" style="background-color: #ff0000;"></span> High</div>
            <div class="legend-item"><span class="legend-color" style="background-color: #ffff00;"></span> Medium</div>
            <div class="legend-item"><span class="legend-color" style="background-color: #00ff00;"></span> Low</div>
        `;
        return div;
    };

    legend.addTo(map);
}

function initializeDrawFeature() {
    const drawnItems = new L.FeatureGroup();
    map.addLayer(drawnItems);

    const drawControl = new L.Control.Draw({
        edit: { featureGroup: drawnItems },
        draw: {
            polygon: {
                shapeOptions: { color: '#ff0000' },
                showArea: true
            },
            rectangle: true,
            polyline: false,
            circle: false,
            marker: false,
            circlemarker: false
        }
    });

    map.addControl(drawControl);

    // Event listener for when a polygon is drawn
    map.on(L.Draw.Event.CREATED, function (event) {
        const layer = event.layer;
        idLayer = Math.random(); // Assign a random ID to the layer

        drawnLayers.push({ id: idLayer, layer: layer }); // Add to drawn layers array
        drawnItems.addLayer(layer); // Add layer to the feature group

        handlePolygonDraw(layer);
    });
}

function handlePolygonDraw(layer) {
    const coords = layer.getLatLngs()[0];

    let minLat = Infinity, maxLat = -Infinity, minLng = Infinity, maxLng = -Infinity;
    coords.forEach(coord => {
        minLat = Math.min(minLat, coord.lat);
        maxLat = Math.max(maxLat, coord.lat);
        minLng = Math.min(minLng, coord.lng);
        maxLng = Math.max(maxLng, coord.lng);
    });

    const location = document.getElementById('actualLocation').value;
    const date = document.getElementById('date').value;

    const data = {
        id: idLayer,
        minLat: minLat,
        maxLat: maxLat,
        minLng: minLng,
        maxLng: maxLng,
        location: location,
        characteristics: '', // Placeholder for future use
        date: date
    };

    console.log(data);
    sendDataToServer(data); // Sends data to the backend
}

// Function to get the CSRF token from cookies
function getCookie(name) {
    const cookies = document.cookie.split(';').map(cookie => cookie.trim());
    const targetCookie = cookies.find(cookie => cookie.startsWith(`${name}=`));
    return targetCookie ? decodeURIComponent(targetCookie.split('=')[1]) : null;
}

async function sendDataToServer(data) {
    const url = '/dashboard/';  // Ensure this matches your Django view
    const csrfToken = getCookie('csrftoken');
    
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken,
            },
            body: JSON.stringify(data),
        });

        // Check if the response is ok (status 200-299)
        if (!response.ok) {
            throw new Error(`Server error: ${response.status} ${response.statusText}`);
        }

        const responseData = await response.json(); // Parse the JSON response
        console.log('Success:', responseData);

        // Update map or UI with server response
        modifyMap(responseData); 
    } catch (error) {
        handleError(error, data.id);
    }
}

function handleError(error, layerId) {
    console.error('Error:', error);

    // Attempt to remove the layer from the map
    const layerToRemove = drawnLayers.find(item => item.id === layerId);
    if (layerToRemove) {
        map.removeLayer(layerToRemove.layer);
    } else {
        console.warn(`Layer with ID ${layerId} not found`);
    }
}

// Function to modify the map based on the server response
function modifyMap(responseData) {
    const { newColor, labelText } = getColorAndLabel(responseData.result);
    
    // Find the corresponding drawn layer by ID
    const targetLayer = drawnLayers.find(item => item.id === responseData.id)?.layer;

    if (targetLayer) {
        // Change the color of the target layer
        targetLayer.setStyle({ color: newColor });

        // Calculate the center of the polygon
        const latLngs = targetLayer.getLatLngs()[0];
        const center = getPolygonCenter(latLngs);

        // Create and place the label marker on the map
        addLabelToMap(center, labelText);
    } else {
        console.error("Layer with ID " + responseData.id + " not found.");
    }
}

// Function to get the color and label text based on the result value
function getColorAndLabel(result) {
    if (result < 1) {
        return { newColor: '#00ff00', labelText: "Low probability" };
    } else if (result < 2) {
        return { newColor: '#ffff00', labelText: "Average probability" };
    } else {
        return { newColor: '#ff0000', labelText: "High probability" };
    }
}

// Function to add a label marker to the map
function addLabelToMap(center, labelText) {
    const labelIcon = L.divIcon({
        className: 'text-label', // Custom class for styling
        html: `<div style="color: black; font-weight: bold;">${labelText}</div>`, // Your text
        iconSize: [100, 40], // Adjust the size as needed
        iconAnchor: [50, 20] // Center the icon on the label position
    });

    // Create a marker with the custom icon at the polygon center
    L.marker(center, { icon: labelIcon }).addTo(map);
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
