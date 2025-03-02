import React from 'react';
import { Container, Typography, Box, Button } from '@mui/material';
import { useNavigate } from 'react-router-dom';

function Home() {
  const navigate = useNavigate();

  return (
    <Container maxWidth="md">
      <Box
        sx={{
          mt: 8,
          display: 'flex',
          flexDirection: 'column',
          alignItems: 'center',
          textAlign: 'center',
        }}
      >
        <Typography variant="h2" component="h1" gutterBottom>
          Welcome to FoodPicker
        </Typography>
        <Typography variant="h5" component="h2" gutterBottom color="text.secondary">
          Find the perfect restaurant near you
        </Typography>
        <Box sx={{ mt: 4, display: 'flex', gap: 2 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            onClick={() => navigate('/map')}
          >
            Find Restaurants Near Me
          </Button>
          <Button
            variant="outlined"
            color="primary"
            size="large"
            onClick={() => navigate('/restaurants')}
          >
            Browse All Restaurants
          </Button>
        </Box>
      </Box>
    </Container>
  );
}

export default Home; 