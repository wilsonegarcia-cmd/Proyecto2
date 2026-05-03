#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Quick Test para el Proyecto de Control de Acceso Bluetooth
Verifica que todos los componentes estén funcionando correctamente
"""

import os
import sys
import json
import sqlite3

def check_server_files():
    """Verificar que los archivos del servidor existen"""
    print("="*70)
    print("📋 VERIFICANDO ARCHIVOS DEL PROYECTO")
    print("="*70)
    
    base_path = "c:\\Users\\Eduardo Garcia\\Desktop\\Proyecto2"
    files_to_check = {
        "Servidor": [
            "server\\app.py",
            "server\\test_api.py",
            "server\\requirements.txt"
        ],
        "Android": [
            "MainActivity.kt",
            "activity_main.xml",
            "strings.xml",
            "colors.xml"
        ],
        "Android Build": [
            "android\\build.gradle",
            "android\\app\\build.gradle"
        ]
    }
    
    all_good = True
    for category, files in files_to_check.items():
        print(f"\n{category}:")
        for file in files:
            full_path = os.path.join(base_path, file)
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"  ✓ {file} ({size} bytes)")
            else:
                print(f"  ✗ {file} NO ENCONTRADO")
                all_good = False
    
    return all_good

def check_database():
    """Verificar estructura de la base de datos"""
    print("\n" + "="*70)
    print("🗄️  VERIFICANDO BASE DE DATOS")
    print("="*70)
    
    db_path = "c:\\Users\\Eduardo Garcia\\Desktop\\Proyecto2\\server\\access.db"
    
    try:
        # Verificar si existe
        if os.path.exists(db_path):
            print(f"\n✓ Base de datos encontrada: {db_path}")
            
            # Verificar contenido
            conn = sqlite3.connect(db_path)
            c = conn.cursor()
            
            # Verificar tabla usuarios
            c.execute("SELECT COUNT(*) FROM usuarios")
            user_count = c.fetchone()[0]
            print(f"  • Tabla 'usuarios': {user_count} registros")
            
            # Verificar tabla logs
            c.execute("SELECT COUNT(*) FROM logs")
            log_count = c.fetchone()[0]
            print(f"  • Tabla 'logs': {log_count} registros")
            
            # Mostrar usuarios
            c.execute("SELECT token, nombre FROM usuarios")
            users = c.fetchall()
            print(f"  • Usuarios disponibles:")
            for token, nombre in users:
                print(f"    - {token}: {nombre}")
            
            conn.close()
            return True
        else:
            print(f"\n⚠️  Base de datos NO EXISTE: {db_path}")
            print("   Se creará automáticamente al ejecutar app.py")
            return False
            
    except Exception as e:
        print(f"\n✗ Error al verificar BD: {e}")
        return False

def check_python_modules():
    """Verificar que los módulos Python están disponibles"""
    print("\n" + "="*70)
    print("📦 VERIFICANDO MÓDULOS PYTHON")
    print("="*70)
    
    modules = ['flask', 'requests']
    all_available = True
    
    for module in modules:
        try:
            __import__(module)
            print(f"\n✓ {module}: Instalado")
        except ImportError:
            print(f"\n✗ {module}: NO INSTALADO")
            print(f"   Instalar con: pip install {module}")
            all_available = False
    
    return all_available

def check_android_manifest():
    """Verificar permisos en AndroidManifest"""
    print("\n" + "="*70)
    print("🛡️  VERIFICANDO PERMISOS ANDROID")
    print("="*70)
    
    manifest_path = "c:\\Users\\Eduardo Garcia\\Desktop\\Proyecto2\\android\\app\\src\\main\\AndroidManifest.xml"
    
    required_perms = [
        "android.permission.BLUETOOTH",
        "android.permission.BLUETOOTH_ADMIN",
        "android.permission.BLUETOOTH_CONNECT",
        "android.permission.BLUETOOTH_SCAN",
        "android.permission.ACCESS_FINE_LOCATION"
    ]
    
    try:
        if os.path.exists(manifest_path):
            with open(manifest_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            print(f"\n✓ AndroidManifest.xml encontrado")
            print(f"\n  Permisos requeridos:")
            
            for perm in required_perms:
                if perm in content:
                    print(f"    ✓ {perm}")
                else:
                    print(f"    ⚠️  {perm} (podría faltar)")
            
            return True
        else:
            print(f"\n⚠️  AndroidManifest.xml NO ENCONTRADO (se generará con Android Studio)")
            return False
            
    except Exception as e:
        print(f"\n✗ Error: {e}")
        return False

def generate_report():
    """Generar reporte final"""
    print("\n" + "="*70)
    print("📊 REPORTE FINAL")
    print("="*70)
    
    results = {
        "Archivos": check_server_files(),
        "Base de Datos": check_database(),
        "Módulos Python": check_python_modules(),
    }
    
    completed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print(f"\n✓ Verificaciones completadas: {completed}/{total}")
    
    if completed == total:
        print("\n" + "="*70)
        print("✅ TODO LISTO PARA COMENZAR")
        print("="*70)
        print("""
Próximos pasos:

1. SERVIDOR (5 min):
   cd server
   python app.py
   (en otra terminal) python test_api.py

2. ANDROID (20 min):
   - Descargar Android Studio
   - Crear proyecto "BluetoothAccess"
   - Copiar MainActivity.kt, activity_main.xml, etc.
   - Compilar

3. ESP32 (1 hora):
   - Instalar ESP-IDF v5.1+
   - Copiar código
   - Configurar WiFi
   - Compilar y subir

4. PRUEBAS:
   - Conectar app a ESP32
   - Enviar tokens
   - Verificar LED y buzzer
        """)
    else:
        print("\n⚠️  Hay algunos problemas. Ver arriba para detalles.")
    
    return completed == total

if __name__ == "__main__":
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*15 + "VERIFICACIÓN DEL PROYECTO" + " "*29 + "║")
    print("║" + " "*10 + "Control de Acceso con Bluetooth (ESP32+Android)" + " "*10 + "║")
    print("╚" + "="*68 + "╝")
    print()
    
    try:
        success = generate_report()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n✗ Error durante verificación: {e}")
        sys.exit(1)
