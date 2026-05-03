#!/usr/bin/env python3
"""
Script para generar la estructura completa del proyecto Android
"""
import os
from pathlib import Path

# Rutas base
BASE_DIR = r"c:\Users\Eduardo Garcia\Desktop\Proyecto2\android"
MAIN_DIR = Path(BASE_DIR) / "app" / "src" / "main"
JAVA_DIR = MAIN_DIR / "java" / "com" / "example" / "bluetoothaccess"
RES_DIR = MAIN_DIR / "res"

# Crear directorios
directories = [
    JAVA_DIR,
    RES_DIR / "layout",
    RES_DIR / "values",
    RES_DIR / "mipmap",
    MAIN_DIR / "../test/java/com/example/bluetoothaccess",
    MAIN_DIR / "../androidTest/java/com/example/bluetoothaccess",
]

print("Creando estructura de directorios...")
for dir_path in directories:
    dir_path.mkdir(parents=True, exist_ok=True)
    print(f"✓ {dir_path}")

print("\n✓ Estructura de directorios creada exitosamente")
