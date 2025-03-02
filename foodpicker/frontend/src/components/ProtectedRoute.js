import React from 'react';
import { Navigate, useLocation } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

function ProtectedRoute({ children }) {
  const { isAuthenticated, loading } = useAuth();
  const location = useLocation();

  if (loading) {
    return null; // or a loading spinner
  }

  if (!isAuthenticated) {
    // Redirect to login page with return url
    return <Navigate to="/signin" state={{ from: location }} replace />;
  }

  return children;
}

export default ProtectedRoute; 