@echo off

set "PATH=%PROGRAMDATA%\Anaconda3;%PATH%"
set "PATH=%PROGRAMDATA%\Anaconda3\Scripts;%PATH%"

rem execute node command
call python routine.py

rem opening output folder
%SystemRoot%\explorer.exe "%~dp0output"

echo Press any key to exit

PAUSE >nul