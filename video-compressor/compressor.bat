@echo off

rem put node, npm, and ffmpeg in the PATH
set "PATH=%APPDATA%\npm;%PATH%"
set "PATH=%APPDATA%\ffmpeg\bin;%PATH%"

rem execute node command
call npm start

echo.
echo Press any key to exit

PAUSE >nul