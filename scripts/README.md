# 🔧 NuxAI Scripts

Helper scripts for running and managing NuxAI.

## 📜 Available Scripts

### setup.sh
Automated installation of all dependencies.

```bash
./scripts/setup.sh
```

Does:
- Detects your OS
- Installs system dependencies
- Installs Python packages
- Downloads Vosk model (optional)
- Sets up Flutter (optional)

### start.sh
Quick start for both backend and overlay.

```bash
./scripts/start.sh
```

Opens two terminals:
- Terminal 1: Backend server
- Terminal 2: Flutter overlay

### deploy.sh
Creates distribution packages.

```bash
./scripts/deploy.sh
```

Generates:
- `dist/nuxai-backend-1.0.0.tar.gz`
- `dist/nuxai-overlay-1.0.0-linux.tar.gz`
- `dist/install.sh`

### run_tray.py
Runs NuxAI with system tray icon.

```bash
python scripts/run_tray.py
```

Features:
- System tray icon
- Right-click menu
- Background operation
- Easy access to settings

## 🚀 Quick Commands

```bash
# Setup everything
./scripts/setup.sh

# Start NuxAI
./scripts/start.sh

# With system tray
python scripts/run_tray.py

# Deploy package
./scripts/deploy.sh
```

## 📝 Notes

- All scripts should be run from project root
- Make sure scripts are executable: `chmod +x scripts/*.sh`
- Check logs in `backend/logs/nuxai.log`

