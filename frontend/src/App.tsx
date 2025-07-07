import { useState } from 'react';
import {
  Container,
  Box,
  Typography,
  TextField,
  Button,
  CircularProgress,
  Paper,
  createTheme,
  ThemeProvider,
  CssBaseline,
} from '@mui/material';
import { motion } from 'framer-motion';

const elegantTheme = createTheme({
  palette: {
    mode: 'dark',
    primary: {
      main: '#6366F1', // A modern indigo
    },
    background: {
      default: '#0B1120', // A deep, dark blue
      paper: 'rgba(17, 25, 40, 0.75)', // A semi-transparent, glassy surface
    },
    text: {
      primary: '#E5E7EB', // Light gray for primary text
      secondary: '#9CA3AF', // Darker gray for secondary text
    },
  },
  typography: {
    fontFamily: 'Inter, sans-serif',
    h1: {
      fontWeight: 900,
    },
    button: {
      textTransform: 'none',
      fontWeight: 'bold',
    },
  },
  components: {
    MuiPaper: {
      styleOverrides: {
        root: {
          border: '1px solid rgba(255, 255, 255, 0.12)',
          backdropFilter: 'blur(16px) saturate(180%)',
          WebkitBackdropFilter: 'blur(16px) saturate(180%)',
          borderRadius: '12px',
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: '8px',
          padding: '10px 20px',
        },
      },
    },
  },
});

function App() {
  const [meetingUrl, setMeetingUrl] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [error, setError] = useState('');

  const handleStartRecording = async () => {
    if (!meetingUrl.startsWith('https://meet.google.com/')) {
      setError('Please enter a valid Google Meet URL.');
      return;
    }
    setError('');
    setIsLoading(true);
    setStatusMessage('Joining the meeting... please wait.');

    await new Promise(resolve => setTimeout(resolve, 3000));

    setIsLoading(false);
    setStatusMessage('Recording has started!');
  };

  return (
    <ThemeProvider theme={elegantTheme}>
      <CssBaseline />
      <Container component="main" maxWidth="md" sx={{ position: 'relative', zIndex: 1 }}>
        <Box
          sx={{
            minHeight: '100vh',
            display: 'flex',
            flexDirection: 'column',
            alignItems: 'center',
            justifyContent: 'center',
            textAlign: 'center',
          }}
        >
          <motion.div
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
          >
            <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 4 }}>
              <Box
                component="img"
                src="/logo.svg"
                alt="WrapUp.AI Logo"
                sx={{ height: '60px', mr: 2 }}
              />
              <Typography component="h1" variant="h2" sx={{ fontWeight: 900 }}>
                WrapUp.AI
              </Typography>
            </Box>
            <Typography variant="h5" color="text.secondary" sx={{ mb: 6, maxWidth: '600px' }}>
              Focus on the conversation, not the notes. You drive the talk, we'll build the doc.
            </Typography>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, scale: 0.95 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.8, delay: 0.4 }}
            style={{ width: '100%' }}
          >
            <Paper elevation={0} sx={{ p: 4, mt: 2 }}>
              <Box component="form" noValidate>
                <TextField
                  fullWidth
                  id="meetingUrl"
                  label="Paste your Google Meet link here"
                  name="meetingUrl"
                  autoFocus
                  value={meetingUrl}
                  onChange={(e) => setMeetingUrl(e.target.value)}
                  disabled={isLoading}
                  error={!!error}
                  helperText={error}
                  sx={{ mb: 2 }}
                />
                <Button
                  type="button"
                  fullWidth
                  variant="contained"
                  size="large"
                  onClick={handleStartRecording}
                  disabled={isLoading}
                >
                  {isLoading ? <CircularProgress size={26} color="inherit" /> : 'Start Recording'}
                </Button>
                {statusMessage && (
                  <Typography color="text.secondary" sx={{ mt: 3 }}>
                    {statusMessage}
                  </Typography>
                )}
              </Box>
            </Paper>
          </motion.div>

          <Box mt={8}>
            <Typography variant="body2" color="text.secondary">
              &copy; {new Date().getFullYear()} WrapUp.AI
            </Typography>
          </Box>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;
