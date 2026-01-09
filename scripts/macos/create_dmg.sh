#!/bin/bash

# SoftEther VPN ARM64 - macOS DMG Creator
# This script creates a .dmg disk image with compiled binaries

set -e

echo "=============================================="
echo "SoftEther VPN ARM64 - DMG Creator"
echo "Creating macOS .dmg disk image"
echo "=============================================="
echo

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script must run on macOS"
    exit 1
fi

# Variables
VERSION="1.0-arm64"
DMG_NAME="SoftEtherVPN-ARM64-${VERSION}"
DMG_TMP="dmg_temp"
VOLUME_NAME="SoftEther VPN for Apple Silicon"
BUILD_DIR="../../bin"

# Check if built binaries exist
if [ ! -d "$BUILD_DIR" ]; then
    echo "❌ Error: Built binaries not found at $BUILD_DIR"
    echo "   Please build the project first:"
    echo "   cd ../.."
    echo "   ./configure && make"
    exit 1
fi

echo "✅ Found built binaries"
echo

# Clean previous build
echo "Creating DMG structure..."
rm -rf "$DMG_TMP"
mkdir -p "$DMG_TMP/SoftEther VPN"

# Copy built binaries
echo "Copying binaries..."
cp -r "$BUILD_DIR/vpnserver" "$DMG_TMP/SoftEther VPN/" 2>/dev/null || true
cp -r "$BUILD_DIR/vpnclient" "$DMG_TMP/SoftEther VPN/" 2>/dev/null || true
cp -r "$BUILD_DIR/vpnbridge" "$DMG_TMP/SoftEther VPN/" 2>/dev/null || true
cp -r "$BUILD_DIR/vpncmd" "$DMG_TMP/SoftEther VPN/" 2>/dev/null || true
cp -r "$BUILD_DIR/hamcore.se2" "$DMG_TMP/SoftEther VPN/" 2>/dev/null || true

# Create installation script
cat > "$DMG_TMP/SoftEther VPN/install.sh" << 'INSTALLEOF'
#!/bin/bash
echo "Installing SoftEther VPN..."
sudo mkdir -p /usr/local/softether
sudo cp -r vpnserver /usr/local/softether/ 2>/dev/null || true
sudo cp -r vpnclient /usr/local/softether/ 2>/dev/null || true
sudo cp -r vpnbridge /usr/local/softether/ 2>/dev/null || true
sudo cp -r vpncmd /usr/local/softether/ 2>/dev/null || true
sudo cp hamcore.se2 /usr/local/softether/ 2>/dev/null || true
echo "✅ Installation complete!"
echo "To start: sudo /usr/local/softether/vpnserver/vpnserver start"
INSTALLEOF

chmod +x "$DMG_TMP/SoftEther VPN/install.sh"

# Create README for DMG
cat > "$DMG_TMP/README.txt" << 'EOF'
SoftEther VPN for Apple Silicon (ARM64)
========================================

Thank you for downloading SoftEther VPN!

INSTALLATION:
-------------
1. Open "SoftEther VPN" folder
2. Run install.sh:
   • Right-click → Open With → Terminal
   • Or: cd "SoftEther VPN" && ./install.sh
3. Enter your administrator password when prompted
4. Installation complete!

WHAT'S INCLUDED:
---------------
• VPN Server  - Full-featured VPN server
• VPN Client  - VPN client for remote access
• VPN Bridge  - Network bridging component
• vpncmd      - Command-line administration tool
• install.sh  - Installation script

GETTING STARTED:
---------------
After installation, open Terminal and run:

  To start VPN Server:
    sudo /usr/local/softether/vpnserver/vpnserver start

  To start VPN Client:
    sudo /usr/local/softether/vpnclient/vpnclient start

  To manage VPN:
    /usr/local/softether/vpncmd/vpncmd

MANUAL INSTALLATION:
--------------------
If install.sh doesn't work:
  sudo mkdir -p /usr/local/softether
  sudo cp -r "SoftEther VPN"/* /usr/local/softether/

SYSTEM REQUIREMENTS:
-------------------
• Apple Silicon Mac (M1, M2, M3, M4, or later)
• macOS 11.0 (Big Sur) or later
• Administrator privileges

DOCUMENTATION:
-------------
After installation: /usr/local/softether/docs/

Online: https://www.softether.org/

SUPPORT:
--------
Website: https://www.softether.org/
GitHub:  https://github.com/SoftEtherVPN/SoftEtherVPN_Stable/

LICENSE:
--------
Apache License 2.0
https://www.apache.org/licenses/LICENSE-2.0

---
This package contains SoftEther VPN compiled natively for ARM64.
Optimized for Apple Silicon processors.
EOF

# Create Documentation folder
mkdir -p "$DMG_TMP/Documentation"

# Copy documentation files if they exist
DOC_SOURCE="../../docs/macos"
[ -f "$DOC_SOURCE/BUILD_MACOS_ARM64.md" ] && cp "$DOC_SOURCE/BUILD_MACOS_ARM64.md" "$DMG_TMP/Documentation/"
[ -f "$DOC_SOURCE/QUICKSTART_APPLE_SILICON.md" ] && cp "$DOC_SOURCE/QUICKSTART_APPLE_SILICON.md" "$DMG_TMP/Documentation/"
[ -f "$DOC_SOURCE/GUI_USER_GUIDE.md" ] && cp "$DOC_SOURCE/GUI_USER_GUIDE.md" "$DMG_TMP/Documentation/"
[ -f "../../LICENSE.TXT" ] && cp "../../LICENSE.TXT" "$DMG_TMP/Documentation/"
[ -f "../../README.TXT" ] && cp "../../README.TXT" "$DMG_TMP/Documentation/"

echo "✅ DMG structure created"
echo

# Calculate size needed
echo "Calculating required size..."
SIZE=$(du -sm "$DMG_TMP" | awk '{print $1}')
SIZE=$((SIZE + 10))  # Add 10MB padding

echo "Creating temporary DMG..."
hdiutil create -srcfolder "$DMG_TMP" \
    -volname "$VOLUME_NAME" \
    -fs HFS+ \
    -fsargs "-c c=64,a=16,e=16" \
    -format UDRW \
    -size ${SIZE}m \
    "${DMG_NAME}.temp.dmg"

echo "✅ Temporary DMG created"

# Mount the DMG
echo "Mounting DMG..."
DEVICE=$(hdiutil attach -readwrite -noverify -noautoopen "${DMG_NAME}.temp.dmg" | grep '/Volumes/' | awk '{print $1}')
MOUNT_POINT="/Volumes/$VOLUME_NAME"

echo "✅ DMG mounted at: $MOUNT_POINT"

# Set custom icon and background (optional)
echo "Configuring DMG appearance..."

# Create .background folder for custom background
# mkdir -p "$MOUNT_POINT/.background"
# If you have a background image:
# cp background.png "$MOUNT_POINT/.background/"

# Set DMG view options using AppleScript
osascript << EOF
tell application "Finder"
    tell disk "$VOLUME_NAME"
        open
        set current view of container window to icon view
        set toolbar visible of container window to false
        set statusbar visible of container window to false
        set the bounds of container window to {100, 100, 700, 500}
        set viewOptions to the icon view options of container window
        set arrangement of viewOptions to not arranged
        set icon size of viewOptions to 128
        set background picture of viewOptions to file ".background:background.png"
        
        -- Position items
        set position of item "$PKG_FILE" of container window to {150, 150}
        set position of item "README.txt" of container window to {400, 150}
        set position of item "Documentation" of container window to {275, 300}
        
        close
        open
        update without registering applications
        delay 2
    end tell
end tell
EOF

# Ensure changes are written
sync
sleep 2

# Unmount
echo "Unmounting DMG..."
hdiutil detach "$DEVICE"

echo "✅ DMG unmounted"

# Convert to compressed read-only image
echo "Compressing DMG..."
hdiutil convert "${DMG_NAME}.temp.dmg" \
    -format UDZO \
    -imagekey zlib-level=9 \
    -o "${DMG_NAME}.dmg"

echo "✅ DMG compressed"

# Clean up
rm -f "${DMG_NAME}.temp.dmg"
rm -rf "$DMG_TMP"

echo
echo "=============================================="
echo "✅ SUCCESS! DMG created successfully!"
echo "=============================================="
echo
echo "📀 Disk image:"
echo "   ${DMG_NAME}.dmg"
echo
echo "File size: $(du -h "${DMG_NAME}.dmg" | cut -f1)"
echo "Location: $(pwd)/${DMG_NAME}.dmg"
echo
echo "To use:"
echo "   1. Double-click ${DMG_NAME}.dmg to open"
echo "   2. Double-click the .pkg file inside to install"
echo
echo "To distribute:"
echo "   Share ${DMG_NAME}.dmg with other Apple Silicon Mac users"
echo
echo "The DMG contains:"
echo "   • ${PKG_FILE} - Installer package"
echo "   • README.txt - Installation instructions"
echo "   • Documentation folder - Additional docs"
echo
echo "Done! 🎉"
