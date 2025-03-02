import React, { useState, useEffect } from 'react';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import { Container, Typography, Box, CircularProgress } from '@mui/material';
import axios from 'axios';
import 'leaflet/dist/leaflet.css';
import L from 'leaflet';

// Fix for default marker icon in react-leaflet
delete L.Icon.Default.prototype._getIconUrl;
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png'),
});

function RestaurantMap() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userLocation, setUserLocation] = useState(null);

  useEffect(() => {
    // Get user's location
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (position) => {
          setUserLocation([position.coords.latitude, position.coords.longitude]);
        },
        (error) => {
          console.error('Error getting location:', error);
          setUserLocation([0, 0]); // Default location if geolocation fails
        }
      );
    }

    // Fetch restaurants
    const fetchRestaurants = async () => {
      try {
        const response = await axios.get('http://localhost:8000/api/restaurants/');
        setRestaurants(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching restaurants:', error);
        setLoading(false);
      }
    };

    fetchRestaurants();
  }, []);

  if (loading || !userLocation) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl" sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Restaurant Map
      </Typography>
      <Box sx={{ height: '70vh', width: '100%' }}>
        <MapContainer
          center={userLocation}
          zoom={13}
          style={{ height: '100%', width: '100%' }}
        >
          <TileLayer
            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
          />
          {restaurants.map((restaurant) => (
            restaurant.latitude && restaurant.longitude ? (
              <Marker
                key={restaurant.id}
                position={[restaurant.latitude, restaurant.longitude]}
              >
                <Popup>
                  <Typography variant="h6">{restaurant.name}</Typography>
                  <Typography variant="body2">{restaurant.description}</Typography>
                  <Typography variant="body2">
                    Opening Hours: {restaurant.opentime} - {restaurant.closetime}
                  </Typography>
                  <Typography variant="body2">Price: ${restaurant.price}</Typography>
                </Popup>
              </Marker>
            ) : null
          ))}
        </MapContainer>
      </Box>
    </Container>
  );
}

export default RestaurantMap; 