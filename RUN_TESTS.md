# 🧪 NuxAI Testing Guide

## Quick Test

### 1. Start the Backend

```bash
cd /home/eric/nux/backend
python3 main.py
```

You should see:
```
🚀 Starting NuxAI Backend v1.0.0...
============================================================
🖥️  Platform detected: Linux
🔌 Loading skills...
  ✓ Loaded: weather v1.0.0
  ✓ Loaded: notes v1.0.0
  ✓ Loaded: developer v1.0.0
============================================================
✅ NuxAI v1.0.0 is ready!
   🎤 Wake words: computer, hey computer, nux, hey nux
   🎭 Personality: Nux (friendly)
   🗣️  TTS: Enabled
   🔌 Skills: 3 loaded
   🧠 LLM: Disabled
   ⌨️  Hotkeys: Enabled
   🖥️  Platform: Linux
   🌐 Web UI: http://127.0.0.1:8000/settings
============================================================
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### 2. Run API Tests

In a **new terminal**:

```bash
cd /home/eric/nux
python3 test_api.py
```

Expected output:
```
🚀 NuxAI API Test Suite
============================================================
Testing: http://127.0.0.1:8000

🧪 Testing: Root Endpoint (GET /)
✅ Status: 200
ℹ️  Service: NuxAI v1.0.0

🧪 Testing: Health Check (GET /api/health)
✅ Status: healthy

🧪 Testing: Status Check (GET /api/status)
✅ Status: running
    ✓ wake_word_detection
    ✓ voice_recognition
    ✓ text_to_speech
    ✓ intent_parsing
    ✓ skills

🧪 Testing: Settings UI (GET /settings)
✅ Settings page loaded

🧪 Testing: API Documentation (GET /docs)
✅ API docs accessible

🧪 Testing: WebSocket Connection (WS /ws/overlay)
✅ WebSocket connected
✅ Received: connected

============================================================
📊 Test Summary
============================================================
✅ PASS - Root Endpoint
✅ PASS - Health Check
✅ PASS - Status Endpoint
✅ PASS - Settings UI
✅ PASS - API Documentation
✅ PASS - WebSocket

Results: 6/6 tests passed
🎉 All tests passed!
```

### 3. Test Web UI

Open browser and visit:

- **Settings**: http://127.0.0.1:8000/settings
- **API Docs**: http://127.0.0.1:8000/docs
- **Health**: http://127.0.0.1:8000/api/health

### 4. Test Skills

```bash
cd /home/eric/nux/backend

# List skills
python3 nuxai_cli.py --list-skills

# Test weather skill
python3 nuxai_cli.py --test weather "what's the weather"

# Test notes skill
python3 nuxai_cli.py --test notes "remember to test NuxAI"

# Test developer skill
python3 nuxai_cli.py --test developer "git status"
```

### 5. Test Overlay (Optional)

If Flutter is installed:

```bash
cd /home/eric/nux/overlay
flutter run -d linux
```

You should see the NuxAI overlay window connect to the backend.

## Manual Testing Checklist

### ✅ Backend Tests

- [ ] Backend starts without errors
- [ ] All 3 skills load successfully
- [ ] Configuration loads from config.json
- [ ] TTS engine initializes
- [ ] Platform manager detects OS
- [ ] Logs are created in backend/logs/

### ✅ API Tests

- [ ] GET / returns service info
- [ ] GET /api/health returns healthy
- [ ] GET /api/status shows features
- [ ] GET /settings loads web UI
- [ ] GET /docs shows Swagger UI
- [ ] WS /ws/overlay connects

### ✅ Skills Tests

- [ ] Weather skill loads
- [ ] Notes skill loads
- [ ] Developer skill loads
- [ ] CLI can list skills
- [ ] CLI can test skills

### ✅ Web UI Tests

- [ ] Settings page loads
- [ ] All form fields visible
- [ ] Can change personality type
- [ ] Can toggle features
- [ ] Save button works

### ✅ Integration Tests

- [ ] WebSocket stays connected
- [ ] Can send/receive messages
- [ ] Context memory stores interactions
- [ ] Platform manager works
- [ ] Hotkeys initialize (if available)

## Performance Tests

### Memory Usage

```bash
# Check backend memory
ps aux | grep "python3 main.py" | awk '{print $6/1024 " MB"}'
```

Expected: <100 MB idle, ~500 MB with Whisper

### Response Time

```bash
# Test API response time
time curl http://127.0.0.1:8000/api/health
```

Expected: <100ms

### WebSocket Latency

Run test_api.py and check WebSocket response time.
Expected: <50ms

## Stress Tests

### Multiple Requests

```bash
# Send 100 requests
for i in {1..100}; do
    curl -s http://127.0.0.1:8000/api/health > /dev/null
done
```

Backend should handle without issues.

### Long-running Test

```bash
# Keep backend running for 1 hour
python3 main.py &
BACKEND_PID=$!

# Monitor
watch -n 10 'ps aux | grep $BACKEND_PID'

# After 1 hour
kill $BACKEND_PID
```

Check logs for memory leaks or errors.

## Debugging

### Enable Debug Logging

Edit `config.json`:
```json
{
  "app": {
    "debug": true
  }
}
```

### View Logs

```bash
# Real-time logs
tail -f backend/logs/nuxai.log

# Search for errors
grep ERROR backend/logs/nuxai.log

# Search for warnings
grep WARN backend/logs/nuxai.log
```

### Check Dependencies

```bash
cd backend
pip list | grep -E "fastapi|uvicorn|vosk|whisper|pyttsx3"
```

### Network Debugging

```bash
# Check if port is open
lsof -i :8000

# Check connections
netstat -an | grep 8000

# Test with verbose curl
curl -v http://127.0.0.1:8000/api/health
```

## Common Issues

### Port Already in Use

```bash
# Find what's using port 8000
lsof -i :8000

# Kill it
kill -9 <PID>

# Or change port in config.json
```

### Import Errors

```bash
# Reinstall dependencies
cd backend
pip install -r requirements.txt --force-reinstall
```

### TTS Not Working

```bash
# Install espeak
sudo apt-get install espeak espeak-data

# Test espeak
espeak "Hello World"
```

### WebSocket Connection Fails

Check firewall:
```bash
sudo ufw status
sudo ufw allow 8000/tcp
```

## Test Results Log

Keep track of your tests:

```bash
# Create test log
echo "NuxAI Test Results - $(date)" > test_results.log

# Run tests
python3 test_api.py 2>&1 | tee -a test_results.log

# View results
cat test_results.log
```

## Automated Testing

### Setup CI/CD (Optional)

Create `.github/workflows/test.yml`:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.10'
      - name: Install dependencies
        run: |
          cd backend
          pip install -r requirements.txt
      - name: Run tests
        run: |
          python3 test_api.py
```

---

**All tests passing? You're ready to go! 🚀**

