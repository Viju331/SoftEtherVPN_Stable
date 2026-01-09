# SoftEther VPN - macOS ARM64 Support

This directory contains the native macOS GUI application for managing SoftEther VPN on Apple Silicon.

## 📱 GUI Application

### vpn_manager_gui.py
Native macOS GUI application for managing SoftEther VPN with:
- Service control (VPN Server, Client, Bridge)
- Status monitoring
- User management
- Configuration interface
- Log viewer
- Remote server management

## 🚀 Usage

### Run Directly:
```bash
python3 gui/vpn_manager_gui.py
```

### Create Application Bundle:
```bash
cd scripts/macos
./create_mac_app.sh
# This creates: "SoftEther VPN Manager.app"
```

### Install to Applications:
```bash
cp -r "SoftEther VPN Manager.app" /Applications/
```

## 📖 Documentation

See **[docs/macos/GUI_USER_GUIDE.md](../docs/macos/GUI_USER_GUIDE.md)** for complete documentation.

## 🎨 Features

- ✅ Native macOS look and feel
- ✅ Service management (Start/Stop/Monitor)
- ✅ User and configuration management
- ✅ Visual status indicators
- ✅ Remote server connection
- ✅ Log viewer
- ✅ Compatible with Apple Silicon M1/M2/M3/M4

## 📦 Requirements

- macOS 11.0 (Big Sur) or later
- Python 3 with Tkinter (pre-installed)
- SoftEther VPN installed

---

For more information, see [GUI User Guide](../docs/macos/GUI_USER_GUIDE.md)
