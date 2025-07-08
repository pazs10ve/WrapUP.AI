# WrapUp.AI - AI-Powered Meeting Summarizer

WrapUp.AI is a full-stack web application designed to automatically record, transcribe, summarize, and document your Google Meet calls. Focus on the conversation, not on taking notes—we handle the rest.

## Features

- **One-Click Recording:** Simply paste a Google Meet link to open and start recording the meeting in a new tab.
- **Screen & Audio Capture:** Captures the meeting's audio directly from the browser.
- **AI-Powered Transcription:** Utilizes AssemblyAI for fast and accurate speech-to-text transcription.
- **Intelligent Summarization:** Leverages Google's Gemini API to generate concise summaries, key discussion points, and actionable items.
- **Email Delivery:** Automatically sends the summary and full transcript to your email address using Brevo (Sendinblue).
- **Modern, Responsive UI:** A clean and intuitive user interface built with React and Material-UI.

## Architecture

The application is built with a modern, decoupled architecture:

1.  **Frontend (React/Vite):** A single-page application that provides the user interface for starting recordings. It captures the screen/tab audio and sends it to the Next.js backend.
2.  **Backend API Layer (Next.js):** Acts as a proxy and handles file uploads from the frontend. It receives the recorded audio chunks, assembles them, and forwards the complete file to the FastAPI backend for processing.
3.  **AI Backend (Python/FastAPI):** The core processing engine. It receives the audio file, orchestrates calls to AssemblyAI for transcription and Google Gemini for summarization, sends the final summary via email, and logs meeting metadata to a database.
4.  **Database (SQLite):** A lightweight database to store metadata about each processed meeting.

## Tech Stack

**Frontend:**
- React (with Vite)
- TypeScript
- Material-UI
- Axios

**Backend (API Layer):**
- Next.js
- TypeScript

**Backend (AI Processing):**
- Python 3.12
- FastAPI
- AssemblyAI API
- Google Gemini API
- Brevo (Sendinblue) API
- Pydub & PyAudio for audio manipulation

**Deployment:**
- **Frontend:** Netlify
- **Next.js Backend:** Render
- **FastAPI Backend:** Render (using Docker)
- **Containerization:** Docker

## Project Structure

```
.
├── backend/         # Next.js Backend (API Layer)
├── frontend/        # React Frontend (UI)
├── app.py           # FastAPI application entrypoint
├── transcribe.py    # Transcription logic
├── summarize.py     # Summarization logic
├── send_email.py    # Email sending logic
├── Dockerfile       # Docker configuration for FastAPI backend
├── requirements.txt # Python dependencies
└── ...
```

## Setup for Local Development

### Prerequisites
- Node.js and npm
- Python 3.12+ and pip
- `ffmpeg` installed on your system

### 1. Clone the Repository

```bash
git clone https://github.com/pazs10ve/WrapUP.AI.git
cd WrapUP.AI
```

### 2. Configure Environment Variables

You will need to create `.env` files for both the frontend and the Python backend.

- **Python Backend:** Create a file named `.env` in the root directory.
  ```
  GEMINI_API_KEY="YOUR_GEMINI_API_KEY"
  ASSEMBLYAI_API_KEY="YOUR_ASSEMBLYAI_API_KEY"
  BREVO_API_KEY="YOUR_BREVO_API_KEY"
  ```

- **Frontend:** Create a file named `.env` in the `frontend/` directory.
  ```
  VITE_API_URL=http://localhost:3000
  ```

### 3. Install Dependencies

```bash
# Install Python dependencies
pip install -r requirements.txt

# Install Next.js backend dependencies
cd backend
npm install
cd ..

# Install React frontend dependencies
cd frontend
npm install
cd ..
```

### 4. Run the Application

Open three separate terminals:

- **Terminal 1: Run FastAPI Backend**
  ```bash
  uvicorn app:app --host 0.0.0.0 --port 8001
  ```

- **Terminal 2: Run Next.js Backend**
  ```bash
  cd backend
  npm run dev
  ```

- **Terminal 3: Run React Frontend**
  ```bash
  cd frontend
  npm run dev
  ```

Navigate to the URL provided by the frontend terminal (usually `http://localhost:5173`) to use the application.

## Deployment

The application is deployed across two services:

- **Render:** Hosts the FastAPI backend (via Docker) and the Next.js backend.
- **Netlify:** Hosts the static React frontend.

Pushing to the `main` branch will automatically trigger new deployments on both platforms based on their respective configurations.
