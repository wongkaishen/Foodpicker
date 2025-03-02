import React, { createContext, useState, useContext, useEffect } from 'react';
import axios from 'axios';

// Create axios instance with default config
const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  withCredentials: true,
  xsrfCookieName: 'csrftoken',
  xsrfHeaderName: 'X-CSRFToken',
});

// Function to get CSRF token
const getCSRFToken = async () => {
  try {
    const response = await api.get('/api/csrf/');
    return response.data.csrfToken;
  } catch (error) {
    console.error('Error fetching CSRF token:', error);
    return null;
  }
};

// Add request interceptor to add CSRF token
api.interceptors.request.use(async config => {
  if (!document.cookie.includes('csrftoken')) {
    await getCSRFToken();
  }
  
  const csrfToken = document.cookie
    .split('; ')
    .find(row => row.startsWith('csrftoken='))
    ?.split('=')[1];

  if (csrfToken) {
    config.headers['X-CSRFToken'] = csrfToken;
  }
  
  // Set content type for non-GET requests if not already set
  if (config.method !== 'get' && !config.headers['Content-Type']) {
    config.headers['Content-Type'] = 'application/x-www-form-urlencoded';
  }
  
  return config;
}, error => {
  console.error('Request interceptor error:', error);
  return Promise.reject(error);
});

// Add response interceptor for better error handling
api.interceptors.response.use(
  response => response,
  error => {
    console.error('API Error:', error);
    if (error.response) {
      console.error('Response data:', error.response.data);
      console.error('Response status:', error.response.status);
      console.error('Response headers:', error.response.headers);
    }
    return Promise.reject(error);
  }
);

const AuthContext = createContext(null);

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Check if user is logged in on component mount
    checkAuthStatus();
  }, []);

  const checkAuthStatus = async () => {
    try {
      const response = await api.get('/api/auth/user/');
      if (response.data.user) {
        setUser(response.data.user);
      }
    } catch (error) {
      console.error('Auth check failed:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
      }
    } finally {
      setLoading(false);
    }
  };

  const login = async (username, password) => {
    try {
      // Get CSRF token first
      await api.get('/api/csrf/');
      
      const formData = new URLSearchParams();
      formData.append('username', username);
      formData.append('pass1', password);

      const response = await api.post('/signin', formData);
      
      if (response.data.success) {
        setUser(response.data.user);
        return { success: true };
      }
      
      return {
        success: false,
        error: response.data.message || 'Invalid username or password'
      };
    } catch (error) {
      console.error('Login error:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
      }
      return {
        success: false,
        error: error.response?.data?.message || 'Login failed. Please try again.'
      };
    }
  };

  const logout = async () => {
    try {
      const response = await api.get('/signout');
      if (response.data.success) {
        setUser(null);
        return { success: true };
      }
      return {
        success: false,
        error: response.data.message || 'Logout failed'
      };
    } catch (error) {
      console.error('Logout error:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
      }
      return {
        success: false,
        error: error.response?.data?.message || 'Logout failed'
      };
    }
  };

  const validateRegistration = (userData) => {
    const errors = [];
    
    if (!userData.username || !userData.username.trim()) {
      errors.push('Username is required');
    } else if (userData.username.length > 15) {
      errors.push('Username must be under 15 characters');
    } else if (!/^[a-zA-Z0-9]+$/.test(userData.username)) {
      errors.push('Username must be alphanumeric');
    }

    if (!userData.email || !userData.email.trim()) {
      errors.push('Email is required');
    } else if (!/\S+@\S+\.\S+/.test(userData.email)) {
      errors.push('Invalid email format');
    }

    if (!userData.first_name || !userData.first_name.trim()) {
      errors.push('First name is required');
    }

    if (!userData.last_name || !userData.last_name.trim()) {
      errors.push('Last name is required');
    }

    if (!userData.password || userData.password.length < 8) {
      errors.push('Password must be at least 8 characters long');
    }

    return errors;
  };

  const register = async (userData) => {
    try {
      // Client-side validation
      const validationErrors = validateRegistration(userData);
      if (validationErrors.length > 0) {
        return {
          success: false,
          error: validationErrors.join(', ')
        };
      }

      // Ensure we have a CSRF token
      await getCSRFToken();

      const formData = new URLSearchParams();
      formData.append('username', userData.username);
      formData.append('email', userData.email);
      formData.append('fname', userData.first_name);
      formData.append('lname', userData.last_name);
      formData.append('pass1', userData.password);
      formData.append('pass2', userData.password);

      const response = await api.post('/signup', formData.toString());

      if (response.data.success) {
        return { 
          success: true, 
          message: response.data.message || 'Account created successfully! Please check your email for verification.' 
        };
      }

      return {
        success: false,
        error: response.data.message || 'Registration failed. Please try again.'
      };
    } catch (error) {
      console.error('Registration error:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
        console.error('Response headers:', error.response.headers);
        
        if (error.response.data && error.response.data.message) {
          return {
            success: false,
            error: error.response.data.message
          };
        }
      }
      
      return {
        success: false,
        error: 'Registration failed. Please try again.'
      };
    }
  };

  const value = {
    user,
    loading,
    login,
    logout,
    register,
    isAuthenticated: !!user,
    api
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider');
  }
  return context;
};

export default AuthContext; 