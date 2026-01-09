#!/bin/bash

# SoftEther VPN Apple Silicon Setup Script
# This script helps set up and build SoftEther VPN on Apple Silicon Macs (M1/M2/M3/M4)

set -e

echo "=========================================="
echo "SoftEther VPN - Apple Silicon Setup"
echo "=========================================="
echo

# Check if running on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This script is for macOS only"
    exit 1
fi

# Check if running on Apple Silicon
ARCH=$(uname -m)
if [[ "$ARCH" != "arm64" ]]; then
    echo "⚠️  Warning: This script is optimized for Apple Silicon (ARM64)"
    echo "   Detected architecture: $ARCH"
    echo "   You may want to use the standard build process instead."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi
fi

echo "✅ Detected Apple Silicon Mac ($(sysctl -n machdep.cpu.brand_string))"
echo

# Check for Xcode Command Line Tools
echo "Checking for Xcode Command Line Tools..."
if ! command -v gcc &> /dev/null; then
    echo "❌ Xcode Command Line Tools not found"
    echo "Installing Xcode Command Line Tools..."
    xcode-select --install
    echo "⚠️  Please wait for installation to complete, then run this script again"
    exit 1
else
    echo "✅ Xcode Command Line Tools installed"
fi

# Check for Homebrew
echo "Checking for Homebrew..."
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew not found"
    echo "Installing Homebrew..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
    
    # Add Homebrew to PATH for Apple Silicon
    if [[ "$ARCH" == "arm64" ]]; then
        echo 'eval "$(/opt/homebrew/bin/brew shellenv)"' >> ~/.zprofile
        eval "$(/opt/homebrew/bin/brew shellenv)"
    fi
else
    echo "✅ Homebrew installed at $(brew --prefix)"
fi

# Install dependencies
echo
echo "Installing required dependencies..."
DEPS=(openssl readline ncurses)
MISSING_DEPS=()

for dep in "${DEPS[@]}"; do
    if brew list "$dep" &> /dev/null; then
        echo "✅ $dep is already installed"
    else
        MISSING_DEPS+=("$dep")
    fi
done

if [ ${#MISSING_DEPS[@]} -gt 0 ]; then
    echo "Installing missing dependencies: ${MISSING_DEPS[*]}"
    brew install "${MISSING_DEPS[@]}"
else
    echo "✅ All dependencies are installed"
fi

# Display library paths
echo
echo "Library paths:"
echo "  Homebrew prefix: $(brew --prefix)"
echo "  OpenSSL: $(brew --prefix openssl)"
echo "  Readline: $(brew --prefix readline)"

# Run configure
echo
echo "Running configure script..."
if [ -f "./configure" ]; then
    ./configure
else
    echo "❌ Error: configure script not found"
    echo "   Please make sure you're in the SoftEther VPN root directory"
    exit 1
fi

# Build
echo
read -p "Would you like to build SoftEther VPN now? (Y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Build skipped. Run 'make' when ready to build."
    exit 0
fi

echo "Building SoftEther VPN..."
make -j$(sysctl -n hw.ncpu)

echo
echo "=========================================="
echo "✅ Build completed successfully!"
echo "=========================================="
echo
echo "Binaries are located in:"
echo "  VPN Server:  bin/vpnserver/vpnserver"
echo "  VPN Client:  bin/vpnclient/vpnclient"
echo "  VPN Bridge:  bin/vpnbridge/vpnbridge"
echo "  VPN Command: bin/vpncmd/vpncmd"
echo
echo "To verify ARM64 architecture:"
echo "  file bin/vpnserver/vpnserver"
echo
echo "To install system-wide:"
echo "  sudo make install"
echo
echo "To start VPN Server:"
echo "  sudo ./bin/vpnserver/vpnserver start"
echo
echo "For more information, see BUILD_MACOS_ARM64.md"
echo
