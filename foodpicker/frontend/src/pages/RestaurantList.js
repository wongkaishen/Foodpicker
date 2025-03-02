import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Grid,
  Card,
  CardContent,
  CardMedia,
  Typography,
  CardActionArea,
  CircularProgress,
  Box,
} from '@mui/material';
import axios from 'axios';

function RestaurantList() {
  const [restaurants, setRestaurants] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
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

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" component="h1" gutterBottom>
        Restaurants
      </Typography>
      <Grid container spacing={3}>
        {restaurants.map((restaurant) => (
          <Grid item xs={12} sm={6} md={4} key={restaurant.id}>
            <Card>
              <CardActionArea onClick={() => navigate(`/restaurants/${restaurant.id}`)}>
                <CardMedia
                  component="img"
                  height="140"
                  image={`https://source.unsplash.com/400x300/?restaurant,food&${restaurant.id}`}
                  alt={restaurant.name}
                />
                <CardContent>
                  <Typography gutterBottom variant="h5" component="div">
                    {restaurant.name}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    {restaurant.description.slice(0, 100)}...
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                    Opening Hours: {restaurant.opentime} - {restaurant.closetime}
                  </Typography>
                  <Typography variant="body2" color="primary" sx={{ mt: 1 }}>
                    ${restaurant.price}
                  </Typography>
                </CardContent>
              </CardActionArea>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Container>
  );
}

export default RestaurantList; 