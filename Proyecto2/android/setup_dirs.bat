@echo off
REM Crear estructura de directorios para Android

cd /d "c:\Users\Eduardo Garcia\Desktop\Proyecto2\android"

REM Crear estructura de directorios
echo Creando estructura de directorios...

md app\src\main\java\com\example\bluetoothaccess 2>nul
md app\src\main\res\layout 2>nul
md app\src\main\res\values 2>nul
md app\src\main\res\mipmap 2>nul
md app\src\test\java\com\example\bluetoothaccess 2>nul
md app\src\androidTest\java\com\example\bluetoothaccess 2>nul

echo.
echo ✓ Estructura creada exitosamente
echo.
echo Directorios creados:
echo - app/src/main/java/com/example/bluetoothaccess/
echo - app/src/main/res/layout/
echo - app/src/main/res/values/
echo.
