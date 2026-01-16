cmake_minimum_required(VERSION 3.16)
project(SoftEtherVPNQtManager VERSION 1.0 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

add_executable(SoftEtherVPNQtManager MACOSX_BUNDLE
    src/main.cpp
    src/MainWindow.cpp
    src/AccountDialog.cpp
    src/VLANDialog.cpp
    src/StatusDialog.cpp
    src/VpnBackend.cpp
    resources/resources.qrc
)

# Set macOS app bundle properties
set_target_properties(SoftEtherVPNQtManager PROPERTIES
    MACOSX_BUNDLE_GUI_IDENTIFIER "com.softether.vpnmanager"
    MACOSX_BUNDLE_BUNDLE_NAME "SoftEther VPN Manager"
    MACOSX_BUNDLE_BUNDLE_VERSION "1.0"
    MACOSX_BUNDLE_SHORT_VERSION_STRING "1.0"
    MACOSX_BUNDLE_INFO_STRING "SoftEther VPN Manager for macOS"
)

target_link_libraries(SoftEtherVPNQtManager PRIVATE Qt6::Widgets)
