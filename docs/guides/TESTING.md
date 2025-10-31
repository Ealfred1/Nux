# NuxAI v0.3 - Testing Guide

## 🧪 Testing the Complete System

### Prerequisites Check

Before testing, ensure you have:
- [ ] Python 3.8+ installed
- [ ] Flutter 3.0+ installed (optional for full testing)
- [ ] Microphone connected and working
- [ ] Speakers/headphones for TTS output

### Quick Dependency Check

```bash
# Check Python
python3 --version

# Check if pip works
pip3 --version

# Check audio system
arecord -l

# Check Flutter (optional)
flutter --version
```

## 📋 Test Plan

### Level 1: Backend Only Test (No Dependencies)

Test the backend without installing heavy dependencies:

```bash
cd /home/eric/nux/backend
python3 main.py
```

**Expected Output**:
```
🚀 Starting NuxAI Backend v0.3.0...
✅ Configuration loaded from config.json
✅ NuxAI Backend is ready!
   - Wake words: ['computer', 'hey computer', 'nux', 'hey nux']
   - Personality: Nux (friendly)
   - TTS enabled: True
INFO:     Started server process
INFO:     Waiting for application startup complete.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://127.0.0.1:8000
```

**Test API**:
```bash
# Health check
curl http://127.0.0.1:8000/api/health

# Status check
curl http://127.0.0.1:8000/api/status

# API docs
# Open browser: http://127.0.0.1:8000/docs
```

### Level 2: Install Dependencies

```bash
cd /home/eric/nux/backend

# Install base dependencies (without Whisper for now)
pip install fastapi uvicorn websockets vosk pyaudio pyttsx3 python-dotenv pydantic pydantic-settings

# Start backend
python3 main.py
```

**What Works**:
- ✅ FastAPI server
- ✅ WebSocket communication
- ✅ TTS engine (pyttsx3)
- ✅ Personality system
- ✅ Intent parsing
- ✅ Command execution
- ⚠️ Whisper STT (requires larger install)

### Level 3: Full Installation with Whisper

```bash
cd /home/eric/nux/backend

# Install all dependencies including Whisper
pip install -r requirements.txt

# This will download ~1.5GB of PyTorch + Whisper models
# Takes 5-10 minutes depending on connection
```

**What's Added**:
- ✅ Whisper speech recognition
- ✅ Full STT capabilities
- ✅ Better accuracy

### Level 4: Flutter Overlay Test

```bash
cd /home/eric/nux/overlay

# Get Flutter dependencies
flutter pub get

# Run overlay (requires Linux desktop)
flutter run -d linux
```

**Expected Behavior**:
- Overlay window appears
- Connects to backend WebSocket
- Shows "Ready" state
- Displays "NuxAI" branding

## 🎯 Feature Tests

### Test 1: Configuration Loading

```bash
# View config
cat backend/config.json

# Modify personality
# Change "type": "friendly" to "type": "professional"
# Restart backend and observe different response style
```

### Test 2: TTS Engine

```python
# Test TTS independently
cd backend
python3 -c "
from core.tts_engine import TTSEngine
import asyncio

tts = TTSEngine()
asyncio.run(tts.speak('Hello! This is Nux speaking!'))
"
```

### Test 3: Intent Parser

```python
# Test intent parsing
cd backend
python3 -c "
from core.intent_parser import IntentParser

parser = IntentParser()
result = parser.parse('open browser')
print(result)

result = parser.parse('set volume to 50')
print(result)
"
```

**Expected Output**:
```python
{'intent': 'open_application', 'original_text': 'open browser', ...}
{'intent': 'volume_control', 'original_text': 'set volume to 50', ...}
```

### Test 4: Command Execution

```python
# Test command executor
cd backend
python3 -c "
from core.command_executor import CommandExecutor
import asyncio

executor = CommandExecutor()
result = asyncio.run(executor.execute('what time is it'))
print(result)
"
```

### Test 5: Full Voice Flow (Without Model)

Even without Whisper model, the system works with fallback demo commands:

```bash
# Start backend
cd backend
python3 main.py

# In logs, you'll see:
# - Wake word detector starts (may use fallback)
# - System is listening
# - TTS is initialized
```

## 🐛 Common Issues & Fixes

### Issue: PyAudio fails to install

**Solution**:
```bash
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

### Issue: pyttsx3 doesn't speak

**Solution**:
```bash
# Install espeak
sudo apt-get install espeak espeak-data libespeak-dev

# Test
espeak "Hello World"
```

### Issue: Whisper is slow

**Options**:
1. Use smaller model in `config.json`: change `"whisper_model": "base"` to `"tiny"`
2. Use GPU acceleration (if available)
3. Stick with Vosk for faster performance

### Issue: Flutter overlay won't build

**Solution**:
```bash
# Enable Linux desktop
flutter config --enable-linux-desktop

# Install dependencies
sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev

# Clean and rebuild
flutter clean
flutter pub get
flutter run -d linux
```

## ✅ Validation Checklist

After setup, verify:

- [ ] Backend starts without errors
- [ ] Configuration loads from `config.json`
- [ ] TTS engine initializes (check logs)
- [ ] API endpoints respond correctly
- [ ] WebSocket connection works
- [ ] Intent parser recognizes commands
- [ ] Command executor runs actions
- [ ] Personality responses are appropriate
- [ ] Overlay connects to backend (if running)
- [ ] Voice responses play through speakers

## 🎭 Personality Testing

Test different personalities:

1. **Friendly** (default):
   - "Hey! I'm here!"
   - "Cool, doing it!"
   
2. **Professional**:
   - "NuxAI assistant ready."
   - "Understood. Executing."

3. **Casual**:
   - "Hey! What's up?"
   - "Alright!"

4. **Excited**:
   - "Yes! I'm so ready!"
   - "Woohoo! Done!"

Change in `config.json`:
```json
"personality": {
  "type": "professional"  // or casual, excited
}
```

## 📊 Performance Benchmarks

Expected performance on modest hardware:

| Operation | Time | Notes |
|-----------|------|-------|
| Backend startup | 2-5s | Without Whisper model load |
| Wake word detection | Real-time | Vosk or fallback |
| Speech recording (5s) | 5s | Configurable duration |
| Whisper transcription | 2-8s | Depends on model size |
| Intent parsing | <0.1s | Very fast |
| Command execution | 0.5-2s | Depends on command |
| TTS response | 1-3s | Depends on text length |
| **Total flow** | **10-20s** | Wake to voice response |

## 🚀 Next Steps After Testing

If everything works:

1. ✅ Customize personality in `config.json`
2. ✅ Add your own wake words
3. ✅ Adjust TTS rate/volume to preference
4. ✅ Start using voice commands!

If issues persist:
- Check `backend/logs/nuxai.log`
- Review error messages
- Open an issue on GitHub
- Refer to troubleshooting section in README

## 🎉 Success Criteria

NuxAI v0.3 is working if:
- ✅ Backend runs and serves API
- ✅ Voice commands are recognized (Whisper or fallback)
- ✅ Intents are parsed correctly
- ✅ Commands execute successfully
- ✅ Voice responses are spoken
- ✅ Personality is reflected in responses
- ✅ Overlay shows state changes (if running)

You're ready to say "Computer" and get a voice response! 🎤

