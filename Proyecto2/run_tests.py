#!/usr/bin/env python3
"""
Script standalone para ejecutar servidor y pruebas automáticamente
"""
import subprocess
import time
import sys
import os
from pathlib import Path

# Cambiar al directorio del servidor
SERVER_DIR = Path(__file__).parent / "server"
os.chdir(SERVER_DIR)

def install_deps():
    """Instalar dependencias"""
    print("\n[*] Instalando dependencias...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests", "--quiet"], 
                      check=True, capture_output=True)
        print("[✓] Dependencias instaladas correctamente")
        return True
    except subprocess.CalledProcessError as e:
        print(f"[✗] Error al instalar: {e}")
        return False

def start_server():
    """Iniciar servidor Flask en background"""
    print("\n[*] Iniciando servidor Flask...")
    try:
        # Iniciar el servidor en background
        process = subprocess.Popen([sys.executable, "app.py"],
                                 stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        time.sleep(3)  # Esperar a que inicie
        
        if process.poll() is None:  # Verificar que sigue corriendo
            print(f"[✓] Servidor iniciado (PID: {process.pid})")
            return process
        else:
            print("[✗] El servidor se cerró inesperadamente")
            return None
    except Exception as e:
        print(f"[✗] Error al iniciar servidor: {e}")
        return None

def run_tests():
    """Ejecutar pruebas"""
    print("\n[*] Ejecutando pruebas...")
    time.sleep(1)
    try:
        result = subprocess.run([sys.executable, "test_api.py"], 
                              capture_output=False, check=False)
        return result.returncode == 0
    except Exception as e:
        print(f"[✗] Error al ejecutar pruebas: {e}")
        return False

def main():
    print("=" * 60)
    print("  SERVIDOR DE CONTROL DE ACCESO - PRUEBAS AUTOMATIZADAS")
    print("=" * 60)
    
    # Instalar dependencias
    if not install_deps():
        sys.exit(1)
    
    # Iniciar servidor
    server = start_server()
    if not server:
        sys.exit(1)
    
    try:
        # Ejecutar pruebas
        success = run_tests()
        
        print("\n" + "=" * 60)
        if success:
            print("  [✓] PRUEBAS COMPLETADAS EXITOSAMENTE")
        else:
            print("  [!] PRUEBAS COMPLETADAS CON ADVERTENCIAS")
        print("=" * 60)
        
    finally:
        # Detener servidor
        print("\n[*] Deteniendo servidor...")
        server.terminate()
        try:
            server.wait(timeout=3)
        except subprocess.TimeoutExpired:
            server.kill()
        print("[✓] Servidor detenido")

if __name__ == "__main__":
    main()
