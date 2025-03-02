import React, { useEffect, useState } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { CircularProgress, Alert } from '@mui/material';

const VerifyEmail = () => {
  const [searchParams] = useSearchParams();
  const navigate = useNavigate();
  const { api } = useAuth();
  const [status, setStatus] = useState('verifying'); // 'verifying', 'success', 'error'
  const [message, setMessage] = useState('');

  useEffect(() => {
    const verifyEmail = async () => {
      try {
        const uid = searchParams.get('uid');
        const token = searchParams.get('token');

        if (!uid || !token) {
          setStatus('error');
          setMessage('Invalid verification link');
          return;
        }

        const response = await api.post('/api/verify-email/', { uid, token });
        
        if (response.data.success) {
          setStatus('success');
          setMessage('Email verified successfully! Redirecting to home page...');
          setTimeout(() => {
            navigate('/');
          }, 3000);
        } else {
          setStatus('error');
          setMessage(response.data.message || 'Verification failed');
        }
      } catch (error) {
        setStatus('error');
        setMessage(error.response?.data?.message || 'Verification failed');
      }
    };

    verifyEmail();
  }, [searchParams, navigate, api]);

  return (
    <div style={{ 
      display: 'flex', 
      flexDirection: 'column',
      alignItems: 'center',
      justifyContent: 'center',
      minHeight: '60vh',
      padding: '20px'
    }}>
      {status === 'verifying' && (
        <>
          <CircularProgress />
          <p style={{ marginTop: '20px' }}>Verifying your email...</p>
        </>
      )}
      
      {status === 'success' && (
        <Alert severity="success" style={{ marginTop: '20px' }}>
          {message}
        </Alert>
      )}
      
      {status === 'error' && (
        <Alert severity="error" style={{ marginTop: '20px' }}>
          {message}
        </Alert>
      )}
    </div>
  );
};

export default VerifyEmail; 