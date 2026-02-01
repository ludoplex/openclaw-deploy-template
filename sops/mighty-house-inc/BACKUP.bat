@echo off
echo === Mighty House SOPs - Local Backup ===
echo.

set TIMESTAMP=%DATE:~10,4%-%DATE:~4,2%-%DATE:~7,2%_%TIME:~0,2%%TIME:~3,2%
set TIMESTAMP=%TIMESTAMP: =0%
set BACKUP_DIR=%USERPROFILE%\Backups
set BACKUP_FILE=%BACKUP_DIR%\mighty-house-sops-%TIMESTAMP%.zip

if not exist "%BACKUP_DIR%" mkdir "%BACKUP_DIR%"

echo Creating backup: %BACKUP_FILE%
echo.

powershell -Command "Compress-Archive -Path '%~dp0*' -DestinationPath '%BACKUP_FILE%' -Force"

if %ERRORLEVEL% EQU 0 (
    echo.
    echo Backup created successfully!
    echo Location: %BACKUP_FILE%
) else (
    echo.
    echo Backup failed!
)

echo.
pause
