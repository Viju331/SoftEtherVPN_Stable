cmake_minimum_required(VERSION 3.16)
project(SoftEtherVPNQtManager VERSION 1.0 LANGUAGES CXX)

set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

find_package(Qt6 COMPONENTS Widgets REQUIRED)

add_executable(SoftEtherVPNQtManager
    src/main.cpp
    src/MainWindow.cpp
    src/MainWindow.h
    resources/resources.qrc
)

target_link_libraries(SoftEtherVPNQtManager PRIVATE Qt6::Widgets)
