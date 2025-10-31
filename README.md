# 🎤 NuxAI - Intelligent Cross-Platform Voice Assistant

<div align="center">

**An offline, privacy-focused voice assistant for Linux desktops**

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/yourusername/nuxai)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/flutter-3.0+-02569B.svg)](https://flutter.dev/)

</div>

---

## 📋 Overview

NuxAI is a native desktop voice assistant that brings voice interaction to Linux, working entirely offline with no cloud dependencies. Activate it with a wake word, see a beautiful visual overlay, and execute commands hands-free.

### ✨ Key Features

- 🎙️ **Offline Wake Word Detection** - Uses Vosk for local voice recognition
- 🖥️ **Sleek Visual Overlay** - Modern, transparent Flutter UI
- ⚡ **Fast Command Execution** - Open apps, take screenshots, get system info
- 🔒 **Privacy-First** - All processing happens on your machine
- 🚀 **FastAPI Backend** - High-performance Python server
- 📡 **Real-time Communication** - WebSocket-based frontend/backend sync

## 🏗️ Architecture

```
nuxai/
├── backend/          # Python FastAPI backend
│   ├── api/          # API routes & WebSocket handlers
│   ├── core/         # Wake word detection, voice processing, commands
│   ├── utils/        # Logging and utilities
│   └── main.py       # Application entry point
│
└── overlay/          # Flutter overlay UI
    ├── lib/
    │   ├── screens/  # Main overlay screen
    │   ├── widgets/  # UI components
    │   ├── services/ # WebSocket service
    │   └── models/   # State models
    └── pubspec.yaml
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.8+**
- **Flutter 3.0+** (for overlay)
- **Linux** (Ubuntu/Debian/Fedora/Arch)
- **PortAudio** (for microphone access)

### Installation

#### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/nuxai.git
cd nuxai
```

#### 2. Set Up Backend

```bash
cd backend

# Install system dependencies (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install -y portaudio19-dev python3-pyaudio gnome-screenshot

# Install Python dependencies
pip install -r requirements.txt

# Optional: Download Vosk model for better accuracy
mkdir -p models
cd models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
cd ../..
```

#### 3. Set Up Overlay

```bash
cd overlay

# Install Flutter if not already installed
# Visit: https://docs.flutter.dev/get-started/install/linux

# Enable Linux desktop support
flutter config --enable-linux-desktop

# Install system dependencies (Ubuntu/Debian)
sudo apt-get install -y clang cmake ninja-build pkg-config libgtk-3-dev

# Get Flutter dependencies
flutter pub get
cd ..
```

### Running NuxAI

#### Terminal 1: Start Backend

```bash
cd backend
python main.py
```

Backend will start on `http://127.0.0.1:8000`

#### Terminal 2: Start Overlay

```bash
cd overlay
flutter run -d linux
```

## 🎯 Usage

1. **Start the backend** - It will begin listening for wake words
2. **Start the overlay** - The UI connects to the backend via WebSocket
3. **Say "Computer" or "Hey Nux"** - The overlay appears
4. **Speak your command** - e.g., "open browser", "take screenshot"
5. **Watch it execute** - The overlay shows the result

### Supported Commands (v0.1)

| Command | Action |
|---------|--------|
| "open browser" | Opens default web browser |
| "take screenshot" | Captures screen to Pictures/Screenshots |
| "what time is it" | Displays current time |
| "open terminal" | Opens terminal window |
| "open file manager" | Opens file browser |
| "open calculator" | Opens calculator app |

## 🛠️ Configuration

### Backend Configuration

Edit `backend/.env` (create from `.env.example`):

```env
HOST=127.0.0.1
PORT=8000
SAMPLE_RATE=16000
```

### Overlay Configuration

Edit WebSocket URL in `overlay/lib/services/websocket_service.dart`:

```dart
static const String wsUrl = 'ws://127.0.0.1:8000/ws/overlay';
```

## 📡 API Documentation

Once the backend is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

### Key Endpoints

- `GET /` - Root endpoint
- `GET /api/health` - Health check
- `GET /api/status` - Detailed status
- `WS /ws/overlay` - WebSocket for overlay communication

## 🔧 Development

### Backend Development

```bash
cd backend

# Run with auto-reload
uvicorn main:app --reload

# Run tests (when available)
pytest
```

### Overlay Development

```bash
cd overlay

# Hot reload
flutter run -d linux

# Build release
flutter build linux --release
```

## 🐛 Troubleshooting

### Microphone Not Working

```bash
# Test microphone
arecord -l

# Adjust permissions
sudo usermod -a -G audio $USER
```

### No Wake Word Detection

- Download the Vosk model (see Installation step 2)
- Check microphone input levels
- Verify PortAudio installation

### Overlay Not Connecting

- Ensure backend is running on port 8000
- Check firewall settings
- Verify WebSocket URL in overlay config

## 🗺️ Roadmap

### v0.2
- [ ] Better wake word accuracy
- [ ] More voice commands
- [ ] Plugin system for custom commands
- [ ] System tray integration

### v0.3
- [ ] macOS support
- [ ] Windows support
- [ ] Multiple language support
- [ ] Voice feedback (TTS)

### v1.0
- [ ] Cloud integration (optional)
- [ ] Smart home control
- [ ] Calendar/reminder integration
- [ ] Learning/adaptive behavior

## 📄 License

MIT License - See [LICENSE](LICENSE) file for details

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 💬 Support

- 🐛 **Issues**: [GitHub Issues](https://github.com/yourusername/nuxai/issues)
- 💡 **Discussions**: [GitHub Discussions](https://github.com/yourusername/nuxai/discussions)
- 📧 **Email**: your.email@example.com

## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) - Offline speech recognition
- [FastAPI](https://fastapi.tiangolo.com/) - Modern Python web framework
- [Flutter](https://flutter.dev/) - Beautiful native applications

---

<div align="center">

**Made with ❤️ for the Linux community**

[⭐ Star on GitHub](https://github.com/yourusername/nuxai) • [🐦 Follow on Twitter](https://twitter.com/yourusername)

</div>

