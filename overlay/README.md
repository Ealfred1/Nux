# NuxAI Overlay

Flutter-based visual overlay for NuxAI voice assistant.

## Features

- 🎨 Modern, transparent overlay UI
- 📡 Real-time WebSocket communication with backend
- 🎭 Animated state indicators
- ⚡ Lightweight and responsive

## Prerequisites

- Flutter SDK 3.0 or higher
- Linux desktop environment

## Setup

### 1. Install Flutter

If Flutter is not installed:

```bash
# Download Flutter
cd ~
git clone https://github.com/flutter/flutter.git -b stable
export PATH="$PATH:`pwd`/flutter/bin"

# Verify installation
flutter doctor
```

### 2. Install Dependencies

```bash
cd overlay
flutter pub get
```

### 3. Linux Desktop Setup

Enable Linux desktop support:

```bash
flutter config --enable-linux-desktop
```

Install required system packages:

```bash
sudo apt-get install clang cmake ninja-build pkg-config libgtk-3-dev
```

## Running

### Development Mode

```bash
flutter run -d linux
```

### Build Release

```bash
flutter build linux --release
```

The binary will be in `build/linux/x64/release/bundle/`

## Configuration

The overlay connects to the backend WebSocket at:
- Default: `ws://127.0.0.1:8000/ws/overlay`

To change the backend URL, edit `lib/services/websocket_service.dart`

## Project Structure

```
lib/
├── main.dart                 # App entry point
├── screens/
│   └── overlay_screen.dart   # Main overlay screen
├── widgets/
│   ├── listening_indicator.dart  # Animated mic indicator
│   └── command_display.dart      # Command/result display
├── services/
│   └── websocket_service.dart    # WebSocket communication
└── models/
    └── overlay_state.dart        # State definitions
```

