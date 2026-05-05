@echo off
echo.
echo ========================================
echo   Aurora 4x Dashboard Generator
echo ========================================
echo.

set SCRIPT_DASH="%~dp0aurora_reader.py"
set SCRIPT_MIN="%~dp0aurora_minerals.py"
set DB="%~dp0AuroraDB.db"

if not exist "%~dp0AuroraDB.db" (
    echo AuroraDB.db not found.
    echo Enter DB path:
    set /p DB="DB path: "
)

echo [1/2] Generating dashboard...
py %SCRIPT_DASH% %DB% 2>nul
if %errorlevel% neq 0 (
    python3 %SCRIPT_DASH% %DB% 2>nul
    if %errorlevel% neq 0 (
        python %SCRIPT_DASH% %DB%
    )
)

echo.
echo [2/2] Generating mineral viewer...
py %SCRIPT_MIN% %DB% 2>nul
if %errorlevel% neq 0 (
    python3 %SCRIPT_MIN% %DB% 2>nul
    if %errorlevel% neq 0 (
        python %SCRIPT_MIN% %DB%
    )
)

echo.
echo Done! Open aurora_dashboard.html and aurora_minerals.html in your browser.
echo.
pause
