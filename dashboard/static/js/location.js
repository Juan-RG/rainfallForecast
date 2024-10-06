

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

  async function getCityName(latitude, longitude) {
    const cachedCity = localStorage.getItem("userCity");
    if (cachedCity) {
      document.getElementById("actualLocation").value = cachedCity;
      return;
    }
  
    const url = `https://nominatim.openstreetmap.org/reverse?lat=${latitude}&lon=${longitude}&format=json`;
    try {
      document.getElementById("actualLocation").value = "Loading location...";
      const response = await fetch(url);
      const data = await response.json();
      const city = data.address.city || data.address.town || data.address.village;
      document.getElementById("actualLocation").value = city;
      localStorage.setItem("userCity", city); // Cache the city
    } catch (error) {
      document.getElementById("actualLocation").value = `Error: ${error.message}`;
    }
  }
  window.onload = getUserLocation;

