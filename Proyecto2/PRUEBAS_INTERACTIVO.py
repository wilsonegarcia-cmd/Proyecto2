#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script Interactivo de Pruebas - Sistema de Control de Acceso Bluetooth
Permite probar el servidor sin necesidad de usar curl manualmente
"""

import subprocess
import time
import os
import sys
import json

def print_header(title):
    print("\n" + "="*70)
    print("  " + title)
    print("="*70 + "\n")

def print_step(step_num, title):
    print(f"\n🔹 PASO {step_num}: {title}")
    print("-" * 70)

def install_dependencies():
    """Instalar Flask y requests"""
    print_header("INSTALANDO DEPENDENCIAS")
    
    modules = ['flask', 'requests']
    for module in modules:
        print(f"📦 Instalando {module}...", end=" ", flush=True)
        try:
            result = subprocess.run(
                [sys.executable, '-m', 'pip', 'install', module, '--quiet'],
                capture_output=True,
                timeout=60
            )
            if result.returncode == 0:
                print("✓")
            else:
                print("✗")
                return False
        except Exception as e:
            print(f"✗ Error: {e}")
            return False
    
    print("\n✅ Todas las dependencias instaladas\n")
    return True

def start_server():
    """Iniciar servidor en background"""
    print_header("INICIANDO SERVIDOR FLASK")
    
    server_path = r"c:\Users\Eduardo Garcia\Desktop\Proyecto2\server\app.py"
    
    try:
        # Cambiar a la carpeta del servidor
        os.chdir(r"c:\Users\Eduardo Garcia\Desktop\Proyecto2\server")
        
        # Iniciar servidor
        process = subprocess.Popen(
            [sys.executable, 'app.py'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        print("⏳ Esperando a que el servidor inicie...")
        time.sleep(3)
        
        if process.poll() is None:  # Process está corriendo
            print("✅ Servidor iniciado en http://localhost:5000")
            print("\n📋 El servidor está corriendo en background.")
            print("   Se ejecutarán las pruebas ahora...\n")
            return process
        else:
            print("✗ Error al iniciar servidor")
            return None
            
    except Exception as e:
        print(f"✗ Error: {e}")
        return None

def run_tests():
    """Ejecutar test_api.py"""
    print_header("EJECUTANDO PRUEBAS AUTOMÁTICAS")
    
    try:
        result = subprocess.run(
            [sys.executable, 'test_api.py'],
            capture_output=True,
            timeout=30,
            text=True
        )
        
        print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        return result.returncode == 0
        
    except Exception as e:
        print(f"✗ Error ejecutando pruebas: {e}")
        return False

def test_endpoint_manual(endpoint, method='GET', data=None, description=""):
    """Probar un endpoint manualmente"""
    import requests
    
    base_url = "http://localhost:5000"
    full_url = base_url + endpoint
    
    print(f"\n📍 {description}")
    print(f"   Endpoint: {method} {endpoint}")
    
    try:
        if method == 'GET':
            response = requests.get(full_url, timeout=5)
        elif method == 'POST':
            response = requests.post(
                full_url,
                json=data,
                headers={'Content-Type': 'application/json'},
                timeout=5
            )
        
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        return response.status_code == 200
        
    except Exception as e:
        print(f"   ✗ Error: {e}")
        return False

def interactive_menu():
    """Menú interactivo para pruebas manuales"""
    print_header("PRUEBAS MANUALES DE ENDPOINTS")
    
    import requests
    
    while True:
        print("\n📌 OPCIONES DE PRUEBA:")
        print("  1. Verificar token válido (TOKEN123)")
        print("  2. Verificar token inválido (INVALID)")
        print("  3. Listar todos los usuarios")
        print("  4. Agregar nuevo usuario")
        print("  5. Registrar evento de acceso")
        print("  6. Volver al menú principal")
        print("  0. Salir")
        
        choice = input("\n👉 Selecciona una opción (0-6): ").strip()
        
        if choice == '1':
            test_endpoint_manual(
                "/check?token=TOKEN123",
                description="Verificar token válido (TOKEN123)"
            )
        
        elif choice == '2':
            test_endpoint_manual(
                "/check?token=INVALID",
                description="Verificar token inválido (INVALID)"
            )
        
        elif choice == '3':
            test_endpoint_manual(
                "/usuarios",
                description="Listar todos los usuarios"
            )
        
        elif choice == '4':
            token = input("\n¿Qué token? (ej: TEST_TOKEN): ").strip()
            nombre = input("¿Qué nombre? (ej: Mi Usuario): ").strip()
            
            test_endpoint_manual(
                "/usuarios",
                method='POST',
                data={"token": token, "nombre": nombre},
                description=f"Agregar usuario: {nombre}"
            )
        
        elif choice == '5':
            token = input("\n¿Qué token? (ej: TOKEN123): ").strip()
            resultado = input("¿Resultado? (GRANTED/DENIED): ").strip()
            
            test_endpoint_manual(
                "/log",
                method='POST',
                data={
                    "token": token,
                    "timestamp": "2026-05-03T19:30:00Z",
                    "resultado": resultado
                },
                description=f"Registrar evento: {token} → {resultado}"
            )
        
        elif choice == '6':
            break
        
        elif choice == '0':
            print("\n👋 Saliendo...\n")
            sys.exit(0)
        
        else:
            print("❌ Opción no válida")

def main_menu():
    """Menú principal"""
    while True:
        print("\n" + "="*70)
        print("       🧪 PRUEBAS - SISTEMA DE CONTROL DE ACCESO BLUETOOTH")
        print("="*70)
        
        print("\n📌 OPCIONES:")
        print("  1. Instalar dependencias")
        print("  2. Iniciar servidor y ejecutar pruebas automáticas")
        print("  3. Pruebas manuales de endpoints")
        print("  4. Ver estado del servidor")
        print("  0. Salir")
        
        choice = input("\n👉 Selecciona una opción (0-4): ").strip()
        
        if choice == '1':
            install_dependencies()
        
        elif choice == '2':
            print("\n⚠️  Importante:")
            print("  • Se abrirá el servidor en background")
            print("  • Se ejecutarán 6 pruebas automáticas")
            print("  • El servidor seguirá corriendo para pruebas manuales")
            
            input("\n👉 Presiona Enter para continuar...")
            
            if install_dependencies():
                server = start_server()
                if server:
                    success = run_tests()
                    if success:
                        print("\n✅ ¡TODAS LAS PRUEBAS PASARON!")
                        print("\nℹ️  El servidor sigue corriendo.")
                        print("    Para detener: Cierra esta ventana o presiona Ctrl+C")
                        
                        try:
                            input("\n👉 Presiona Enter para volver al menú...")
                        except KeyboardInterrupt:
                            print("\n\n👋 Deteniendo...\n")
                            server.terminate()
                            sys.exit(0)
                    else:
                        print("\n❌ Algunas pruebas fallaron")
                        server.terminate()
        
        elif choice == '3':
            interactive_menu()
        
        elif choice == '4':
            import requests
            try:
                response = requests.get("http://localhost:5000/usuarios", timeout=2)
                if response.status_code == 200:
                    print("\n✅ Servidor está corriendo")
                    print(f"   Usuarios en BD: {len(response.json())}")
                else:
                    print("\n❌ Servidor respondió con error")
            except:
                print("\n❌ Servidor NO está corriendo")
                print("   Ejecuta opción 2 para iniciar")
        
        elif choice == '0':
            print("\n👋 Hasta luego!\n")
            sys.exit(0)
        
        else:
            print("❌ Opción no válida")

if __name__ == "__main__":
    try:
        print("\n")
        print("╔" + "="*68 + "╗")
        print("║" + " "*20 + "🧪 PRUEBAS DEL PROYECTO" + " "*25 + "║")
        print("║" + " "*10 + "Control de Acceso con Bluetooth" + " "*27 + "║")
        print("╚" + "="*68 + "╝")
        print()
        
        main_menu()
        
    except KeyboardInterrupt:
        print("\n\n👋 Interrupción del usuario. Saliendo...\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}\n")
        sys.exit(1)
