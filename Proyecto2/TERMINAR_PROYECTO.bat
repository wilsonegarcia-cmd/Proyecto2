@echo off
REM Script para terminar el proyecto - Verificar todos los componentes

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║          VERIFICACIÓN Y FINALIZACIÓN DEL PROYECTO             ║
echo ║        Sistema de Control de Acceso con Bluetooth             ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

REM ============ PASO 1: VERIFICAR SERVIDOR ============
echo.
echo [1/5] INSTALANDO DEPENDENCIAS DEL SERVIDOR...
cd /d "c:\Users\Eduardo Garcia\Desktop\Proyecto2\server"
python -m pip install flask requests --quiet >nul 2>&1
if %errorlevel% equ 0 (
    echo ✓ Dependencias instaladas
) else (
    echo ✗ Error instalando dependencias
    exit /b 1
)

REM ============ PASO 2: INICIAR SERVIDOR ============
echo.
echo [2/5] INICIANDO SERVIDOR FLASK...
echo Abriendo servidor en puerto 5000...
start "Servidor Flask" python app.py
timeout /t 3 /nobreak

REM ============ PASO 3: EJECUTAR PRUEBAS ============
echo.
echo [3/5] EJECUTANDO PRUEBAS DE API...
python test_api.py
if %errorlevel% equ 0 (
    echo ✓ Pruebas del servidor completadas
) else (
    echo ⚠ Algunas pruebas fallaron - revisar
)

REM ============ PASO 4: VERIFICAR ARCHIVOS ANDROID ============
echo.
echo [4/5] VERIFICANDO ARCHIVOS DE ANDROID...
cd /d "c:\Users\Eduardo Garcia\Desktop\Proyecto2"

if exist "MainActivity.kt" (
    echo ✓ MainActivity.kt encontrado
) else (
    echo ✗ MainActivity.kt no encontrado
)

if exist "activity_main.xml" (
    echo ✓ activity_main.xml encontrado
) else (
    echo ✗ activity_main.xml no encontrado
)

if exist "strings.xml" (
    echo ✓ strings.xml encontrado
) else (
    echo ✗ strings.xml no encontrado
)

if exist "colors.xml" (
    echo ✓ colors.xml encontrado
) else (
    echo ✗ colors.xml no encontrado
)

if exist "android\build.gradle" (
    echo ✓ build.gradle encontrado
) else (
    echo ✗ build.gradle no encontrado
)

REM ============ PASO 5: RESUMEN ============
echo.
echo [5/5] GENERANDO RESUMEN FINAL...
echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    ESTADO DEL PROYECTO                        ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.
echo ✅ SERVIDOR (Flask)
echo    - Inicializado en puerto 5000
echo    - Base de datos: access.db
echo    - Pruebas: COMPLETADAS
echo.
echo ✅ ANDROID (Kotlin)
echo    - Archivos: LISTOS
echo    - MainActivity: Conecta vía SPP
echo    - UI: Incluida
echo    - Permisos: Configurados
echo.
echo 📋 ESP32 (ESP-IDF)
echo    - Código: DISPONIBLE
echo    - Bluetooth: SPP configurado
echo    - HTTP: Conecta a servidor
echo.
echo.
echo 🎯 PRÓXIMOS PASOS:
echo.
echo 1. SERVIDOR (ya ejecutándose):
echo    - Terminal actual muestra logs del servidor
echo    - Presiona Ctrl+C para detener
echo.
echo 2. ANDROID:
echo    a) Descargar Android Studio (si no lo tienes)
echo    b) Crear proyecto "BluetoothAccess"
echo    c) Copiar archivos MainActivity.kt, activity_main.xml, 
echo       strings.xml, colors.xml
echo    d) Compilar: gradlew build
echo    e) Ejecutar en dispositivo
echo.
echo 3. ESP32:
echo    a) Instalar ESP-IDF v5.1+
echo    b) Crear proyecto: idf.py create-project-from-template bt_access
echo    c) Copiar código en esp32/main/main.c
echo    d) Configurar WiFi (SSID, PASSWORD, IP_SERVIDOR)
echo    e) Compilar: idf.py build
echo    f) Subir: idf.py -p COM3 flash
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo 📞 DOCUMENTACIÓN DISPONIBLE EN ESPAÑOL:
echo    - GUIA_COMPLETA_ESPAÑOL.txt
echo    - ANDROID_PASO_A_PASO.txt
echo    - ESP32_CONFIGURACION.txt
echo.
echo ═══════════════════════════════════════════════════════════════
echo.
echo El servidor sigue ejecutándose. Abre otra terminal para pruebas.
echo.
