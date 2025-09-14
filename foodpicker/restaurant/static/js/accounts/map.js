// Initialize Google Map
let map;

function initMap() {
    // Initialize the map at a default location and zoom level
    map = new google.maps.Map(document.getElementById('map'), {
        zoom: 2,
        center: { lat: 0, lng: 0 }, // Start with a global view
        mapTypeControl: false,
        streetViewControl: false,
        fullscreenControl: false
    });

    // Check if there are any restaurants to display
    if (restaurants.length > 0) {
        const bounds = new google.maps.LatLngBounds();

        // Loop through each restaurant and add a marker
        restaurants.forEach(function (restaurant) {
            // Check if latitude and longitude are valid
            if (!isNaN(restaurant.latitude) && !isNaN(restaurant.longitude)) {
                // Create a marker at the restaurant's location
                const marker = new google.maps.Marker({
                    position: { lat: restaurant.latitude, lng: restaurant.longitude },
                    map: map,
                    title: restaurant.name,
                    icon: {
                        path: google.maps.SymbolPath.CIRCLE,
                        scale: 10,
                        fillColor: "#04AA6D",
                        fillOpacity: 1,
                        strokeColor: "#ffffff",
                        strokeWeight: 3
                    }
                });

                // Add an info window to the marker with restaurant details
                const infoWindow = new google.maps.InfoWindow({
                    content: '<b>' + restaurant.name + '</b><br>' + restaurant.description
                });

                marker.addListener('click', () => {
                    infoWindow.open(map, marker);
                });

                // Extend the map bounds to include this marker
                bounds.extend(new google.maps.LatLng(restaurant.latitude, restaurant.longitude));
            } else {
                console.error('Invalid coordinates for restaurant:', restaurant.name);
            }
        });

        // Adjust the map view to fit all the markers
        map.fitBounds(bounds);
    } else {
        console.log("No restaurants available to display.");
    }
}

// Make initMap available globally for Google Maps callback
window.initMap = initMap;
