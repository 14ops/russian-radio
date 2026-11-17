@echo off
rem Opens Povtori FM in Chrome or Edge. Keep this file next to "Povtori FM.html".
setlocal
set "PAGE=%~dp0Povtori FM.html"
if not exist "%PAGE%" goto missing
reg query "HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if not errorlevel 1 goto chrome
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" >nul 2>&1
if not errorlevel 1 goto chrome
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe" /reg:32 >nul 2>&1
if not errorlevel 1 goto chrome
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" >nul 2>&1
if not errorlevel 1 goto edge
reg query "HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\App Paths\msedge.exe" /reg:32 >nul 2>&1
if not errorlevel 1 goto edge
start "" "%PAGE%"
exit /b 0
:chrome
start "" chrome "%PAGE%"
exit /b 0
:edge
start "" msedge "%PAGE%"
exit /b 0
:missing
echo.
echo   Povtori FM.html is not in this folder:
echo   "%~dp0"
echo.
echo   Double-click "Update Povtori FM.cmd" to download the missing files.
echo.
pause
exit /b 1
