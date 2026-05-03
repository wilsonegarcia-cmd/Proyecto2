import subprocess
import sys
import os
import time

os.chdir(r'c:\Users\Eduardo Garcia\Desktop\Proyecto2\server')

print("Instalando dependencias...")
subprocess.run([sys.executable, "-m", "pip", "install", "flask", "requests", "--quiet"])

print("Iniciando servidor...")
server = subprocess.Popen([sys.executable, "app.py"])
time.sleep(3)

print("Ejecutando pruebas...")
subprocess.run([sys.executable, "test_api.py"])

print("Deteniendo servidor...")
server.terminate()
