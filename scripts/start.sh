#!/bin/bash

# NuxAI Startup Script
# Starts both backend and overlay in separate terminal windows

echo "🚀 Starting NuxAI v0.1..."

# Check if backend dependencies are installed
if ! python3 -c "import fastapi" &> /dev/null; then
    echo "❌ Backend dependencies not installed."
    echo "Run: cd backend && pip install -r requirements.txt"
    exit 1
fi

# Start backend in new terminal
echo "📡 Starting backend..."
if command -v gnome-terminal &> /dev/null; then
    gnome-terminal --title="NuxAI Backend" -- bash -c "cd backend && python3 main.py; exec bash"
elif command -v konsole &> /dev/null; then
    konsole --title="NuxAI Backend" -e bash -c "cd backend && python3 main.py; exec bash" &
elif command -v xfce4-terminal &> /dev/null; then
    xfce4-terminal --title="NuxAI Backend" -e "bash -c 'cd backend && python3 main.py; exec bash'" &
else
    echo "⚠️  No terminal emulator found. Starting backend in background..."
    cd backend && python3 main.py &
    BACKEND_PID=$!
    cd ..
fi

# Wait for backend to start
echo "⏳ Waiting for backend to start..."
sleep 3

# Check if flutter is installed
if command -v flutter &> /dev/null; then
    echo "🎨 Starting overlay..."
    if command -v gnome-terminal &> /dev/null; then
        gnome-terminal --title="NuxAI Overlay" -- bash -c "cd overlay && flutter run -d linux; exec bash"
    elif command -v konsole &> /dev/null; then
        konsole --title="NuxAI Overlay" -e bash -c "cd overlay && flutter run -d linux; exec bash" &
    elif command -v xfce4-terminal &> /dev/null; then
        xfce4-terminal --title="NuxAI Overlay" -e "bash -c 'cd overlay && flutter run -d linux; exec bash'" &
    else
        cd overlay && flutter run -d linux &
    fi
else
    echo "⚠️  Flutter not installed. Overlay will not start."
    echo "Visit: https://docs.flutter.dev/get-started/install/linux"
fi

echo "✅ NuxAI is starting!"
echo ""
echo "Backend: http://127.0.0.1:8000"
echo "API Docs: http://127.0.0.1:8000/docs"
echo ""
echo "Say 'Computer' or 'Hey Nux' to activate!"

