@echo off
title NOVA Server Launcher
echo ========================================================
echo       STARTING PROJECT NOVA (CORE HUB + WEB)
echo ========================================================
cd /d "C:\Project\Nova"

echo Starting NOVA Core Backend on port 8000...
start "NOVA Core Backend" cmd /k "cd services\core && ..\..\services\core\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8000 --reload"

echo Starting NOVA Web Client on port 3000...
start "NOVA Web Client" cmd /k "pnpm.cmd --filter @nova/web dev"

echo.
echo ========================================================
echo Backend Core: http://localhost:8000/health
echo Frontend Web: http://localhost:3000
echo ========================================================
pause
