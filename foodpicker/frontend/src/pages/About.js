import React from 'react';
import { Container, Typography, Box } from '@mui/material';

function About() {
  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          About FoodPicker
        </Typography>
        <Typography variant="body1" paragraph>
          FoodPicker is your ultimate destination for discovering great restaurants in your area. 
          Our platform helps you find the perfect dining spot based on your location and preferences.
        </Typography>
        <Typography variant="body1" paragraph>
          Whether you're looking for a quick bite or a fine dining experience, 
          FoodPicker makes it easy to explore restaurants, view their locations on a map, 
          and find detailed information about their offerings and operating hours.
        </Typography>
        <Typography variant="body1">
          Join our community to share your favorite restaurants and help others 
          discover great dining experiences in your neighborhood.
        </Typography>
      </Box>
    </Container>
  );
}

export default About; 