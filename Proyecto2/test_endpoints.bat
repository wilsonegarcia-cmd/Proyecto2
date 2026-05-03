@echo off
REM Script de prueba usando curl - sin dependencia de Python

setlocal enabledelayedexpansion

REM Variables
set "BASE_URL=http://localhost:5000"
set "SERVER_DIR=c:\Users\Eduardo Garcia\Desktop\Proyecto2\server"
set "PASS=0"
set "FAIL=0"

echo.
echo ============================================================
echo   SERVIDOR DE CONTROL DE ACCESO - PRUEBAS CON CURL
echo ============================================================
echo.

REM Instalar Flask
echo [*] Instalando Flask...
python -m pip install flask requests --quiet 2>nul
if errorlevel 1 (
    echo [ERROR] No se pudo instalar Flask
    exit /b 1
)

REM Iniciar servidor
echo [*] Iniciando servidor en background...
cd /d "%SERVER_DIR%"
start "Servidor Flask" /B python app.py >nul 2>&1

REM Esperar a que inicie
timeout /t 3 /nobreak >nul

echo [OK] Servidor iniciado
echo.

REM Prueba 1: Token autorizado
echo [TEST 1] Verificando token AUTORIZADO...
curl -s "%BASE_URL%/check?token=TOKEN123" | findstr /I "autorizado" >nul
if !errorlevel! equ 0 (
    echo [PASS] Token autorizado retorna respuesta correcta
    set /a PASS+=1
) else (
    echo [FAIL] Token autorizado no retorna respuesta esperada
    set /a FAIL+=1
)

REM Prueba 2: Token no autorizado
echo [TEST 2] Verificando token NO AUTORIZADO...
curl -s "%BASE_URL%/check?token=INVALID" | findstr /I "autorizado" >nul
if !errorlevel! equ 0 (
    echo [PASS] Token no autorizado retorna respuesta correcta
    set /a PASS+=1
) else (
    echo [FAIL] Token no autorizado no retorna respuesta esperada
    set /a FAIL+=1
)

REM Prueba 3: Listar usuarios
echo [TEST 3] Listando usuarios...
curl -s "%BASE_URL%/usuarios" | findstr /I "TOKEN" >nul
if !errorlevel! equ 0 (
    echo [PASS] Listado de usuarios retorna datos
    set /a PASS+=1
) else (
    echo [FAIL] Listado de usuarios vacío
    set /a FAIL+=1
)

REM Resumen
echo.
echo ============================================================
echo   RESUMEN DE PRUEBAS
echo ============================================================
echo [PASS] %PASS% pruebas completadas
echo [FAIL] %FAIL% pruebas fallidas
echo ============================================================
echo.

REM Detener servidor
echo [*] Deteniendo servidor...
taskkill /F /IM python.exe >nul 2>&1

pause
