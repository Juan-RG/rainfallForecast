

function getUserLocation() {
    if ("geolocation" in navigator) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          const latitude = position.coords.latitude;
          const longitude = position.coords.longitude;
          getCityName(latitude, longitude);
          initMap(latitude, longitude);
        },
        (error) => {
          document.getElementById("locationOutput").textContent = `Error getting location: ${error.message}`;
        }
      );
    } else {
      document.getElementById("locationOutput").textContent = "Geolocation is not supported by this browser.";
    }
  }

  function getCityName(latitude, longitude) {
    const url = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`;

    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        const city = data.address.city || data.address.town || data.address.village;
        //Set the form value in to the actual position
        const locationInput = document.getElementById("actualLocation").value = city;
        locationInput.value = city; 
      })
      .catch((error) => {
        const locationInput = document.getElementById("actualLocation").value = `Error getting city name: ${error.message}`;
      });
  }

  window.onload = getUserLocation;
