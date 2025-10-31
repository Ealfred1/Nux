# NuxAI Architecture

## System Overview

NuxAI consists of two main components that communicate via WebSocket:

```
┌─────────────────────────────────────────────────────────────┐
│                         User Input                           │
│                     (Voice: "Computer")                      │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                    Backend (Python)                          │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Wake Word Detector (Vosk)                    │  │
│  │  - Listens to microphone                             │  │
│  │  - Detects "computer", "nux", etc.                   │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │ Wake word detected                          │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Voice Processor                               │  │
│  │  - Captures command after wake word                   │  │
│  │  - Converts speech to text                            │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │ Command text                                │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Command Executor                              │  │
│  │  - Maps voice commands to actions                     │  │
│  │  - Executes system commands                           │  │
│  │  - Returns results                                    │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │ Results                                     │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         WebSocket Manager                             │  │
│  │  - Broadcasts events to overlay                       │  │
│  │  - Manages connections                                │  │
│  └────────────┬─────────────────────────────────────────┘  │
└───────────────┼─────────────────────────────────────────────┘
                │ WebSocket (Port 8000)
                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Overlay (Flutter)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         WebSocket Service                             │  │
│  │  - Connects to backend                                │  │
│  │  - Receives state updates                             │  │
│  │  - Auto-reconnects on disconnect                      │  │
│  └────────────┬─────────────────────────────────────────┘  │
│               │ State changes                               │
│               ▼                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         Overlay Screen                                │  │
│  │  - Displays current state                             │  │
│  │  - Shows commands & results                           │  │
│  │  - Animated indicators                                │  │
│  └──────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────┘
                      │
                      ▼
              Visual Feedback to User
```

## Backend Architecture

### FastAPI Application

The backend is built on FastAPI, providing:
- High-performance async request handling
- WebSocket support for real-time communication
- Automatic API documentation
- Easy extensibility

### Core Components

#### 1. Wake Word Detector (`core/wake_word_detector.py`)
- Uses Vosk for offline speech recognition
- Continuously listens to microphone input
- Detects configurable wake words
- Triggers voice command capture

#### 2. Voice Processor (`core/voice_processor.py`)
- Activates after wake word detection
- Captures user's voice command
- Converts speech to text
- Passes command to executor

#### 3. Command Executor (`core/command_executor.py`)
- Maps voice commands to system actions
- Executes Linux system commands
- Returns execution results
- Extensible command registry

#### 4. WebSocket Manager (`core/websocket_manager.py`)
- Singleton pattern for connection management
- Broadcasts events to all connected clients
- Handles connection/disconnection gracefully
- Supports multiple overlay instances

### API Layer

#### REST Endpoints (`api/health.py`)
- `/api/health` - Health check
- `/api/status` - System status

#### WebSocket Endpoint (`api/websocket.py`)
- `/ws/overlay` - Real-time overlay communication

## Overlay Architecture

### Flutter Application

Built with Flutter for:
- Native performance on Linux
- Beautiful, hardware-accelerated UI
- Cross-platform potential
- Rich widget ecosystem

### Key Components

#### 1. WebSocket Service (`services/websocket_service.dart`)
- Manages connection to backend
- Implements automatic reconnection
- Parses and dispatches messages
- Notifies UI of state changes

#### 2. Overlay Screen (`screens/overlay_screen.dart`)
- Main UI container
- Responds to state changes
- Manages animations
- Displays command feedback

#### 3. Widgets
- **Listening Indicator** - Animated mic icon
- **Command Display** - Shows current command and result

#### 4. State Management
- Uses Provider for state management
- WebSocketService as ChangeNotifier
- Reactive UI updates

## Communication Protocol

### Message Types (Backend → Overlay)

```json
// Connection established
{
  "type": "connected",
  "message": "Connected to NuxAI backend"
}

// Wake word detected
{
  "type": "wake_word_detected",
  "message": "Wake word detected",
  "timestamp": 1234567890
}

// Listening for command
{
  "type": "listening_started",
  "message": "Listening for command..."
}

// Command received
{
  "type": "command_received",
  "command": "open browser"
}

// Command result
{
  "type": "command_result",
  "result": {
    "success": true,
    "command": "open browser",
    "result": "Opening firefox"
  }
}

// Error
{
  "type": "error",
  "message": "Error message"
}
```

### Message Types (Overlay → Backend)

```json
// Overlay ready
{
  "type": "overlay_ready",
  "timestamp": 1234567890
}

// Heartbeat
{
  "type": "ping",
  "timestamp": 1234567890
}
```

## State Flow

1. **Idle State**
   - Backend listens for wake word
   - Overlay shows ready state

2. **Wake Word Detected**
   - Backend broadcasts `wake_word_detected`
   - Overlay shows listening animation
   - Backend starts command capture

3. **Processing State**
   - Backend captures and processes command
   - Broadcasts `command_received`
   - Overlay shows processing animation

4. **Execution State**
   - Backend executes command
   - Broadcasts `command_result`
   - Overlay shows result

5. **Return to Idle**
   - After timeout or completion
   - Both systems reset to idle

## Extension Points

### Adding New Commands

1. Add command handler to `CommandExecutor`:

```python
def _my_command(self):
    # Implementation
    return "Result message"

# Register in __init__
self.command_map["my command"] = self._my_command
```

### Adding New UI States

1. Add state to `overlay_state.dart`:

```dart
enum OverlayStateType {
  // ... existing states
  myNewState,
}
```

2. Handle in `overlay_screen.dart`

### Custom Wake Words

Edit `backend/core/wake_word_detector.py`:

```python
WAKE_WORDS = ["computer", "hey nux", "my custom word"]
```

## Performance Considerations

- **Backend**: Async/await for non-blocking operations
- **Overlay**: Flutter's optimized rendering pipeline
- **Communication**: Efficient JSON serialization
- **Voice Processing**: Vosk runs in separate thread

## Security

- Backend binds to localhost only (127.0.0.1)
- No external network communication
- All processing happens locally
- No data leaves the machine

## Future Improvements

- Plugin system for extensible commands
- Multiple language support
- Cloud integration (optional)
- Encrypted communication
- User authentication for multi-user systems

