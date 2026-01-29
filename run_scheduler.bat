@echo off
REM Automated Daily Stock Monitor Snapshot Runner
REM This script is designed to be run by Windows Task Scheduler

cd /d "C:\Users\User\.gemini\antigravity\scratch\stock_monitor"

echo [%date% %time%] Running daily stock monitor snapshot...
"C:\Users\User\miniconda3\python.exe" scheduler.py >> logs\scheduler.log 2>&1

if %ERRORLEVEL% EQU 0 (
    echo [%date% %time%] Snapshot completed successfully
) else (
    echo [%date% %time%] Snapshot failed with error code %ERRORLEVEL%
)
