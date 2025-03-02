import React, { useState, useEffect } from 'react';
import { useParams } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  Card,
  CardMedia,
  CircularProgress,
  Grid,
  Paper,
} from '@mui/material';
import axios from 'axios';
import { MapContainer, TileLayer, Marker, Popup } from 'react-leaflet';
import 'leaflet/dist/leaflet.css';

function RestaurantDetail() {
  const { id } = useParams();
  const [restaurant, setRestaurant] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchRestaurant = async () => {
      try {
        const response = await axios.get(`http://localhost:8000/api/restaurants/${id}/`);
        setRestaurant(response.data);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching restaurant:', error);
        setLoading(false);
      }
    };

    fetchRestaurant();
  }, [id]);

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!restaurant) {
    return (
      <Container>
        <Typography variant="h5" sx={{ mt: 4 }}>
          Restaurant not found
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Grid container spacing={4}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardMedia
              component="img"
              height="300"
              image={`https://source.unsplash.com/800x600/?restaurant,food&${restaurant.id}`}
              alt={restaurant.name}
            />
          </Card>
          <Box sx={{ mt: 3 }}>
            <Typography variant="h4" gutterBottom>
              {restaurant.name}
            </Typography>
            <Typography variant="body1" paragraph>
              {restaurant.description}
            </Typography>
            <Typography variant="h6" gutterBottom>
              Details
            </Typography>
            <Paper sx={{ p: 2 }}>
              <Typography variant="body1">
                Price: ${restaurant.price}
              </Typography>
              <Typography variant="body1">
                Opening Hours: {restaurant.opentime} - {restaurant.closetime}
              </Typography>
              <Typography variant="body1">
                Address: {restaurant.street_address}, {restaurant.city}, {restaurant.state} {restaurant.postal_code}
              </Typography>
            </Paper>
          </Box>
        </Grid>
        <Grid item xs={12} md={6}>
          {restaurant.latitude && restaurant.longitude && (
            <Box sx={{ height: '400px', width: '100%' }}>
              <MapContainer
                center={[restaurant.latitude, restaurant.longitude]}
                zoom={15}
                style={{ height: '100%', width: '100%' }}
              >
                <TileLayer
                  url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                  attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                />
                <Marker position={[restaurant.latitude, restaurant.longitude]}>
                  <Popup>
                    <Typography variant="body1">{restaurant.name}</Typography>
                  </Popup>
                </Marker>
              </MapContainer>
            </Box>
          )}
        </Grid>
      </Grid>
    </Container>
  );
}

export default RestaurantDetail; 