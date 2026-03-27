@echo off
setlocal

cd /d "%~dp0"

echo [RepairPlan] Starting application...

where py >nul 2>nul
if %errorlevel% neq 0 (
  echo [ERROR] Python launcher ^("py"^) was not found.
  echo Install Python for Windows first: https://www.python.org/downloads/
  pause
  exit /b 1
)

if not exist ".venv\Scripts\python.exe" (
  echo [RepairPlan] Creating virtual environment...
  py -3 -m venv .venv
  if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    pause
    exit /b 1
  )
)

echo [RepairPlan] Upgrading pip...
call ".venv\Scripts\python.exe" -m pip install --upgrade pip
if %errorlevel% neq 0 (
  echo [ERROR] Failed to upgrade pip.
  pause
  exit /b 1
)

echo [RepairPlan] Installing requirements...
call ".venv\Scripts\python.exe" -m pip install -r requirements.txt
if %errorlevel% neq 0 (
  echo [ERROR] Failed to install requirements.
  pause
  exit /b 1
)

echo [RepairPlan] Applying migrations...
call ".venv\Scripts\python.exe" manage.py migrate
if %errorlevel% neq 0 (
  echo [ERROR] Migrations failed.
  pause
  exit /b 1
)

echo [RepairPlan] Ensuring role groups exist...
call ".venv\Scripts\python.exe" manage.py seed_roles
if %errorlevel% neq 0 (
  echo [ERROR] Failed to seed roles.
  pause
  exit /b 1
)

echo.
echo [RepairPlan] App is starting at http://127.0.0.1:8000/
echo [RepairPlan] Admin is at http://127.0.0.1:8000/admin/
echo.

call ".venv\Scripts\python.exe" manage.py runserver

endlocal
