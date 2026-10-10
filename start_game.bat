@echo off
if exist "%~dp0.venv\Scripts\python.exe" (
    "%~dp0.venv\Scripts\python.exe" "%~dp0main.py" %*
) else (
    py "%~dp0main.py" %*
)
if errorlevel 1 pause
