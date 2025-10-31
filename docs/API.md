# NuxAI API Documentation

## Base URL

```
http://127.0.0.1:8000
```

## REST API

### Health Check

Check if the backend is running.

**Endpoint**: `GET /api/health`

**Response**:
```json
{
  "status": "healthy",
  "service": "NuxAI Backend",
  "version": "0.1.0",
  "timestamp": "2025-10-31T12:00:00.000000"
}
```

### System Status

Get detailed system status.

**Endpoint**: `GET /api/status`

**Response**:
```json
{
  "status": "running",
  "service": "NuxAI Backend",
  "version": "0.1.0",
  "features": {
    "wake_word_detection": true,
    "voice_commands": true,
    "websocket": true,
    "offline_mode": true
  },
  "timestamp": "2025-10-31T12:00:00.000000"
}
```

### Root Endpoint

Get basic service information.

**Endpoint**: `GET /`

**Response**:
```json
{
  "name": "NuxAI",
  "version": "0.1.0",
  "status": "running",
  "message": "Intelligent Voice Assistant Backend"
}
```

## WebSocket API

### Overlay Connection

Real-time communication endpoint for the overlay UI.

**Endpoint**: `WS /ws/overlay`

#### Connection

```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws/overlay');
```

#### Messages from Backend

##### Connected
Sent when connection is established.

```json
{
  "type": "connected",
  "message": "Connected to NuxAI backend"
}
```

##### Backend Ready
Response to overlay_ready message.

```json
{
  "type": "backend_ready",
  "message": "Backend is ready"
}
```

##### Wake Word Detected
Sent when a wake word is detected.

```json
{
  "type": "wake_word_detected",
  "message": "Wake word detected",
  "timestamp": 1698758400.123
}
```

##### Listening Started
Sent when backend starts listening for a command.

```json
{
  "type": "listening_started",
  "message": "Listening for command..."
}
```

##### Command Received
Sent when a command is captured.

```json
{
  "type": "command_received",
  "command": "open browser"
}
```

##### Command Result
Sent with command execution result.

```json
{
  "type": "command_result",
  "result": {
    "success": true,
    "command": "open browser",
    "result": "Opening firefox"
  }
}
```

or on failure:

```json
{
  "type": "command_result",
  "result": {
    "success": false,
    "command": "unknown command",
    "error": "Command not recognized"
  }
}
```

##### Listening Timeout
Sent when no command is heard within timeout period.

```json
{
  "type": "listening_timeout",
  "message": "No command heard"
}
```

##### Error
Sent when an error occurs.

```json
{
  "type": "error",
  "message": "Error description"
}
```

##### Pong
Response to ping message.

```json
{
  "type": "pong",
  "timestamp": 1698758400.123
}
```

#### Messages to Backend

##### Overlay Ready
Send when overlay is ready to receive messages.

```json
{
  "type": "overlay_ready",
  "timestamp": 1698758400123
}
```

##### Ping
Heartbeat message to keep connection alive.

```json
{
  "type": "ping",
  "timestamp": 1698758400123
}
```

## Supported Voice Commands (v0.1)

| Command | Action | Result Message |
|---------|--------|----------------|
| "open browser" | Opens default browser | "Opening firefox" |
| "open firefox" | Opens Firefox | "Opening firefox" |
| "open chrome" | Opens Chrome | "Opening google-chrome" |
| "take screenshot" | Takes screenshot | "Screenshot saved to ~/Pictures/Screenshots/..." |
| "screenshot" | Takes screenshot | "Screenshot saved to ~/Pictures/Screenshots/..." |
| "what time is it" | Gets current time | "The time is HH:MM AM/PM" |
| "time" | Gets current time | "The time is HH:MM AM/PM" |
| "open terminal" | Opens terminal | "Opening gnome-terminal" |
| "open file manager" | Opens file manager | "Opening nautilus" |
| "open calculator" | Opens calculator | "Opening gnome-calculator" |

## Error Codes

### HTTP Status Codes

- `200` - Success
- `404` - Endpoint not found
- `500` - Internal server error

### WebSocket Close Codes

- `1000` - Normal closure
- `1001` - Going away
- `1002` - Protocol error
- `1011` - Internal error

## Rate Limiting

Currently no rate limiting is implemented. This may be added in future versions.

## Authentication

Currently no authentication is required. The service is designed for local use only.

## Examples

### Python Client Example

```python
import asyncio
import websockets
import json

async def connect_to_nuxai():
    uri = "ws://127.0.0.1:8000/ws/overlay"
    
    async with websockets.connect(uri) as websocket:
        # Send overlay ready message
        await websocket.send(json.dumps({
            "type": "overlay_ready",
            "timestamp": asyncio.get_event_loop().time()
        }))
        
        # Listen for messages
        async for message in websocket:
            data = json.loads(message)
            print(f"Received: {data}")
            
            if data["type"] == "wake_word_detected":
                print("Wake word detected!")
            elif data["type"] == "command_result":
                print(f"Result: {data['result']}")

asyncio.run(connect_to_nuxai())
```

### JavaScript Client Example

```javascript
const ws = new WebSocket('ws://127.0.0.1:8000/ws/overlay');

ws.onopen = () => {
    console.log('Connected to NuxAI');
    ws.send(JSON.stringify({
        type: 'overlay_ready',
        timestamp: Date.now()
    }));
};

ws.onmessage = (event) => {
    const data = JSON.parse(event.data);
    console.log('Received:', data);
    
    switch(data.type) {
        case 'wake_word_detected':
            console.log('Wake word detected!');
            break;
        case 'command_result':
            console.log('Result:', data.result);
            break;
    }
};

ws.onerror = (error) => {
    console.error('WebSocket error:', error);
};
```

### cURL Examples

**Health Check**:
```bash
curl http://127.0.0.1:8000/api/health
```

**Status**:
```bash
curl http://127.0.0.1:8000/api/status
```

## Interactive API Documentation

When the backend is running, visit:

- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

These provide interactive API documentation where you can test endpoints directly.

