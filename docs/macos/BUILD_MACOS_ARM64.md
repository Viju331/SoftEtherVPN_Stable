# Building SoftEther VPN on Apple Silicon (M1/M2/M3/M4) Macs

This guide explains how to build SoftEther VPN on macOS with Apple Silicon (ARM64 architecture).

## Overview

Apple Silicon Macs (M1, M2, M3, M4) use ARM64 architecture instead of x86_64. This build has been optimized to work natively on these processors without requiring Rosetta 2 translation.

## Prerequisites

### 1. Install Xcode Command Line Tools

```bash
xcode-select --install
```

### 2. Install Homebrew

If you don't have Homebrew installed:

```bash
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

On Apple Silicon, Homebrew installs to `/opt/homebrew` by default.

### 3. Install Required Dependencies

```bash
brew install openssl readline ncurses
```

## Build Instructions

### Step 1: Navigate to the Source Directory

```bash
cd /path/to/SoftEtherVPN_Stable
```

### Step 2: Run Configure Script

The configure script will automatically detect your Apple Silicon Mac:

```bash
./configure
```

You should see output like:

```
Detected configuration:
  OS: macos
  CPU: 64bit
  Architecture: arm64
  ARM/AArch64 detected - using optimized build flags
```

### Step 3: Build the Project

```bash
make
```

The build process will:

- Automatically use ARM64-optimized compiler flags
- Link against Homebrew-installed libraries in `/opt/homebrew`
- Create native ARM64 binaries

### Step 4: Verify the Build

Check that the binaries are built for ARM64:

```bash
file bin/vpnserver/vpnserver
```

You should see output containing `arm64`.

### Step 5: Install (Optional)

To install system-wide:

```bash
sudo make install
```

## Running SoftEther VPN

**Note**: For complete information about all components and their ARM64 support status, see [COMPONENTS_ARM64_SUPPORT.md](COMPONENTS_ARM64_SUPPORT.md)

### Start VPN Server

```bash
sudo ./bin/vpnserver/vpnserver start
```

### Start VPN Client

```bash
sudo ./bin/vpnclient/vpnclient start
```

### Start VPN Bridge

```bash
sudo ./bin/vpnbridge/vpnbridge start
```

### Use Command-Line Tool

```bash
./bin/vpncmd/vpncmd
```

**All four components above are natively compiled for ARM64 and fully optimized for your Apple Silicon Mac.**

## Troubleshooting

### Issue: "Library not loaded" errors

If you see errors about missing libraries, ensure Homebrew packages are installed:

```bash
brew install openssl readline ncurses
```

### Issue: Configure script doesn't detect ARM64

Manually verify your architecture:

```bash
uname -m
```

Should output: `arm64`

### Issue: Compilation errors with OpenSSL

Make sure you're using the Homebrew version of OpenSSL:

```bash
brew --prefix openssl
```

The makefile will automatically detect this path.

### Issue: Permission denied errors

Some operations require root privileges:

```bash
sudo ./bin/vpnserver/vpnserver start
```

## Performance Notes

Native ARM64 builds typically provide:

- Better performance compared to x86_64 binaries running under Rosetta 2
- Lower power consumption
- Better thermal characteristics
- Full access to Apple Silicon hardware features

## Architecture Details

### What Changed for ARM64 Support

1. **Configure Script Enhancement**

   - Improved ARM64/aarch64 detection
   - Automatic selection of ARM64-optimized makefile
   - Display of detected configuration

2. **Makefile Optimization**

   - Added `-arch arm64` compiler flag for native ARM64 compilation
   - Automatic detection of Homebrew library paths
   - Inclusion of `/opt/homebrew` paths for libraries
   - Optimized for Apple Silicon processors

3. **Library Linking**
   - Dynamic detection of OpenSSL installation path
   - Dynamic detection of readline installation path
   - Support for both Intel (`/usr/local`) and Apple Silicon (`/opt/homebrew`) Homebrew locations

## Universal Binary (Optional)

If you need to create a universal binary that works on both Intel and Apple Silicon Macs:

```bash
# Build for ARM64
./configure
make
mv bin/vpnserver/vpnserver bin/vpnserver/vpnserver_arm64

# Clean and build for x86_64
make clean
# Modify makefile to use x86_64
sed -i '' 's/-arch arm64/-arch x86_64/g' Makefile
make
mv bin/vpnserver/vpnserver bin/vpnserver/vpnserver_x86_64

# Create universal binary
lipo -create -output bin/vpnserver/vpnserver \
    bin/vpnserver/vpnserver_arm64 \
    bin/vpnserver/vpnserver_x86_64
```

## Compatibility

- ✅ macOS 11.0 Big Sur and later (recommended)
- ✅ macOS 12.0 Monterey
- ✅ macOS 13.0 Ventura
- ✅ macOS 14.0 Sonoma
- ✅ macOS 15.0 Sequoia

## System Requirements

- Apple Silicon Mac (M1, M2, M3, M4, or later)
- macOS 11.0 (Big Sur) or later
- At least 2GB of free disk space
- Administrator (sudo) privileges for installation and running services

## Additional Resources

- [SoftEther VPN Project Website](https://www.softether.org/)
- [GitHub Repository](https://github.com/SoftEtherVPN/SoftEtherVPN)
- [Documentation](https://www.softether.org/4-docs)

## Support

If you encounter issues specific to Apple Silicon builds:

1. Check that all dependencies are installed via Homebrew
2. Verify you're using the latest version of Xcode Command Line Tools
3. Ensure your macOS is up to date
4. Check the GitHub issues page for known problems

## License

SoftEther VPN is licensed under the Apache License 2.0. See LICENSE.TXT for details.
