# NuxAI Backend

FastAPI-based backend for NuxAI voice assistant.

## Features

- 🎤 Offline wake word detection using Vosk
- ⚡ Real-time WebSocket communication
- 🔧 System command execution
- 🚀 Fast and lightweight with FastAPI

## Setup

### 1. Install Python Dependencies

```bash
cd backend
pip install -r requirements.txt
```

### 2. Install System Dependencies (Linux)

```bash
# For PyAudio
sudo apt-get install portaudio19-dev python3-pyaudio

# For screenshot support
sudo apt-get install gnome-screenshot
```

### 3. Download Voice Model (Optional)

For full wake word detection, download the Vosk model:

```bash
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
cd ..
```

Note: The backend will work in demo mode without the model.

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env if needed
```

## Running

```bash
python main.py
```

The backend will start on http://127.0.0.1:8000

## API Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /api/status` - Detailed status
- `WS /ws/overlay` - WebSocket for overlay communication

## Development

```bash
# Run with auto-reload
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

