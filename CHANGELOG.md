# Changelog

All notable changes to NuxAI will be documented in this file.

## [1.0.0] - 2025-10-31 🎉

### Added - Full Production Release
- **System Tray Integration**: Runs quietly in background with tray icon
- **Web-based Settings UI**: Configure NuxAI via browser at /settings
- **Theme System**: Dark/Light/Auto themes
- **Multi-language Foundation**: Infrastructure for i18n support
- **Deployment Scripts**: Easy installation and distribution
- **Platform Detection**: Automatic platform-specific behavior
- **Comprehensive Logging**: Detailed logging across all components

### Technical
- Complete integration of all features
- Production-ready error handling
- Modular architecture
- Extensive documentation

## [0.6.0] - 2025-10-31

### Added - Cross-Platform Support 🌍
- **Platform Manager**: Unified API for Windows, macOS, Linux
- **Hotkey System**: Global keyboard shortcuts (Ctrl+Shift+Space)
- **Platform Abstraction**: Commands work across all OSes
- **Clipboard Integration**: Cross-platform clipboard support
- **Windows Support**: Native Windows commands
- **macOS Support**: Native macOS commands

### Enhanced
- Screenshot works on all platforms
- Volume control unified
- Application launching abstracted
- Path handling normalized

## [0.5.0] - 2025-10-31

### Added - LLM & Context Memory 🧠
- **Local LLM Integration**: GPT4All for intelligent responses
- **Context Memory**: Remembers conversation history
- **Compound Commands**: Parse multiple actions ("open chrome and search")
- **Command History**: Track and search past commands
- **Session Statistics**: Usage analytics
- **Smart Understanding**: LLM-enhanced command interpretation

### Technical
- ChromaDB for vector storage
- Context window management
- Memory cleanup strategies
- LLM fallback handling

## [0.4.0] - 2025-10-31

### Added - Skills System 🔌
- **Dynamic Skill Loading**: Load skills from Python files
- **Skill Manager**: Centralized skill lifecycle
- **Built-in Skills**:
  - Weather: Get weather info (wttr.in API)
  - Notes: Voice notes and reminders
  - Developer: Git, Docker, VS Code commands
- **CLI Tool**: `nuxai_cli.py` for skill management
- **Skill API**: Easy custom skill development

### Technical
- Async skill execution
- Skill metadata system
- Priority-based skill matching
- Hot-reloadable skills

## [0.3.0] - 2025-10-31

### Added - Voice Output & Personality 🗣️
- **Text-to-Speech (TTS)**: Added pyttsx3 for voice responses
- **Personality System**: Configurable AI personality (friendly, professional, casual, excited)
- **Custom Responses**: Context-aware, personality-driven responses
- **Configuration System**: JSON-based configuration with `config.json`
- **Voice Settings**: Adjustable TTS rate, volume, and voice selection

### Enhanced
- Overlay displays personalized TTS responses
- Enhanced user feedback with voice confirmation
- Extended idle timeout for TTS playback
- Configuration-driven behavior

## [0.2.0] - 2025-10-31

### Added - Whisper Integration & Intent Parsing 🧠
- **Whisper STT**: Integrated OpenAI Whisper for accurate speech-to-text
- **Speech Processor**: Proper audio recording and transcription module
- **Intent Parser**: Natural language understanding with regex patterns
- **Advanced Commands**: Support for complex commands like:
  - Volume control (increase, decrease, set level, mute)
  - Web search (opens browser with search query)
  - System control (shutdown, restart, sleep)
  - File operations (planned)

### Enhanced
- Intent-based command routing for better accuracy
- Fallback mechanisms for models not available
- Command suggestions system
- Better error handling and logging

## [0.1.0] - 2025-10-31

### Added - Initial Release 🚀
- **Wake Word Detection**: Using Vosk for offline detection
- **FastAPI Backend**: High-performance async Python server
- **Flutter Overlay**: Beautiful cross-platform UI
- **WebSocket Communication**: Real-time bidirectional messaging
- **Basic Commands**:
  - Open browser/applications
  - Take screenshots
  - Get current time
  - Open terminal, file manager, calculator
- **Complete Documentation**: README, API docs, architecture guides
- **Setup Scripts**: Automated installation and startup
- **Git Repository**: Version controlled with proper .gitignore

### Technical
- Monorepo structure with backend and overlay
- Modular architecture for easy extension
- Comprehensive logging system
- Type-safe configuration
- CORS-enabled API
- Health check endpoints

---

## Version Roadmap

### [0.4.0] - Planned
- Skills/plugins system
- Dynamic skill loading
- CLI for skill management
- Developer API for custom skills

### [0.5.0] - Planned
- Local LLM integration (TinyLlama/GPT4All)
- Context memory
- Conversation history
- Compound commands

### [0.6.0] - Planned
- Windows support
- macOS support
- Cross-platform command abstraction
- Hotkey fallback

### [1.0.0] - Planned
- Stable release
- Multi-language support
- Plugin marketplace
- Custom themes
- Cloud sync (optional)

