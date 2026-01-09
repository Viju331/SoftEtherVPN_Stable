# SoftEther VPN - macOS Scripts

Automated scripts for building, packaging, and installing SoftEther VPN on macOS (Apple Silicon).

## 📜 Available Scripts

### setup_apple_silicon.sh

**Automated installation script** - One command to install everything!

```bash
./setup_apple_silicon.sh
```

**What it does:**

- Detects Apple Silicon architecture
- Installs dependencies via Homebrew
- Configures and builds all components
- Installs to `/usr/local/softether/`

### create_dmg.sh

**Creates .dmg disk image** - Distributable installer

```bash
./create_dmg.sh
```

**Output:** `SoftEtherVPN-ARM64-1.0.dmg`

**Note**: Build the project first with `./configure && make`

### create_mac_app.sh

**Creates GUI .app bundle** - Native macOS application

```bash
./create_mac_app.sh
```

**Output:** `SoftEther VPN Manager.app`

## 🚀 Quick Start

### Option 1: Automated Installation (Recommended)

```bash
cd scripts/macos
chmod +x setup_apple_silicon.sh
./setup_apple_silicon.sh
```

### Option 2: Manual Build + DMG

```bash
cd scripts/macos

# 1. Make scripts executable
chmod +x *.sh

# 2. Build from source (manual - see docs)
cd ../../
./configure
make

# 3. Create DMG installer
cd scripts/macos
./create_dmg.sh
```

### Option 3: GUI Application

```bash
cd scripts/macos
chmod +x create_mac_app.sh
./create_mac_app.sh

# Install to Applications
cp -r "SoftEther VPN Manager.app" /Applications/
```

## 📖 Documentation

See **[docs/macos/](../../docs/macos/)** for complete documentation:

- [HOW_TO_CREATE_INSTALLERS.md](../../docs/macos/HOW_TO_CREATE_INSTALLERS.md)
- [BUILD_MACOS_ARM64.md](../../docs/macos/BUILD_MACOS_ARM64.md)
- [QUICKSTART_APPLE_SILICON.md](../../docs/macos/QUICKSTART_APPLE_SILICON.md)

## 🔧 Requirements

- macOS 11+ (Big Sur or later)
- Apple Silicon (M1/M2/M3/M4)
- Homebrew package manager
- Xcode Command Line Tools

## 📦 Script Details

### setup_apple_silicon.sh

- Checks architecture (ARM64 required)
- Installs: OpenSSL, readline, ncurses, zlib
- Configures makefiles with ARM64 flags
- Builds all components
- Sets up installation directories

### create_dmg.sh

- Copies built binaries to DMG structure
- Creates installation script
- Customizes DMG appearance
- Adds background and icons
- Output: Distributable .dmg file

### create_mac_app.sh

- Packages Python GUI as .app bundle
- Creates Info.plist
- Sets up launcher scripts
- Output: Native macOS application

## 🎯 Usage Examples

### Install and Create DMG

```bash
# Full automation
./setup_apple_silicon.sh && ./create_dmg.sh
```

### Create GUI Application

```bash
./create_mac_app.sh
open "SoftEther VPN Manager.app"
```

### Clean Build

```bash
cd ../../
make clean
cd scripts/macos
./setup_apple_silicon.sh
```

---

**Platform**: macOS 11+ (Apple Silicon ARM64)  
**Last Updated**: January 2026
