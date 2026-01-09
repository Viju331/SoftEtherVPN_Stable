#!/bin/bash

# Create macOS Application Bundle for SoftEther VPN Manager

APP_NAME="SoftEther VPN Manager"
APP_DIR="${APP_NAME}.app"
CONTENTS_DIR="${APP_DIR}/Contents"
MACOS_DIR="${CONTENTS_DIR}/MacOS"
RESOURCES_DIR="${CONTENTS_DIR}/Resources"

echo "Creating macOS Application Bundle..."

# Clean previous build
rm -rf "${APP_DIR}"

# Create directory structure
mkdir -p "${MACOS_DIR}"
mkdir -p "${RESOURCES_DIR}"

# Copy Python script
cp vpn_manager_gui.py "${MACOS_DIR}/vpn_manager"
chmod +x "${MACOS_DIR}/vpn_manager"

# Create launcher script
cat > "${MACOS_DIR}/launch.sh" << 'EOF'
#!/bin/bash
DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$DIR"
python3 vpn_manager 2>&1 | logger -t "SoftEtherVPN"
EOF

chmod +x "${MACOS_DIR}/launch.sh"

# Create Info.plist
cat > "${CONTENTS_DIR}/Info.plist" << 'EOF'
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>CFBundleDevelopmentRegion</key>
    <string>en</string>
    <key>CFBundleExecutable</key>
    <string>launch.sh</string>
    <key>CFBundleIconFile</key>
    <string>AppIcon</string>
    <key>CFBundleIdentifier</key>
    <string>org.softether.vpn.manager</string>
    <key>CFBundleInfoDictionaryVersion</key>
    <string>6.0</string>
    <key>CFBundleName</key>
    <string>SoftEther VPN Manager</string>
    <key>CFBundlePackageType</key>
    <string>APPL</string>
    <key>CFBundleShortVersionString</key>
    <string>1.0</string>
    <key>CFBundleVersion</key>
    <string>1</string>
    <key>LSMinimumSystemVersion</key>
    <string>11.0</string>
    <key>NSHighResolutionCapable</key>
    <true/>
    <key>NSAppleScriptEnabled</key>
    <true/>
    <key>LSApplicationCategoryType</key>
    <string>public.app-category.utilities</string>
</dict>
</plist>
EOF

# Create simple icon (text-based)
# In a real app, you'd use iconutil to create a proper .icns file
cat > "${RESOURCES_DIR}/AppIcon.iconset.txt" << 'EOF'
For a proper icon, create an iconset with:
- icon_16x16.png
- icon_16x16@2x.png
- icon_32x32.png
- icon_32x32@2x.png
- icon_128x128.png
- icon_128x128@2x.png
- icon_256x256.png
- icon_256x256@2x.png
- icon_512x512.png
- icon_512x512@2x.png

Then run: iconutil -c icns AppIcon.iconset
EOF

echo "✅ Application bundle created: ${APP_DIR}"
echo
echo "To use:"
echo "  1. Open Finder"
echo "  2. Navigate to this directory"
echo "  3. Double-click '${APP_NAME}.app'"
echo
echo "Or from command line:"
echo "  open '${APP_DIR}'"
echo
echo "To install to Applications folder:"
echo "  cp -r '${APP_DIR}' /Applications/"
echo
