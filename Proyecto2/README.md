# 🔐 Proyecto de Control de Acceso con Bluetooth

Sistema de control de acceso que integra ESP32 con Bluetooth Classic, aplicación Android y servidor HTTP.

## 📋 Descripción General

**Flujo del Sistema:**
1. Usuario abre app Android y se empareja con ESP32 vía Bluetooth Classic
2. Envía token de acceso al ESP32
3. ESP32 consulta servidor HTTP para verificar autorización
4. Servidor responde con GRANTED/DENIED
5. ESP32 indica resultado: LED RGB (verde/rojo) + buzzer (corto/largo)
6. Servidor registra el intento con timestamp

## 📁 Estructura del Proyecto

```
Proyecto2/
├── server/              # Servidor HTTP (Flask + SQLite)
│   ├── app.py          # Aplicación Flask
│   ├── requirements.txt # Dependencias
│   ├── test_api.py     # Script de pruebas
│   └── access.db       # Base de datos SQLite (creada automáticamente)
├── esp32/              # Firmware ESP32 (ESP-IDF)
│   └── main/
│       ├── main.c      # Código del microcontrolador
│       └── CMakeLists.txt
├── android/            # App Android (Kotlin)
├── INSTRUCCIONES_PRUEBAS.md
└── README.md
```

## 🚀 Inicio Rápido

### 1️⃣ Servidor HTTP

**Terminal 1 (Servidor):**
```bash
cd server
python -m pip install -r requirements.txt
python app.py
# Se ejecuta en: http://localhost:5000
```

**Terminal 2 (Pruebas):**
```bash
cd server
python test_api.py
```

### 2️⃣ ESP32

1. Instalar [ESP-IDF v5.1+](https://github.com/espressif/esp-idf)
2. Copiar código a `esp32/main/main.c`
3. Configurar credenciales Wi-Fi:
   ```c
   #define SSID "TU_SSID"
   #define PASSWORD "TU_CONTRASENA"
   #define SERVER "http://192.168.1.X:5000"
   ```
4. Compilar y subir:
   ```bash
   idf.py build
   idf.py flash
   idf.py monitor
   ```

### 3️⃣ Aplicación Android

1. Abrir en Android Studio
2. Implementar UI: EditText (token) + Button (conectar) + TextView (respuesta)
3. Agregar permisos en `AndroidManifest.xml`:
   ```xml
   <uses-permission android:name="android.permission.BLUETOOTH"/>
   <uses-permission android:name="android.permission.BLUETOOTH_ADMIN"/>
   <uses-permission android:name="android.permission.BLUETOOTH_CONNECT"/>
   <uses-permission android:name="android.permission.BLUETOOTH_SCAN"/>
   <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION"/>
   ```
4. Compilar e instalar en dispositivo

## 📡 API del Servidor

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| GET | `/check?token={TOKEN}` | Verifica si token está autorizado |
| POST | `/log` | Registra intento de acceso |
| GET | `/usuarios` | Lista todos los usuarios |
| POST | `/usuarios` | Registra nuevo usuario |

**Ejemplos:**

```bash
# Verificar token autorizado
curl "http://localhost:5000/check?token=TOKEN123"
# {"autorizado": true, "nombre": "Usuario Autorizado"}

# Registrar evento
curl -X POST http://localhost:5000/log \
  -H "Content-Type: application/json" \
  -d '{"token":"TOKEN123","timestamp":"2024-01-01 10:30:45","resultado":"GRANTED"}'

# Agregar usuario
curl -X POST http://localhost:5000/usuarios \
  -H "Content-Type: application/json" \
  -d '{"token":"TOKEN456","nombre":"Nuevo Usuario"}'
```

## 🔧 Configuración Importante

### ESP32
- **GPIO 25**: LED Rojo (220Ω)
- **GPIO 26**: LED Verde (220Ω)
- **GPIO 27**: LED Azul (220Ω)
- **GPIO 32**: Buzzer (+)
- **GND**: LED Común (ánodo), Buzzer (-)
- **Wi-Fi & Bluetooth**: Comparten radio 2.4GHz (BR/EDR Only recomendado)

### Android
- **UUID SPP**: `00001101-0000-1000-8000-00805F9B34FB`
- **Operaciones Bluetooth**: Usar Coroutines (Dispatchers.IO) o AsyncTask
- **Permisos**: Requeridos en runtime (Android 6.0+)

### Servidor
- **Host**: 0.0.0.0 (accesible desde cualquier interfaz)
- **Puerto**: 5000 (configurable)
- **Base de datos**: SQLite (access.db)

## ✅ Pruebas del Sistema

Ver: [`INSTRUCCIONES_PRUEBAS.md`](INSTRUCCIONES_PRUEBAS.md)

**Resumen:**
1. ✓ Token autorizado → LED verde + beep corto
2. ✓ Token no autorizado → LED rojo + beep largo
3. ✓ Logs registrados en base de datos
4. ✓ Rango de operación (1-15m)
5. ✓ Tolerancia a desconexión de red

## 📚 Documentación de Referencia

- Manual de prácticas: `ManualPracticas_RedesInalambricas (1).pdf`
- Código base: https://github.com/fabianastudillo/RI-practicas
- ESP-IDF: https://docs.espressif.com/projects/esp-idf
- Android Bluetooth: https://developer.android.com/guide/topics/connectivity/bluetooth

## 🛠️ Dependencias

| Componente | Versión | Descripción |
|-----------|---------|------------|
| Python | 3.7+ | Runtime |
| Flask | 2.x+ | Framework web |
| ESP-IDF | 5.1+ | SDK para ESP32 |
| Android API | 21+ | Mínimo para app |
| Kotlin | 1.x+ | Lenguaje Android |

## 📝 Notas

- La base de datos se crea automáticamente en la primera ejecución
- Usuarios por defecto: `TOKEN123` (autorizado), `INVALID` (no autorizado)
- La IP del servidor debe ser accesible desde la red Wi-Fi del ESP32
- Bluetooth requiere emparejamiento en primera conexión
- El token debe terminar con `\n` al enviar desde ESP32

## 👤 Autores

- Desarrollo: [Tu Nombre]
- Manual de referencia: Fabian Astudillo (RI-practicas)
- Universidad de Cuenca