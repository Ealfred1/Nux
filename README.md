# 🎤 NuxAI - Intelligent Cross-Platform Voice Assistant

<div align="center">

**Your Local AI for Linux, Windows & macOS**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/yourusername/nuxai)
[![Platform](https://img.shields.io/badge/platform-Linux%20%7C%20Windows%20%7C%20macOS-lightgrey.svg)](https://www.linux.org/)
[![Python](https://img.shields.io/badge/python-3.8+-green.svg)](https://www.python.org/)
[![Flutter](https://img.shields.io/badge/flutter-3.0+-02569B.svg)](https://flutter.dev/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)

</div>

---

## 🚀 Quick Start

```bash
# 1. Install dependencies
cd backend
pip install -r requirements.txt

# 2. Start NuxAI
python main.py

# 3. Say "Computer, what time is it?"
```

**That's it!** NuxAI is now listening. 🎧

For detailed instructions, see [docs/guides/START_HERE.md](docs/guides/START_HERE.md)

---

## ✨ Features

### v1.0 Production Release

- 🎙️ **Offline Wake Word Detection** - "Computer" / "Hey Nux"
- 🧠 **Whisper Speech Recognition** - Accurate offline STT
- 🗣️ **Text-to-Speech** - Voice responses with personality
- 🎭 **Personality System** - Friendly, Professional, Casual, Excited
- 🔌 **Skills System** - Extensible plugins (Weather, Notes, Developer)
- 💡 **Intent Parsing** - Natural language understanding
- 🧠 **Local LLM** - Optional GPT4All integration
- 📝 **Context Memory** - Remembers conversation history
- 🖥️ **Cross-Platform** - Linux, Windows, macOS
- ⌨️ **Global Hotkeys** - Ctrl+Shift+Space to activate
- 🎨 **Web UI** - Browser-based settings
- 🔧 **System Tray** - Runs quietly in background
- ⚡ **Fast & Lightweight** - <100MB idle

## 📦 What's Included

```
nuxai/
├── 📁 backend/              Python FastAPI Backend
│   ├── core/                13 core modules
│   ├── skills/              Built-in & custom skills
│   ├── api/                 REST & WebSocket APIs
│   ├── web_ui/              Settings interface
│   └── main.py              Entry point
│
├── 📁 overlay/              Flutter Overlay UI
│   └── lib/                 6 UI components
│
├── 📁 scripts/              Helper Scripts
│   ├── setup.sh             Auto-install
│   ├── start.sh             Quick start
│   ├── deploy.sh            Distribution
│   └── run_tray.py          System tray
│
├── 📁 tests/                Testing Suite
│   └── test_api.py          API tests
│
├── 📁 docs/                 Documentation
│   ├── API.md               API reference
│   ├── ARCHITECTURE.md      System design
│   └── guides/              User guides
│
└── 📄 Essential Files
    ├── README.md            👈 You are here
    ├── CHANGELOG.md         Version history
    ├── LICENSE              MIT License
    └── CONTRIBUTING.md      Contribution guide
```

## 🎯 Built-in Skills

| Skill | Description | Example |
|-------|-------------|---------|
| 🌤️ **Weather** | Get weather anywhere | "What's the weather in London?" |
| 📝 **Notes** | Voice notes & reminders | "Remember to test NuxAI" |
| 💻 **Developer** | Git, Docker, VS Code | "Git status" |

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- pip
- PortAudio (Linux: `sudo apt install portaudio19-dev`)

### Quick Install

```bash
# Clone repository
git clone https://github.com/yourusername/nuxai.git
cd nuxai

# Run setup script
./scripts/setup.sh

# Start NuxAI
./scripts/start.sh
```

### Manual Install

```bash
# Install backend
cd backend
pip install -r requirements.txt

# Optional: Install Flutter for overlay
cd ../overlay
flutter pub get
```

## 🚦 Running NuxAI

### Method 1: Simple (Backend Only)

```bash
cd backend
python main.py
```

### Method 2: With System Tray

```bash
python scripts/run_tray.py
```

### Method 3: Full Stack (Backend + Overlay)

```bash
# Terminal 1: Backend
cd backend && python main.py

# Terminal 2: Overlay
cd overlay && flutter run -d linux
```

### Method 4: As System Service

```bash
# See docs/guides/SYSTEMTRAY.md
systemctl --user enable nuxai
systemctl --user start nuxai
```

## 🎮 Usage

### Voice Commands

```
"Computer, what time is it?"
"Hey Nux, take a screenshot"
"Computer, open browser"
"Hey Nux, what's the weather?"
"Computer, remember to test NuxAI"
"Hey Nux, git status"
```

### Web Interface

Open browser: **http://127.0.0.1:8000/settings**

### CLI Management

```bash
cd backend

# List skills
python nuxai_cli.py --list-skills

# Test skill
python nuxai_cli.py --test weather "weather in London"

# Create custom skill
python nuxai_cli.py --create myskill
```

## ⚙️ Configuration

Edit `backend/config.json`:

```json
{
  "personality": {
    "name": "Nux",
    "type": "friendly"
  },
  "voice": {
    "wake_words": ["computer", "hey nux"],
    "tts_rate": 175
  },
  "features": {
    "skills": true,
    "llm": false,
    "hotkeys": true
  }
}
```

**Personality Types:** `friendly`, `professional`, `casual`, `excited`

## 🧪 Testing

```bash
# Run API tests
python tests/test_api.py

# Test individual skill
cd backend
python nuxai_cli.py --test notes "remember to test"

# Check health
curl http://127.0.0.1:8000/api/health
```

## 📚 Documentation

| Document | Description |
|----------|-------------|
| [START_HERE.md](docs/guides/START_HERE.md) | Quick start guide |
| [QUICKSTART.md](docs/guides/QUICKSTART.md) | 5-minute setup |
| [API.md](docs/API.md) | API reference |
| [ARCHITECTURE.md](docs/ARCHITECTURE.md) | System design |
| [RUN_TESTS.md](docs/guides/RUN_TESTS.md) | Testing guide |
| [SYSTEMTRAY.md](docs/guides/SYSTEMTRAY.md) | System tray setup |
| [CHANGELOG.md](CHANGELOG.md) | Version history |

## 🔧 Development

### Create Custom Skill

```bash
cd backend
python nuxai_cli.py --create myskill
# Edit skills/user/myskill_skill.py
```

### Skill Template

```python
from core.skill_base import Skill, SkillMetadata

class MySkill(Skill):
    def get_metadata(self):
        return SkillMetadata(
            name="myskill",
            version="1.0.0",
            author="You",
            description="What it does",
            triggers=["keyword1", "keyword2"]
        )
    
    async def execute(self, command, context):
        return {
            "success": True,
            "result": "Done!",
            "speak": "Voice response here"
        }
```

## 🗺️ Roadmap

### ✅ Completed (v0.1 - v1.0)

- Wake word detection
- Whisper STT
- Text-to-speech
- Personality system
- Skills system
- LLM integration
- Context memory
- Cross-platform support
- System tray
- Web UI

### 🚧 Future (v1.1+)

- Plugin marketplace
- Mobile app (iOS/Android)
- Cloud sync (optional)
- Multi-language support
- Voice training
- Smart home integration
- Calendar/reminders
- Music control

## 🐛 Troubleshooting

### Microphone not working
```bash
# Test microphone
arecord -l

# Fix permissions
sudo usermod -a -G audio $USER
```

### Port 8000 already in use
```bash
# Check what's using it
lsof -i :8000

# Or change port in config.json
```

### Dependencies issues
```bash
cd backend
pip install -r requirements.txt --force-reinstall
```

See [docs/guides/RUN_TESTS.md](docs/guides/RUN_TESTS.md) for more troubleshooting.

## 🤝 Contributing

Contributions welcome! Please read [CONTRIBUTING.md](CONTRIBUTING.md) first.

1. Fork the repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🙏 Acknowledgments

- [Vosk](https://alphacephei.com/vosk/) - Offline speech recognition
- [OpenAI Whisper](https://github.com/openai/whisper) - Speech-to-text
- [FastAPI](https://fastapi.tiangolo.com/) - Web framework
- [Flutter](https://flutter.dev/) - UI framework
- [GPT4All](https://gpt4all.io/) - Local LLM

## 💬 Support

- 📖 [Documentation](docs/)
- 🐛 [Issues](https://github.com/yourusername/nuxai/issues)
- 💡 [Discussions](https://github.com/yourusername/nuxai/discussions)

## 📊 Stats

- **40 Code Files**
- **3,655 Lines of Code**
- **13 Core Modules**
- **3 Built-in Skills**
- **Cross-Platform Support**
- **100% Offline Capable**

---

<div align="center">

**Made with ❤️ for the Linux community**

[⭐ Star on GitHub](https://github.com/yourusername/nuxai) • [🐦 Follow Updates](https://twitter.com/yourusername)

**🎉 Start using NuxAI today: `python backend/main.py`**

</div>
