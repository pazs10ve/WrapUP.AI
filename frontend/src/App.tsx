import { useState, useRef } from 'react';
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
  const [ownerEmail, setOwnerEmail] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [statusMessage, setStatusMessage] = useState('');
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const meetWindowRef = useRef<Window | null>(null);
  const [error, setError] = useState('');

    const handleStartRecording = async () => {
    const emailValid = /.+@.+\..+/.test(ownerEmail);
    if (!meetingUrl || !meetingUrl.startsWith('https://meet.google.com/')) {
      setError('Please enter a valid Google Meet link.');
      return;
    }
    if (!emailValid) {
      setError('Please enter a valid email address.');
      return;
    }

    setIsLoading(true);
    setError('');
    setStatusMessage('Opening meeting tab...');

    const meetWindow = window.open(meetingUrl, '_blank');
    meetWindowRef.current = meetWindow;
    if (!meetWindow) {
      setIsLoading(false);
      setError('Popup blocked. Please allow pop-ups for this site.');
      return;
    }

    // Give the tab a moment to load before asking the user to pick it.
    setTimeout(async () => {
      try {
        setStatusMessage('Please choose the Meet tab and click "Share" to start capture.');
        // Ask for tab (or window) capture with audio.
        // Chrome will show built-in picker.
        // @ts-ignore – preferCurrentTab is non-standard but most browsers ignore it.
        const stream = await navigator.mediaDevices.getDisplayMedia({
          video: true,
          audio: true,
        });
        // We only need audio; turn off video tracks to save bandwidth.
        stream.getVideoTracks().forEach(t => t.stop());

        const mediaRecorder = new MediaRecorder(stream, { mimeType: 'audio/webm' });
        mediaRecorderRef.current = mediaRecorder;
        mediaRecorder.ondataavailable = async (evt) => {
          if (evt.data.size) {
            const arrayBuffer = await evt.data.arrayBuffer();
            const meetCode = new URL(meetingUrl).pathname.split('/')[1];
            await fetch('/api/record-chunk', {
              method: 'POST',
              headers: { 'Content-Type': 'application/octet-stream', 'x-meet-code': meetCode },
              body: arrayBuffer,
            });
          }
        };
        const stopCleanup = async () => {
          setIsRecording(false);
          setStatusMessage('Recording finished. Uploading for processing...');
          meetWindowRef.current?.close();

          const meetingCode = new URL(meetingUrl).pathname.split('/')[1];

          // First, ensure the owner's email is logged
          await fetch('/api/owner-email', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ meetingCode, email: ownerEmail }),
          });

          // Now, trigger the final processing
          console.log(`[App.tsx] Calling /api/record-finish for meeting code: ${meetingCode}`);
          const response = await fetch('/api/record-finish', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ 
              meetingCode,
              meetLink: meetingUrl,
              ownerEmail
            }),
          });

          if (response.ok) {
            setStatusMessage('Processing complete! Your summary will be emailed shortly.');
          } else {
            const errorData = await response.json();
            setError(`Processing failed: ${errorData.detail || 'Unknown error'}`);
            setStatusMessage('There was an error processing your meeting.');
          }
        };
        mediaRecorder.onstop = stopCleanup;
        stream.getAudioTracks()[0].addEventListener('ended', () => {
          if (mediaRecorder.state !== 'inactive') mediaRecorder.stop();
        });
        mediaRecorder.start(1000); // 1-second chunks
        setStatusMessage('Recording... (click Stop when done)');
        setIsRecording(true);
        setIsLoading(false);

        // Poll for window closed
        const winInterval = setInterval(() => {
          if (meetWindowRef.current && meetWindowRef.current.closed) {
            clearInterval(winInterval);
            if (mediaRecorder.state !== 'inactive') mediaRecorder.stop();
          }
        }, 1000);

        // Expose stop function
        (window as any).stopWrapupRecording = () => {
          if (mediaRecorder.state !== 'inactive') mediaRecorder.stop();
        };
      } catch (err: any) {
        setIsLoading(false);
        setError(err.message || 'Capture cancelled.');
        setStatusMessage('');
        meetWindow.close();
      }
    }, 1500);
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
                            <Box component="form" noValidate onSubmit={(e) => { e.preventDefault(); handleStartRecording(); }}>
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
                <TextField
                  fullWidth
                  id="ownerEmail"
                  label="Your email (to receive summary)"
                  value={ownerEmail}
                  onChange={(e) => setOwnerEmail(e.target.value)}
                  disabled={isLoading || isRecording}
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
                <Button
                  sx={{ mt: 2 }}
                  fullWidth
                  variant="outlined"
                  color="secondary"
                  disabled={!isRecording}
                  onClick={() => (window as any).stopWrapupRecording?.()}
                >
                  Stop Recording
                </Button>

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
