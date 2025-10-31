#!/bin/bash

# NuxAI Setup Script
# Installs all dependencies and prepares the environment

echo "🔧 Setting up NuxAI v0.1..."
echo ""

# Detect OS
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "❌ Cannot detect OS"
    exit 1
fi

echo "📦 Detected OS: $OS"
echo ""

# Install system dependencies
echo "📥 Installing system dependencies..."

case $OS in
    ubuntu|debian|pop)
        sudo apt-get update
        sudo apt-get install -y \
            python3 \
            python3-pip \
            python3-dev \
            portaudio19-dev \
            python3-pyaudio \
            gnome-screenshot \
            clang \
            cmake \
            ninja-build \
            pkg-config \
            libgtk-3-dev \
            git
        ;;
    fedora)
        sudo dnf install -y \
            python3 \
            python3-pip \
            python3-devel \
            portaudio-devel \
            gnome-screenshot \
            clang \
            cmake \
            ninja-build \
            gtk3-devel \
            git
        ;;
    arch|manjaro)
        sudo pacman -S --needed \
            python \
            python-pip \
            portaudio \
            gnome-screenshot \
            clang \
            cmake \
            ninja \
            gtk3 \
            git
        ;;
    *)
        echo "⚠️  Unsupported OS: $OS"
        echo "Please install dependencies manually."
        ;;
esac

echo ""
echo "🐍 Installing Python backend dependencies..."
cd backend
pip3 install -r requirements.txt --user
cd ..

echo ""
echo "📱 Flutter setup..."

if ! command -v flutter &> /dev/null; then
    echo "❌ Flutter not found."
    echo ""
    echo "To install Flutter:"
    echo "1. Visit: https://docs.flutter.dev/get-started/install/linux"
    echo "2. Or run: "
    echo "   cd ~ && git clone https://github.com/flutter/flutter.git -b stable"
    echo "   export PATH=\"\$PATH:\$HOME/flutter/bin\""
    echo "   flutter doctor"
    echo ""
    read -p "Install Flutter now? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        cd ~
        git clone https://github.com/flutter/flutter.git -b stable
        export PATH="$PATH:$HOME/flutter/bin"
        echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.bashrc
        echo 'export PATH="$PATH:$HOME/flutter/bin"' >> ~/.zshrc
        flutter doctor
        cd - > /dev/null
    fi
fi

if command -v flutter &> /dev/null; then
    echo "✅ Flutter found"
    flutter config --enable-linux-desktop
    cd overlay
    flutter pub get
    cd ..
fi

echo ""
echo "📥 Downloading Vosk model (optional, ~40MB)..."
read -p "Download voice recognition model for better accuracy? (y/n) " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    mkdir -p backend/models
    cd backend/models
    if [ ! -d "vosk-model-small-en-us-0.15" ]; then
        echo "Downloading..."
        wget -q --show-progress https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip
        unzip -q vosk-model-small-en-us-0.15.zip
        rm vosk-model-small-en-us-0.15.zip
        echo "✅ Model downloaded"
    else
        echo "✅ Model already exists"
    fi
    cd ../..
fi

echo ""
echo "✅ Setup complete!"
echo ""
echo "To start NuxAI:"
echo "  ./start.sh"
echo ""
echo "Or manually:"
echo "  Terminal 1: cd backend && python3 main.py"
echo "  Terminal 2: cd overlay && flutter run -d linux"
echo ""

