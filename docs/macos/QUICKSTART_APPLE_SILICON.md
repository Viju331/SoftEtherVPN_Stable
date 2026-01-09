# Quick Start Guide for Apple Silicon Macs

## For Mac M1, M2, M3, M4, and later

### The Fastest Way (Automated)

```bash
# 1. Navigate to SoftEther VPN directory
cd /path/to/SoftEtherVPN_Stable

# 2. Make the setup script executable
chmod +x setup_apple_silicon.sh

# 3. Run the automated setup
./setup_apple_silicon.sh
```

That's it! The script will:

- ✅ Check your system
- ✅ Install Xcode Command Line Tools (if needed)
- ✅ Install Homebrew (if needed)
- ✅ Install dependencies (OpenSSL, readline, ncurses)
- ✅ Configure the build
- ✅ Compile SoftEther VPN

### Manual Method (If You Prefer)

```bash
# 1. Install Xcode Command Line Tools
xcode-select --install

# 2. Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# 3. Install dependencies
brew install openssl readline ncurses

# 4. Configure
./configure

# 5. Build
make

# 6. Verify (should say "arm64")
file bin/vpnserver/vpnserver
```

### Starting Services

```bash
# VPN Server
sudo ./bin/vpnserver/vpnserver start

# VPN Client
sudo ./bin/vpnclient/vpnclient start

# VPN Bridge
sudo ./bin/vpnbridge/vpnbridge start

# Command Line Tool
./bin/vpncmd/vpncmd
```

### Common Issues

**"Library not loaded" error?**

```bash
brew install openssl readline ncurses
```

**Permission denied?**

```bash
sudo ./bin/vpnserver/vpnserver start
```

**Not sure if ARM64?**

```bash
uname -m
# Should output: arm64
```

### Need More Help?

See the full guide: [BUILD_MACOS_ARM64.md](BUILD_MACOS_ARM64.md)

### Which Components Are Supported?

See the complete component list: [COMPONENTS_ARM64_SUPPORT.md](COMPONENTS_ARM64_SUPPORT.md)

All core components (Server, Client, Bridge, vpncmd) are **natively supported on ARM64**!

### System Requirements

- ✅ Mac with Apple Silicon (M1/M2/M3/M4)
- ✅ macOS 11.0 (Big Sur) or later
- ✅ At least 2GB free disk space
- ✅ Administrator (sudo) privileges

---

**Tip**: The automated script (`setup_apple_silicon.sh`) is the recommended approach for first-time users!
