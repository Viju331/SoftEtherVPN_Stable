# 📦 How to Create .dmg Installer File

## Overview

The `create_dmg.sh` script will package SoftEther VPN into a professional macOS disk image installer.

## 🚀 Quick Start

### On Your Mac M4:

```bash
# 1. Transfer all files to your Mac

# 2. Build the project first
cd SoftEtherVPN_Stable
./configure && make

# 3. Make script executable
cd scripts/macos
chmod +x create_dmg.sh

# 4. Create the .dmg disk image
./create_dmg.sh
```

**That's it!** You'll get:

- `SoftEtherVPN-ARM64-1.0-arm64.dmg` - Distributable disk image
- `SoftEtherVPN-ARM64-1.0-arm64.dmg` - Disk image (optional)

---

## 📋 Step-by-Step Guide

### Step 1: Transfer Files to Mac

Transfer the entire `SoftEtherVPN_Stable` folder to your Mac M4:

- All source files
- The `create_dmg.sh` script in `scripts/macos/`
- All documentation files

### Step 2: Build the Project

On your Mac M4, open Terminal:

```bash
# Navigate to the directory
cd ~/path/to/SoftEtherVPN_Stable

# Build the project
./configure && make
```

This compiles SoftEther VPN with ARM64 optimization for your Mac.

**Time**: 5-10 minutes

### Step 3: Create .dmg Disk Image

After building, create the DMG:

```bash
# Navigate to scripts
cd scripts/macos

# Make script executable
chmod +x create_dmg.sh

# Run the DMG creator
./create_dmg.sh
```

**What it does:**

1. ✅ Takes the .pkg file
2. ✅ Creates a DMG structure
3. ✅ Adds README and documentation
4. ✅ Configures appearance
5. ✅ Copies built binaries to DMG structure
6. ✅ Creates installation script
7. ✅ Adds README and documentation
8. ✅ Creates disk image
9. ✅ Compresses and finalizes
10. ✅ Creates `SoftEtherVPN-ARM64-1.0-arm64.dmg`

**Time**: 2-3 minutes

---

## 📦 What You Get

### After `create_dmg.sh`:

**File**: `SoftEtherVPN-ARM64-1.0-arm64.dmg`

**How to use:**

1. Double-click to mount
2. Inside: SoftEther VPN folder + documentation
3. Run `install.sh` to install

**Contents:**

- SoftEther VPN folder with binaries
- install.sh installation script
- README.txt with instructions
- Documentation folder

**Installation:**

```bash
# From the mounted DMG
cd "SoftEther VPN"
./install.sh
```

Or drag files to `/usr/local/softether/` manually.

---

## 💡 What the Script Does

### `create_dmg.sh` Script

```
1. Verify macOS and architecture
2. Install dependencies (if needed)
3. Build SoftEther VPN from source
1. Check built binaries exist
2. Create DMG folder structure
3. Copy binaries to DMG
4. Create installation script
5. Add README and documentation
6. Create temporary DMG
7. Configure appearance
8. Compress to final DMG
9. Output: SoftEtherVPN-ARM64-1.0-arm64.dmg
```

---

## 🎯 Installation Methods

### Method 1: Use install.sh (Recommended)

```bash
# Mount the DMG
open SoftEtherVPN-ARM64-1.0-arm64.dmg

# Run installer
cd "/Volumes/SoftEther VPN for Apple Silicon/SoftEther VPN"
./install.sh
```

### Method 2: Manual Installation

```bash
# Copy files manually
sudo mkdir -p /usr/local/softether
sudo cp -r "/Volumes/SoftEther VPN for Apple Silicon/SoftEther VPN"/* /usr/local/softether/
```

---

## 📊 File Details

| Feature           | Details                          |
| ----------------- | -------------------------------- |
| **Format**        | .dmg (Apple Disk Image)          |
| **Size**          | ~25-35MB                         |
| **Contents**      | Binaries + install script + docs |
| **Installation**  | Run install.sh or copy manually  |
| **Creation Time** | 2-3 minutes (after build)        |

---

## 🔧 Customization Options

### Change Installation Location

Edit `create_dmg.sh`, find:

```bash
INSTALL_BASE="/usr/local/softether"
```

Change to:

```bash
INSTALL_BASE="/Applications/SoftEtherVPN"
```

Then update the install.sh section accordingly.

### Change Version Number

Edit the script, find:

```bash
VERSION="1.0-arm64"
```

Change to your version:

```bash
VERSION="2.0-arm64"
```

### Add Custom Background to DMG

1. Create a background image (600x400 px recommended)
2. Save as `background.png`
3. Uncomment the background lines in `create_dmg.sh`

---

## ✅ Installation Instructions (for end users)

### Using .dmg file:

1. Download `SoftEtherVPN-ARM64-1.0-arm64.dmg`
2. Double-click to mount
3. Open "SoftEther VPN" folder
4. Run `install.sh`:
   - Right-click → Open With → Terminal
   - Or double-click and allow execution
5. Enter your Mac password when prompted
6. Done!

**Installed components:**

```
/usr/local/softether/vpnserver/
/usr/local/softether/vpnclient/
/usr/local/softether/vpnbridge/
/usr/local/softether/vpncmd/
```

**Manual Installation Alternative:**

```bash
sudo cp -r "SoftEther VPN"/* /usr/local/softether/
```

---

## 🚦 Starting Services After Installation

### VPN Server:

```bash
sudo /usr/local/softether/vpnserver/vpnserver start
```

### VPN Client:

```bash
sudo /usr/local/softether/vpnclient/vpnclient start
```

### VPN Bridge:

```bash
sudo /usr/local/softether/vpnbridge/vpnbridge start
```

### Command-Line Tool:

```bash
vpncmd
# or
/usr/local/softether/vpncmd/vpncmd
```

---

## 🗑️ Uninstallation

To uninstall:

```bash
# Stop services
sudo /usr/local/softether/vpnserver/vpnserver stop
sudo /usr/local/softether/vpnclient/vpnclient stop
sudo /usr/local/softether/vpnbridge/vpnbridge stop

# Remove files
sudo rm -rf /usr/local/softether
sudo rm /usr/local/bin/vpncmd
```

---

## 🔒 Code Signing (Optional)

To sign the DMG for distribution:

```bash
# Sign the DMG
codesign --sign "Developer ID Application: Your Name" \
    SoftEtherVPN-ARM64-1.0-arm64.dmg
```

**Note**: Requires Apple Developer account and certificate.

---

## 🐛 Troubleshooting

### "Permission denied" when running script

```bash
chmod +x create_dmg.sh
```

### Build not found

```bash
# Build the project first
cd ../..
./configure && make
# Then create DMG
cd scripts/macos
./create_dmg.sh
```

### Installation fails

```bash
# Run install.sh with sudo directly
cd "/Volumes/SoftEther VPN for Apple Silicon/SoftEther VPN"
sudo ./install.sh
```

### DMG won't mount - "Unidentified developer"

```bash
# Right-click the .dmg
# Choose "Open"
# Click "Open" in the dialog
```

Or in System Preferences:

```
Security & Privacy → General → Allow apps from: App Store and identified developers
```

---

## 📤 Distribution Checklist

Before distributing:

- [ ] Test installation on a clean Mac
- [ ] Verify all components work
- [ ] Check binary architecture (`file /usr/local/softether/vpnserver/vpnserver`)
- [ ] Test starting/stopping services
- [ ] Test vpncmd command
- [ ] Verify uninstallation works
- [ ] Include installation instructions
- [ ] Consider code signing for wider distribution

---

## 🎉 Summary

You now have **two powerful scripts** that create professional macOS installers:

1. **`create_pkg.sh`** → Creates `.pkg` installer
2. **`create_dmg.sh`** → Creates `.dmg` disk image

**To use them:**

```bash
# On your Mac M4
chmod +x create_pkg.sh create_dmg.sh
./create_pkg.sh      # Creates .pkg (10-15 min)
./create_dmg.sh      # Creates .dmg (2-3 min)
```

**You get:**

- Professional installers
- Easy distribution
- Standard Mac installation experience
- Complete documentation included

**Ready to share with other Apple Silicon Mac users!** 🚀
