@echo off

rem put node and npm in the PATH
set "PATH=%APPDATA%\npm;%PATH%"

rem execute gulp command
cmd /k gulp