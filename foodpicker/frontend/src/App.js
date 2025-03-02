import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { CacheProvider } from '@emotion/react';
import createCache from '@emotion/cache';
import { AuthProvider } from './contexts/AuthContext';
import ProtectedRoute from './components/ProtectedRoute';
import Navbar from './components/Navbar';
import Home from './pages/Home';
import About from './pages/About';
import Contact from './pages/Contact';
import RestaurantList from './pages/RestaurantList';
import RestaurantDetail from './pages/RestaurantDetail';
import RestaurantMap from './pages/RestaurantMap';
import SignIn from './pages/SignIn';
import SignUp from './pages/SignUp';
import AddRestaurant from './pages/AddRestaurant';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
  },
});

// Create emotion cache
const cache = createCache({
  key: 'css',
  prepend: true,
});

function App() {
  return (
    <CacheProvider value={cache}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <AuthProvider>
          <Router>
            <Navbar />
            <Routes>
              <Route path="/" element={<Home />} />
              <Route path="/about" element={<About />} />
              <Route path="/contact" element={<Contact />} />
              <Route path="/restaurants" element={<RestaurantList />} />
              <Route path="/restaurants/:id" element={<RestaurantDetail />} />
              <Route path="/map" element={<RestaurantMap />} />
              <Route path="/signin" element={<SignIn />} />
              <Route path="/signup" element={<SignUp />} />
              <Route
                path="/add-restaurant"
                element={
                  <ProtectedRoute>
                    <AddRestaurant />
                  </ProtectedRoute>
                }
              />
            </Routes>
          </Router>
        </AuthProvider>
      </ThemeProvider>
    </CacheProvider>
  );
}

export default App;
