@echo off
REM Script para pruebas del servidor - Windows
REM Ejecuta: python -m pip install flask requests, luego inicia el servidor

chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║        PRUEBAS DEL SISTEMA - CONTROL DE ACCESO BLUETOOTH     ║
echo ║                      FASE 1: SERVIDOR                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

REM ============ PASO 1: INSTALAR DEPENDENCIAS ============
echo [PASO 1/3] Instalando dependencias...
echo.

cd /d "c:\Users\Eduardo Garcia\Desktop\Proyecto2\server"

echo - Instalando Flask...
python -m pip install flask --quiet
if %errorlevel% neq 0 (
    echo ✗ Error instalando Flask
    goto error
)
echo ✓ Flask instalado

echo - Instalando requests...
python -m pip install requests --quiet
if %errorlevel% neq 0 (
    echo ✗ Error instalando requests
    goto error
)
echo ✓ Requests instalado

echo.

REM ============ PASO 2: INICIAR SERVIDOR ============
echo [PASO 2/3] Iniciando servidor Flask...
echo.
echo ⏳ El servidor se iniciará en http://localhost:5000
echo ⏳ Presiona Ctrl+C en esta ventana para detener el servidor
echo ⏳ Abre OTRA VENTANA/TERMINAL para las pruebas
echo.
echo ════════════════════════════════════════════════════════════════
echo.

timeout /t 2

python app.py

goto end

:error
echo.
echo ✗ Hubo un error. Verifica la instalación de Python.
exit /b 1

:end
echo.
echo ════════════════════════════════════════════════════════════════
echo Servidor detenido.
pause
