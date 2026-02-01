@echo off
echo === Mighty House SOPs - Quick Sync ===
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0sync.ps1" %*
echo.
pause
