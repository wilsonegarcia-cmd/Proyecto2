#!/usr/bin/env python3
"""
Script de prueba para validar los endpoints del servidor de control de acceso
"""
import requests
import json
import time
import sys

BASE_URL = "http://localhost:5000"
MAX_RETRIES = 5
RETRY_DELAY = 2

def print_test(name, status, details=""):
    status_icon = "✓" if status else "✗"
    print(f"\n{status_icon} {name}")
    if details:
        print(f"  └─ {details}")

def test_server():
    print("\n" + "="*60)
    print("  PRUEBA DEL SERVIDOR DE CONTROL DE ACCESO")
    print("="*60)
    
    # Intentar conectar al servidor con reintentos
    print("\n[*] Esperando a que el servidor esté listo...")
    for attempt in range(MAX_RETRIES):
        try:
            response = requests.get(f"{BASE_URL}/usuarios", timeout=2)
            print(f"[✓] Servidor disponible en {BASE_URL}")
            break
        except requests.exceptions.ConnectionError:
            if attempt < MAX_RETRIES - 1:
                print(f"[*] Intento {attempt + 1}/{MAX_RETRIES}... reintentando en {RETRY_DELAY}s")
                time.sleep(RETRY_DELAY)
            else:
                print("\n✗ ERROR: No se puede conectar al servidor.")
                print("  Asegúrate de que el servidor está ejecutándose:")
                print(f"  python app.py")
                sys.exit(1)
    
    try:
        # Test 1: Verificar token autorizado
        print("\n[1/6] Verificando token AUTORIZADO...")
        response = requests.get(f"{BASE_URL}/check?token=TOKEN123")
        data = response.json()
        ok = data.get("autorizado") == True and "nombre" in data
        print_test("GET /check?token=TOKEN123", ok, 
                   f"Respuesta: {json.dumps(data)}")
        
        # Test 2: Verificar token NO autorizado
        print("\n[2/6] Verificando token NO AUTORIZADO...")
        response = requests.get(f"{BASE_URL}/check?token=INVALID")
        data = response.json()
        ok = data.get("autorizado") == False
        print_test("GET /check?token=INVALID", ok,
                   f"Respuesta: {json.dumps(data)}")
        
        # Test 3: Listar usuarios
        print("\n[3/6] Listando usuarios registrados...")
        response = requests.get(f"{BASE_URL}/usuarios")
        users = response.json()
        ok = isinstance(users, list) and len(users) > 0
        print_test("GET /usuarios", ok,
                   f"Usuarios encontrados: {len(users)}")
        print(f"  └─ {json.dumps(users, indent=4)}")
        
        # Test 4: Registrar nuevo usuario
        print("\n[4/6] Registrando nuevo usuario...")
        new_user = {"token": "TOKEN_NUEVO", "nombre": "Usuario Prueba"}
        response = requests.post(f"{BASE_URL}/usuarios", json=new_user)
        data = response.json()
        ok = response.status_code == 200
        print_test("POST /usuarios (nuevo usuario)", ok,
                   f"Respuesta: {json.dumps(data)}")
        
        # Test 5: Registrar evento de acceso
        print("\n[5/6] Registrando evento de acceso...")
        log_data = {
            "token": "TOKEN123",
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "resultado": "GRANTED"
        }
        response = requests.post(f"{BASE_URL}/log", json=log_data)
        data = response.json()
        ok = response.status_code == 200
        print_test("POST /log (evento de acceso)", ok,
                   f"Respuesta: {json.dumps(data)}")
        
        # Test 6: Verificar el nuevo usuario
        print("\n[6/6] Verificando nuevo usuario agregado...")
        response = requests.get(f"{BASE_URL}/check?token=TOKEN_NUEVO")
        data = response.json()
        ok = data.get("autorizado") == True
        print_test("GET /check?token=TOKEN_NUEVO", ok,
                   f"Respuesta: {json.dumps(data)}")
        
        print("\n" + "="*60)
        print("  ✓ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60 + "\n")
        return 0
        
    except requests.exceptions.ConnectionError:
        print("\n✗ ERROR: El servidor no está disponible durante las pruebas.")
        return 1
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        return 1

if __name__ == "__main__":
    exit_code = test_server()
    sys.exit(exit_code)
