#!/bin/bash
# Deploy Qt GUI for macOS using macdeployqt and create .dmg
set -e
APP_BUNDLE="qt-gui.app"
QT_BIN="$QT_DIR/bin"

if [ -z "$QT_DIR" ]; then
  echo "Please set QT_DIR environment variable to your Qt installation path."
  exit 1
fi

# Build the app first (assumes CMake build)
# cmake --build . --config Release

# Run macdeployqt
"$QT_BIN/macdeployqt" "$APP_BUNDLE" -dmg

# Output: .dmg file will be created in the build directory
