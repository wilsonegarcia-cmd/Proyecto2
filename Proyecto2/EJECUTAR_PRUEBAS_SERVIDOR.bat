@echo off
REM Script para ejecutar pruebas del servidor - Windows
REM Ejecuta las 6 pruebas de la API

chcp 65001 > nul
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          PRUEBAS AUTOMÁTICAS - SERVIDOR FLASK                ║
echo ║              (Ejecutar en otra terminal)                      ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d "c:\Users\Eduardo Garcia\Desktop\Proyecto2\server"

echo Esperando a que el servidor esté listo...
timeout /t 3

echo.
echo ════════════════════════════════════════════════════════════════
echo Ejecutando 6 pruebas de API...
echo ════════════════════════════════════════════════════════════════
echo.

python test_api.py

echo.
echo ════════════════════════════════════════════════════════════════
pause
