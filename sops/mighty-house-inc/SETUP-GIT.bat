@echo off
echo ================================================
echo Mighty House SOPs - GitHub Repository Setup
echo ================================================
echo.
echo This will:
echo   1. Initialize Git repository
echo   2. Create local backup
echo   3. Push to GitHub (private repo)
echo.
echo Press any key to continue or Ctrl+C to cancel...
pause >nul
echo.
powershell -ExecutionPolicy Bypass -File "%~dp0setup-repo.ps1"
echo.
echo ================================================
echo Setup complete! Press any key to close.
pause >nul
