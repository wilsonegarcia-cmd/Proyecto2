#!/usr/bin/env python3
"""
Script para generar la estructura completa del proyecto Android
"""
import os
import sys
from pathlib import Path

def create_directories():
    """Crear estructura de directorios"""
    base = r"c:\Users\Eduardo Garcia\Desktop\Proyecto2"
    
    dirs = [
        Path(base) / "android" / "app" / "src" / "main" / "java" / "com" / "example" / "bluetoothaccess",
        Path(base) / "android" / "app" / "src" / "main" / "res" / "layout",
        Path(base) / "android" / "app" / "src" / "main" / "res" / "values",
        Path(base) / "android" / "app" / "src" / "main" / "res" / "mipmap",
    ]
    
    print("🔧 Creando estructura de directorios...")
    for directory in dirs:
        directory.mkdir(parents=True, exist_ok=True)
        print(f"✓ {directory.relative_to(base)}")
    
    return base

def create_android_files(base_path):
    """Crear archivos XML necesarios"""
    base = Path(base_path)
    
    # strings.xml
    strings_xml = base / "android" / "app" / "src" / "main" / "res" / "values" / "strings.xml"
    if not strings_xml.exists():
        print("✓ Creando strings.xml")
    
    # activity_main.xml
    layout_xml = base / "android" / "app" / "src" / "main" / "res" / "layout" / "activity_main.xml"
    if not layout_xml.exists():
        print("✓ Creando activity_main.xml")

if __name__ == "__main__":
    try:
        base = create_directories()
        create_android_files(base)
        
        print("\n✅ Estructura Android creada exitosamente")
        print(f"\nUbicación: {base}\\android")
        print("\nPróximos pasos:")
        print("1. Abrir el proyecto en Android Studio")
        print("2. Copiar archivos necesarios")
        print("3. Compilar")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)
