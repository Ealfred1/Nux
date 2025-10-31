# 🎤 NuxAI - Intelligent Cross-Platform Voice Assistant

<div align="center">

**An offline, privacy-focused voice assistant for Linux desktops with personality**

[![Version](https://img.shields.io/badge/version-0.3.0-blue.svg)](https://github.com/yourusername/nuxai)
[![Platform](https://img.shields.io/badge/platform-Linux-lightgrey.svg)](https://www.linux.org/)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/flutter-3.0+-02569B.svg)](https://flutter.dev/)

</div>

---

## 📋 Overview

NuxAI is a native desktop voice assistant that brings **intelligent voice interaction** to Linux, working entirely offline with no cloud dependencies. Activate it with a wake word, see a beautiful visual overlay, speak naturally, and get voice responses with personality!

### ✨ Key Features

- 🎙️ **Offline Wake Word Detection** - Uses Vosk for local voice recognition
- 🧠 **Whisper Speech Recognition** - Accurate STT with OpenAI Whisper (v0.2)
- 🗣️ **Text-to-Speech Responses** - Voice feedback with pyttsx3 (v0.3)
- 🎭 **Personality System** - Customizable AI personality (friendly, professional, casual) (v0.3)
- 💡 **Intent Parsing** - Natural language understanding (v0.2)
- 🖥️ **Sleek Visual Overlay** - Modern, transparent Flutter UI
- ⚡ **Advanced Commands** - Volume control, web search, system operations
- 🔒 **Privacy-First** - All processing happens on your machine
- 🚀 **FastAPI Backend** - High-performance async Python server
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

### Supported Commands (v0.3)

| Command | Action | Version |
|---------|--------|---------|
| "open browser" | Opens default web browser | v0.1 |
| "open [app name]" | Opens any application by name | v0.2 |
| "take screenshot" | Captures screen to Pictures/Screenshots | v0.1 |
| "what time is it" | Displays current time with voice | v0.1 |
| "open terminal" | Opens terminal window | v0.1 |
| "open file manager" | Opens file browser | v0.1 |
| "open calculator" | Opens calculator app | v0.1 |
| "increase/decrease volume" | Adjusts system volume | v0.2 |
| "set volume to [level]" | Sets volume to specific level | v0.2 |
| "mute/unmute" | Mutes or unmutes audio | v0.2 |
| "search for [query]" | Opens browser with search results | v0.2 |

### New in v0.3 🗣️
- **Voice Responses**: Nux now speaks back to you!
- **Personality Types**: Choose from friendly, professional, casual, or excited
- **Custom Configuration**: Edit `backend/config.json` to customize behavior
- **Natural Responses**: Context-aware, personality-driven responses

### New in v0.2 🧠
- **Whisper Integration**: More accurate speech recognition
- **Intent Parsing**: Better natural language understanding
- **Advanced Commands**: Volume control, web search, system operations

## 🛠️ Configuration

### Personality & Voice Settings (v0.3)

Edit `backend/config.json` to customize NuxAI:

```json
{
  "personality": {
    "name": "Nux",
    "type": "friendly",
    "voice_enabled": true
  },
  "voice": {
    "wake_words": ["computer", "hey computer", "nux"],
    "whisper_model": "base",
    "recording_duration": 5,
    "tts_rate": 175,
    "tts_volume": 0.9
  }
}
```

**Personality Types**:
- `friendly` - Warm and helpful (default)
- `professional` - Formal and efficient
- `casual` - Relaxed and conversational
- `excited` - Energetic and enthusiastic

### Server Configuration

Edit `backend/config.json`:

```json
{
  "server": {
    "host": "127.0.0.1",
    "port": 8000
  }
}
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

### ✅ v0.1 - COMPLETE
- [x] Wake word detection
- [x] Visual overlay
- [x] Basic commands
- [x] WebSocket communication

### ✅ v0.2 - COMPLETE
- [x] Whisper integration
- [x] Intent parsing
- [x] Advanced commands (volume, search)
- [x] Better accuracy

### ✅ v0.3 - COMPLETE
- [x] Text-to-speech responses
- [x] Personality system
- [x] Configuration system
- [x] Voice feedback

### v0.4 - In Progress
- [ ] Skills/plugins system
- [ ] Dynamic skill loading
- [ ] CLI for skill management
- [ ] Developer API

### v0.5
- [ ] Local LLM integration
- [ ] Context memory
- [ ] Conversation history
- [ ] Compound commands

### v0.6
- [ ] macOS support
- [ ] Windows support
- [ ] Cross-platform commands
- [ ] Hotkey fallback

### v1.0
- [ ] Stable release
- [ ] Multi-language support
- [ ] Plugin marketplace
- [ ] Custom themes
- [ ] Cloud sync (optional)

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

