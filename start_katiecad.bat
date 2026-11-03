@echo off
rem Starts KatieCAD with the automation bridge on (for the MCP server).
rem First run: creates .venv and installs the dependencies.
setlocal
cd /d "%~dp0"

if exist ".venv\Scripts\python.exe" goto run

rem Find a Python 3.10+ (the default "python" here may be too old).
set "PY="
for %%V in (313 312 311 310) do (
  if not defined PY if exist "%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe" set "PY=%LOCALAPPDATA%\Programs\Python\Python%%V\python.exe"
)
if not defined PY set "PY=python"
"%PY%" -c "import sys, tkinter; sys.exit(0 if sys.version_info >= (3, 10) else 1)"
if errorlevel 1 (
  echo Need Python 3.10 or newer with tkinter. Install it from python.org and re-run.
  pause
  exit /b 1
)

echo Setting up .venv ...
"%PY%" -m venv .venv || goto fail
".venv\Scripts\python.exe" -m pip install -q -r requirements.txt -r mcp_server\requirements.txt || goto fail

:run
".venv\Scripts\python.exe" main.py --bridge
if errorlevel 1 pause
exit /b 0

:fail
echo Setup failed.
pause
exit /b 1
