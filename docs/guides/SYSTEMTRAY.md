# 🎨 NuxAI System Tray Guide

## Running NuxAI with System Tray

The system tray integration allows NuxAI to run quietly in the background with easy access via a tray icon.

### Quick Start

```bash
cd /home/eric/nux
python3 run_tray.py
```

This will:
1. Start the backend server
2. Show a NuxAI icon in your system tray
3. Provide quick access via right-click menu

### System Tray Menu Options

Right-click the tray icon to access:

- **NuxAI** - Default action (shows status)
- **Enable Voice** - Toggle voice recognition on/off
- **Settings** - Open web settings UI
- **Skills** - Manage skills
- **Quit** - Exit NuxAI

### Installation as Startup Application

#### Option 1: Desktop Autostart (GNOME/KDE/XFCE)

Create autostart entry:

```bash
mkdir -p ~/.config/autostart

cat > ~/.config/autostart/nuxai.desktop <<EOF
[Desktop Entry]
Type=Application
Name=NuxAI Voice Assistant
Comment=AI Voice Assistant
Exec=/usr/bin/python3 /home/eric/nux/run_tray.py
Icon=/home/eric/nux/backend/icon.png
Terminal=false
Categories=Utility;
StartupNotify=false
X-GNOME-Autostart-enabled=true
EOF
```

#### Option 2: Systemd User Service

Create systemd service:

```bash
mkdir -p ~/.config/systemd/user

cat > ~/.config/systemd/user/nuxai.service <<EOF
[Unit]
Description=NuxAI Voice Assistant
After=network.target sound.target

[Service]
Type=simple
WorkingDirectory=/home/eric/nux
ExecStart=/usr/bin/python3 /home/eric/nux/run_tray.py
Restart=on-failure
RestartSec=5

[Install]
WantedBy=default.target
EOF

# Enable and start
systemctl --user daemon-reload
systemctl --user enable nuxai
systemctl --user start nuxai
```

Check status:
```bash
systemctl --user status nuxai
```

View logs:
```bash
journalctl --user -u nuxai -f
```

#### Option 3: Simple Background Script

Add to `~/.profile` or `~/.bashrc`:

```bash
# Start NuxAI on login
if ! pgrep -f "run_tray.py" > /dev/null; then
    cd /home/eric/nux && python3 run_tray.py &
fi
```

### Controlling NuxAI

#### Start
```bash
python3 run_tray.py
# or
systemctl --user start nuxai
```

#### Stop
```bash
# From tray: Right-click → Quit
# or
pkill -f "run_tray.py"
# or
systemctl --user stop nuxai
```

#### Restart
```bash
systemctl --user restart nuxai
```

### Troubleshooting

#### Tray icon not showing

1. Check if pystray is installed:
   ```bash
   pip install pystray pillow
   ```

2. Check system tray support:
   - GNOME: Install `gnome-shell-extension-appindicator`
   - KDE: Should work out of the box
   - XFCE: Should work out of the box

3. Check logs:
   ```bash
   tail -f backend/logs/nuxai.log
   ```

#### Backend not starting

Check if port 8000 is available:
```bash
lsof -i :8000
```

Check dependencies:
```bash
cd backend
pip install -r requirements.txt
```

#### Permissions issues

Make scripts executable:
```bash
chmod +x run_tray.py test_api.py
```

### Advanced: Custom Tray Icon

Replace the default icon:

1. Create a PNG icon (64x64 recommended)
2. Save as `backend/icon.png`
3. Update `core/system_tray.py` to load it:

```python
image = Image.open("icon.png")
```

### Integration with Desktop Environment

#### GNOME Quick Settings

Add NuxAI to GNOME quick settings:

```bash
# Install extension
gnome-extensions install nuxai-quick-settings

# Or use custom toggle
gsettings set org.gnome.shell.extensions.nuxai enabled true
```

#### KDE Plasma Widget

Create a Plasma widget for quick access:
- Right-click panel → Add Widgets
- Search for "Run Command"
- Configure to run `python3 /home/eric/nux/run_tray.py`

### Hotkey Activation

Even without the tray, you can activate NuxAI with:

**Default Hotkey:** `Ctrl+Shift+Space`

Change in `config.json`:
```json
{
  "hotkeys": {
    "activate": "ctrl+alt+space"
  }
}
```

### Monitoring

Check if NuxAI is running:

```bash
# Check process
ps aux | grep nuxai

# Check backend
curl http://127.0.0.1:8000/api/health

# Check system tray
pgrep -a python3 | grep run_tray
```

### Logs Location

- Backend logs: `backend/logs/nuxai.log`
- Systemd logs: `journalctl --user -u nuxai`
- Tray logs: stderr/stdout if not daemonized

### Resource Usage

NuxAI is designed to be lightweight:

- Idle: ~50-100 MB RAM
- Active (with Whisper): ~500 MB - 1 GB RAM
- CPU: <5% idle, 20-40% during voice processing

### Uninstall System Tray

Remove autostart:
```bash
rm ~/.config/autostart/nuxai.desktop
```

Remove systemd service:
```bash
systemctl --user stop nuxai
systemctl --user disable nuxai
rm ~/.config/systemd/user/nuxai.service
systemctl --user daemon-reload
```

---

## Tips

1. **Start Minimized**: The tray version runs in background automatically
2. **Battery Life**: Disable wake word detection if on battery
3. **Quick Toggle**: Use tray menu to enable/disable voice
4. **Web Settings**: Access settings anytime via tray menu
5. **Updates**: Restart service after updating code

Enjoy your always-available AI assistant! 🎤

