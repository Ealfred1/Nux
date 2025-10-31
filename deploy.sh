#!/bin/bash

# NuxAI v1.0 Deployment Script
# Builds and packages NuxAI for distribution

set -e

echo "🚀 NuxAI v1.0 Deployment"
echo "========================"

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

# Get version
VERSION=$(grep -oP '"version":\s*"\K[^"]+' backend/config.json | head -1)
echo "Version: ${VERSION}"

# Create dist directory
mkdir -p dist

echo ""
echo -e "${BLUE}📦 Creating backend package...${NC}"
cd backend

# Create requirements with pinned versions
pip freeze > requirements-frozen.txt

# Create tarball
tar -czf ../dist/nuxai-backend-${VERSION}.tar.gz \
    --exclude='__pycache__' \
    --exclude='*.pyc' \
    --exclude='logs' \
    --exclude='models' \
    *.py \
    core/ \
    api/ \
    utils/ \
    skills/ \
    web_ui/ \
    requirements.txt \
    config.json \
    README.md

cd ..

echo -e "${GREEN}✅ Backend packaged${NC}"

# Package overlay if Flutter is available
if command -v flutter &> /dev/null; then
    echo ""
    echo -e "${BLUE}📦 Building Flutter overlay...${NC}"
    cd overlay
    
    flutter build linux --release
    
    # Create tarball
    cd build/linux/x64/release
    tar -czf ../../../../../dist/nuxai-overlay-${VERSION}-linux.tar.gz bundle/
    
    cd ../../../..
    echo -e "${GREEN}✅ Overlay built${NC}"
else
    echo -e "${BLUE}⚠️  Flutter not found, skipping overlay build${NC}"
fi

# Create installation script
cat > dist/install.sh <<'EOF'
#!/bin/bash

echo "Installing NuxAI v1.0..."

# Install backend
tar -xzf nuxai-backend-*.tar.gz -C /opt/nuxai/

# Install dependencies
cd /opt/nuxai
pip install -r requirements.txt

# Create systemd service (optional)
if [ "$1" == "--service" ]; then
    cat > /etc/systemd/system/nuxai.service <<EOL
[Unit]
Description=NuxAI Voice Assistant
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=/opt/nuxai
ExecStart=/usr/bin/python3 /opt/nuxai/main.py
Restart=always

[Install]
WantedBy=multi-user.target
EOL
    
    systemctl daemon-reload
    systemctl enable nuxai
    echo "✅ Service installed. Start with: sudo systemctl start nuxai"
fi

echo "✅ Installation complete!"
echo "Run: cd /opt/nuxai && python3 main.py"
EOF

chmod +x dist/install.sh

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📦 Packages created in dist/:"
ls -lh dist/
echo ""
echo "To install:"
echo "  sudo ./dist/install.sh"

