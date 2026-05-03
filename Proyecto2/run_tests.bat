@echo off
setlocal enabledelayedexpansion

cd /d "c:\Users\Eduardo Garcia\Desktop\Proyecto2\server"

echo.
echo ============================================================
echo   SERVIDOR DE CONTROL DE ACCESO - PRUEBAS
echo ============================================================
echo.

REM Instalar dependencias
echo [*] Instalando dependencias...
python -m pip install flask requests --quiet
if errorlevel 1 (
    echo [ERROR] Fallo al instalar dependencias
    exit /b 1
)
echo [OK] Dependencias instaladas

REM Iniciar servidor en background
echo.
echo [*] Iniciando servidor Flask en background...
start "" /B python app.py >server.log 2>&1
set SERVER_PID=%ERRORLEVEL%
echo [OK] Servidor iniciado (PID: !SERVER_PID!)

REM Esperar a que el servidor inicie
timeout /t 3 /nobreak >nul

REM Ejecutar pruebas
echo.
echo [*] Ejecutando pruebas de API...
echo.

python test_api.py

set TEST_RESULT=%ERRORLEVEL%

echo.
echo [*] Deteniendo servidor...
taskkill /F /IM python.exe >nul 2>&1

echo.
echo ============================================================
if !TEST_RESULT! equ 0 (
    echo   [OK] Todas las pruebas completadas exitosamente
) else (
    echo   [ERROR] Algunas pruebas fallaron
)
echo ============================================================
echo.
pause
