@echo off
REM Script para iniciar el servidor y ejecutar pruebas

cd /d "%~dp0"

echo.
echo ==========================================================
echo   CONTROL DE ACCESO - INICIADOR DEL SERVIDOR
echo ==========================================================
echo.

REM Instalar Flask si no está instalado
echo [*] Verificando dependencias...
python -m pip install flask requests --quiet 2>nul
if errorlevel 1 (
    echo [!] Error al instalar dependencias
    exit /b 1
)

echo [+] Flask y requests instalados
echo.

REM Iniciar servidor en background
echo [*] Iniciando servidor Flask...
start "Flask Server" cmd /k "python app.py"

REM Esperar a que el servidor inicie
timeout /t 3 /nobreak

echo [+] Servidor iniciado en http://localhost:5000
echo.
echo [*] Ejecutando pruebas de API...
echo.

REM Ejecutar pruebas
python test_api.py

echo.
echo [+] Presiona Enter para cerrar esta ventana...
pause >nul
