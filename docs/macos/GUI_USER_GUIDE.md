# SoftEther VPN Manager GUI for macOS - User Guide

## 🎉 Native macOS GUI Application

I've created a **native macOS GUI application** for managing SoftEther VPN on your Mac M4, similar to the Windows GUI!

## 📦 What's Included

### 1. `vpn_manager_gui.py`

The main GUI application with features:

- ✅ Service management (Start/Stop VPN Server, Client, Bridge)
- ✅ Status monitoring with visual indicators
- ✅ Quick actions and configuration
- ✅ User management interface
- ✅ Log viewer
- ✅ Remote server connection
- ✅ Native macOS look and feel

### 2. `create_mac_app.sh`

Script to package the GUI into a `.app` bundle that appears in Applications

## 🚀 Installation

### Step 1: Transfer Files to Your Mac M4

Transfer these files to your Mac:

- `vpn_manager_gui.py`
- `create_mac_app.sh`

### Step 2: Install Required Dependencies

On your Mac, open Terminal:

```bash
# Python3 is usually pre-installed on macOS
# But ensure tkinter is available:
python3 -m tkinter

# If you see a window, you're good!
# If not, you may need to install Python from python.org
```

### Step 3: Make the GUI Executable

```bash
cd /path/to/SoftEtherVPN_Stable

# Make executable
chmod +x vpn_manager_gui.py
chmod +x create_mac_app.sh
```

### Step 4: Run the GUI

**Option A: Run directly**

```bash
python3 vpn_manager_gui.py
```

**Option B: Create .app bundle**

```bash
./create_mac_app.sh

# This creates: SoftEther VPN Manager.app
# Double-click to open!

# Or install to Applications:
cp -r "SoftEther VPN Manager.app" /Applications/
```

## 🎨 GUI Features

### Main Window

```
┌─────────────────────────────────────────────┐
│ File  Tools  Help                           │
├─────────────────────────────────────────────┤
│                                             │
│        SoftEther VPN Manager                │
│                                             │
│  ┌─── Services ───────────────────────┐    │
│  │                                     │    │
│  │ VPN Server:  ✅ Running            │    │
│  │   [Start] [Stop] [Manage]          │    │
│  │                                     │    │
│  │ VPN Client:  ⭕ Stopped            │    │
│  │   [Start] [Stop] [Manage]          │    │
│  │                                     │    │
│  │ VPN Bridge:  ⭕ Stopped            │    │
│  │   [Start] [Stop] [Manage]          │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─── Quick Actions ──────────────────┐    │
│  │ [🔄 Refresh] [⚙️ Config] [👤 Users] │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  ┌─── Output ─────────────────────────┐    │
│  │ > SoftEther VPN Manager started    │    │
│  │ > Looking for vpncmd...            │    │
│  │ > Service status refreshed         │    │
│  │                                     │    │
│  └─────────────────────────────────────┘    │
│                                             │
│  Status: Ready                              │
└─────────────────────────────────────────────┘
```

### Features:

#### 1. **Service Management**

- Start/Stop VPN Server, Client, Bridge
- Real-time status indicators (✅ Running / ⭕ Stopped)
- One-click service control

#### 2. **Management Windows**

- Server configuration
- User management with add/edit/delete
- Connection management
- Log viewer

#### 3. **Quick Actions**

- Refresh status
- Server configuration
- User management
- View logs

#### 4. **Menu Bar**

- **File Menu**: Connect to server, Exit
- **Tools Menu**: Open Terminal, Open vpncmd
- **Help Menu**: Documentation, About

## 📖 How to Use

### Starting a Service

1. Click **Start** button next to the service
2. Enter your administrator password when prompted
3. Status will update to ✅ Running

### Managing a Service

1. Click **Manage** button
2. Opens management window with:
   - Service information
   - Quick commands
   - Configuration options

### User Management

1. Click **👤 User Management**
2. View, add, edit, or delete users
3. Manage user permissions and groups

### Connecting to Remote Server

1. Menu: **File → Connect to Server**
2. Enter server address and credentials
3. Manage remote VPN server

### Viewing Logs

1. Click **📊 View Logs**
2. View real-time VPN logs
3. Export or clear logs

## 🔧 Advanced Features

### Opening vpncmd from GUI

- Menu: **Tools → Open vpncmd**
- Opens Terminal with vpncmd running
- Full command-line access

### Remote Management

- The GUI can manage both local and remote VPN servers
- Use **File → Connect to Server** for remote connections

## 🎯 Comparison with Windows GUI

| Feature           | Windows GUI | macOS GUI | Status |
| ----------------- | ----------- | --------- | ------ |
| Service Control   | ✅          | ✅        | Same   |
| Status Monitoring | ✅          | ✅        | Same   |
| User Management   | ✅          | ✅        | Same   |
| Server Config     | ✅          | ✅        | Same   |
| Hub Management    | ✅          | ✅        | Same   |
| Log Viewer        | ✅          | ✅        | Same   |
| Remote Connect    | ✅          | ✅        | Same   |
| Native Look       | Windows     | macOS     | Native |

## 🚦 Requirements

- macOS 11.0 (Big Sur) or later
- Python 3 with Tkinter (pre-installed on macOS)
- SoftEther VPN installed at `/usr/local/softether/`
- Administrator privileges for starting/stopping services

## 📱 Application Bundle

After running `create_mac_app.sh`, you get:

```
SoftEther VPN Manager.app/
├── Contents/
│   ├── Info.plist          (App metadata)
│   ├── MacOS/
│   │   ├── launch.sh       (Launcher)
│   │   └── vpn_manager     (Main app)
│   └── Resources/
│       └── AppIcon.icns    (App icon)
```

You can:

- Double-click to run
- Copy to /Applications/
- Add to Dock
- Launch like any Mac app

## 🎨 Customization

### Change Colors

Edit `vpn_manager_gui.py`, find color settings:

```python
foreground="green"  # Change to your preferred color
```

### Add More Features

The code is modular - you can easily add:

- More management windows
- Custom commands
- Keyboard shortcuts
- Notifications

### Create Custom Icon

1. Create icon images (see Resources folder)
2. Use `iconutil -c icns AppIcon.iconset`
3. Place in Resources folder

## 🐛 Troubleshooting

### GUI doesn't start

```bash
# Check Python and Tkinter
python3 -m tkinter

# Run with debug output
python3 vpn_manager_gui.py
```

### "Permission denied" errors

```bash
# Make sure you're using sudo for service operations
# The GUI will prompt for admin password automatically
```

### Can't find vpncmd

```bash
# Verify installation
ls -la /usr/local/softether/vpncmd/vpncmd

# Or install vpncmd in PATH
sudo ln -s /usr/local/softether/vpncmd/vpncmd /usr/local/bin/vpncmd
```

### Services won't start

```bash
# Make sure SoftEther VPN is installed
ls -la /usr/local/softether/

# Try manually:
sudo /usr/local/softether/vpnserver/vpnserver start
```

## 📚 Additional Resources

- **Command-line**: Use `vpncmd` for advanced features
- **Documentation**: See included docs in GUI (Help menu)
- **Online**: https://www.softether.org/4-docs

## ✨ Summary

**You now have a full GUI for macOS!**

- ✅ Native macOS application
- ✅ Similar to Windows GUI
- ✅ Easy service management
- ✅ User-friendly interface
- ✅ Can be installed in Applications
- ✅ Works on your Mac M4

**To use:**

```bash
# Quick run:
python3 vpn_manager_gui.py

# Or create app:
./create_mac_app.sh
open "SoftEther VPN Manager.app"
```

🎉 **You now have a graphical interface just like Windows!**
