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
         const coords = layer.getLatLngs();
         console.log("Polygon coordinates:", coords); // You can use this data as needed
     });
}

function sendDataToServer(data) {
     fetch('/your-endpoint', {
         method: 'POST',
         headers: {
             'Content-Type': 'application/json',
         },
         body: JSON.stringify(data),
     })
     .then(response => response.json())
     .then(data => console.log('Success:', data))
     .catch((error) => console.error('Error:', error));
 }