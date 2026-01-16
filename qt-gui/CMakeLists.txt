cmake_minimum_required(VERSION 3.16)
project(SoftEtherVPNQtManager VERSION 1.0 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

# Common source files used by all applications
set(COMMON_SOURCES
    src/MainWindow.cpp
    src/AccountDialog.cpp
    src/VLANDialog.cpp
    src/StatusDialog.cpp
    src/VpnBackend.cpp
    resources/resources.qrc
)

# VPN Manager
add_executable(SoftEtherVPNManager MACOSX_BUNDLE
    src/main.cpp
    ${COMMON_SOURCES}
)
set_target_properties(SoftEtherVPNManager PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER "com.softether.vpnmanager"
    MACOSX_BUNDLE_BUNDLE_NAME "SoftEther VPN Manager"
    MACOSX_BUNDLE_BUNDLE_VERSION "1.0"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0"
    MACOSX_BUNDLE_INFO_STRING "SoftEther VPN Manager for macOS"
)
target_link_libraries(SoftEtherVPNManager PRIVATE Qt6::Widgets)

# VPN Server
add_executable(SoftEtherVPNServer MACOSX_BUNDLE
    src/vpnserver_main.cpp
    ${COMMON_SOURCES}
)
set_target_properties(SoftEtherVPNServer PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER "com.softether.vpnserver"
    MACOSX_BUNDLE_BUNDLE_NAME "SoftEther VPN Server"
    MACOSX_BUNDLE_BUNDLE_VERSION "1.0"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0"
    MACOSX_BUNDLE_INFO_STRING "SoftEther VPN Server for macOS"
)
target_link_libraries(SoftEtherVPNServer PRIVATE Qt6::Widgets)

# VPN Client
add_executable(SoftEtherVPNClient MACOSX_BUNDLE
    src/vpnclient_main.cpp
    ${COMMON_SOURCES}
)
set_target_properties(SoftEtherVPNClient PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER "com.softether.vpnclient"
    MACOSX_BUNDLE_BUNDLE_NAME "SoftEther VPN Client"
    MACOSX_BUNDLE_BUNDLE_VERSION "1.0"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0"
    MACOSX_BUNDLE_INFO_STRING "SoftEther VPN Client for macOS"
)
target_link_libraries(SoftEtherVPNClient PRIVATE Qt6::Widgets)

# VPN Bridge
add_executable(SoftEtherVPNBridge MACOSX_BUNDLE
    src/vpnbridge_main.cpp
    ${COMMON_SOURCES}
)
set_target_properties(SoftEtherVPNBridge PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER "com.softether.vpnbridge"
    MACOSX_BUNDLE_BUNDLE_NAME "SoftEther VPN Bridge"
    MACOSX_BUNDLE_BUNDLE_VERSION "1.0"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0"
    MACOSX_BUNDLE_INFO_STRING "SoftEther VPN Bridge for macOS"
)
target_link_libraries(SoftEtherVPNBridge PRIVATE Qt6::Widgets)
