# NuxAI Quick Start Guide

Get up and running with NuxAI in under 5 minutes!

## 🚀 Fast Setup

### Option 1: Automated Setup (Recommended)

```bash
cd nuxai
./setup.sh
./start.sh
```

That's it! The scripts will handle everything.

### Option 2: Manual Setup

#### Step 1: Backend Setup

```bash
cd backend
pip install -r requirements.txt
python main.py
```

#### Step 2: Overlay Setup (New Terminal)

```bash
cd overlay
flutter pub get
flutter run -d linux
```

## 🎯 First Steps

1. **Wait for "Wake word detector ready!" message** in the backend terminal
2. **The overlay window will appear** - a dark, semi-transparent window
3. **Say "Computer" or "Hey Nux"** into your microphone
4. **The overlay will light up blue** - it's listening!
5. **Say a command** like "open browser"
6. **Watch it execute!**

## 🎤 Try These Commands

```
"open browser"      → Opens your web browser
"take screenshot"   → Captures your screen
"what time is it"   → Shows current time
"open terminal"     → Opens a terminal
"open file manager" → Opens file browser
```

## 🐛 Common Issues

### Backend won't start

```bash
# Install missing dependencies
cd backend
sudo apt-get install portaudio19-dev python3-pyaudio
pip install -r requirements.txt
```

### Overlay won't start

```bash
# Install Flutter
cd ~
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:$HOME/flutter/bin"
flutter config --enable-linux-desktop

cd nuxai/overlay
flutter pub get
flutter run -d linux
```

### No wake word detection

The backend works in demo mode without the Vosk model. For better accuracy:

```bash
cd backend/models
wget https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
unzip vosk-model-small-en-us-0.15.zip
```

### Microphone not working

```bash
# Test microphone
arecord -l

# Check permissions
sudo usermod -a -G audio $USER
# Log out and back in
```

## 📊 Check Status

### Backend Health

Visit in browser: http://127.0.0.1:8000/api/health

Or use curl:
```bash
curl http://127.0.0.1:8000/api/health
```

### API Documentation

Interactive docs: http://127.0.0.1:8000/docs

## 🛑 Stopping NuxAI

Press `Ctrl+C` in both terminal windows (backend and overlay)

## 📚 Next Steps

- Read [README.md](README.md) for full documentation
- Check [docs/API.md](docs/API.md) for API details
- See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Join the community and contribute!

## 💡 Tips

1. **Speak clearly** - The wake word detection works best with clear pronunciation
2. **Wait for the blue light** - Make sure the overlay shows blue before speaking your command
3. **Be patient** - First-time startup takes a few seconds to initialize
4. **Check logs** - Backend logs are in `backend/logs/nuxai.log`

## 🎉 You're Ready!

NuxAI is now active and listening. Say "Computer" to begin!

---

**Need help?** Open an issue on GitHub or check the [README](README.md) for more details.

