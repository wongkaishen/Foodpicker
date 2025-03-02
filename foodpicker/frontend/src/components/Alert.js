import React from 'react';
import { Alert as MuiAlert } from '@mui/material';
import { styled } from '@mui/material/styles';

const StyledAlert = styled(MuiAlert)(({ theme }) => ({
  position: 'fixed',
  top: '20px',
  left: '50%',
  transform: 'translateX(-50%)',
  zIndex: 9999,
  minWidth: '300px',
  maxWidth: '90%',
  '@media (max-width: 600px)': {
    width: '90%',
  },
}));

const Alert = ({ message, severity, onClose }) => {
  if (!message) return null;

  return (
    <StyledAlert
      severity={severity}
      onClose={onClose}
      elevation={6}
      variant="filled"
    >
      {message}
    </StyledAlert>
  );
};

export default Alert; 