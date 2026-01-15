@echo off
REM Deploy Qt GUI for Windows using windeployqt
setlocal
set APP_EXE=qt-gui.exe
set QT_BIN=%QT_DIR%\bin

if "%QT_DIR%"=="" (
    echo Please set QT_DIR environment variable to your Qt installation path.
    exit /b 1
)

REM Build the app first (assumes CMake build)
REM cmake --build . --config Release

REM Run windeployqt
"%QT_BIN%\windeployqt.exe" --release --no-quick-import "%APP_EXE%"

REM Output: All required Qt DLLs and plugins will be copied next to the exe
endlocal
