import React from 'react';
import { Container, Typography, Box, TextField, Button, Grid } from '@mui/material';

function Contact() {
  const handleSubmit = (event) => {
    event.preventDefault();
    // Handle form submission here
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ mt: 8, mb: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Contact Us
        </Typography>
        <Typography variant="body1" paragraph>
          Have questions or suggestions? We'd love to hear from you. Send us a message and we'll respond as soon as possible.
        </Typography>
        <Box component="form" onSubmit={handleSubmit} sx={{ mt: 4 }}>
          <Grid container spacing={3}>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                label="Name"
                name="name"
                autoComplete="name"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                required
                fullWidth
                label="Email"
                name="email"
                type="email"
                autoComplete="email"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Subject"
                name="subject"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                required
                fullWidth
                label="Message"
                name="message"
                multiline
                rows={4}
              />
            </Grid>
            <Grid item xs={12}>
              <Button
                type="submit"
                variant="contained"
                color="primary"
                size="large"
              >
                Send Message
              </Button>
            </Grid>
          </Grid>
        </Box>
      </Box>
    </Container>
  );
}

export default Contact; 