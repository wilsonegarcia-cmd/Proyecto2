# 📱 Guía Completa: Aplicación Android - Control de Acceso Bluetooth

## 📋 Estructura del Proyecto Android

```
android/
├── build.gradle                              (configuración root)
├── settings.gradle
├── gradlew, gradlew.bat
│
└── app/
    ├── build.gradle                          (configuración app)
    ├── proguard-rules.pro
    │
    └── src/
        ├── main/
        │   ├── AndroidManifest.xml           (permisos y activities)
        │   │
        │   ├── java/com/example/bluetoothaccess/
        │   │   ├── MainActivity.kt            (lógica Bluetooth)
        │   │   ├── BluetoothManager.kt        (helper opcional)
        │   │   └── ...
        │   │
        │   └── res/
        │       ├── layout/
        │       │   └── activity_main.xml      (UI)
        │       ├── values/
        │       │   ├── strings.xml            (cadenas de texto)
        │       │   ├── colors.xml             (colores)
        │       │   └── themes/
        │       │       └── styles.xml
        │       └── mipmap/
        │           └── ic_launcher.png
        │
        ├── test/java/...                      (pruebas unitarias)
        └── androidTest/java/...               (pruebas de instrumentación)
```

---

## 🚀 INSTALACIÓN RÁPIDA (5 minutos)

### 1. Requisitos
- Android Studio (versión 2021.3+)
- SDK de Android 31+ 
- Kotlin plugin instalado
- Gradle 7.0+

### 2. Crear proyecto base en Android Studio

```
File → New → New Android Project

Name: BluetoothAccess
Package name: com.example.bluetoothaccess
Save location: c:\Users\Eduardo Garcia\Desktop\Proyecto2\android
Language: Kotlin
Minimum API level: 21 (Android 5.0)
```

### 3. Copiar archivos generados

Después de crear el proyecto, reemplaza los siguientes archivos:

---

## 📄 ARCHIVOS A CREAR/MODIFICAR

### 1. `app/build.gradle`

```gradle
plugins {
    id 'com.android.application'
    id 'org.jetbrains.kotlin.android'
}

android {
    namespace 'com.example.bluetoothaccess'
    compileSdk 33

    defaultConfig {
        applicationId "com.example.bluetoothaccess"
        minSdk 21
        targetSdk 33
        versionCode 1
        versionName "1.0.0"

        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
    }

    buildTypes {
        release {
            minifyEnabled false
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }

    compileOptions {
        sourceCompatibility JavaVersion.VERSION_11
        targetCompatibility JavaVersion.VERSION_11
    }

    kotlinOptions {
        jvmTarget = '11'
    }

    buildFeatures {
        viewBinding true
    }
}

dependencies {
    // Android Core
    implementation 'androidx.core:core-ktx:1.10.0'
    implementation 'androidx.appcompat:appcompat:1.6.1'
    implementation 'com.google.android.material:material:1.8.0'
    implementation 'androidx.constraintlayout:constraintlayout:2.1.4'

    // Lifecycle
    implementation 'androidx.lifecycle:lifecycle-runtime-ktx:2.5.1'
    implementation 'androidx.activity:activity-ktx:1.7.0'
    implementation 'androidx.fragment:fragment-ktx:1.5.1'

    // Coroutines
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-core:1.6.4'
    implementation 'org.jetbrains.kotlinx:kotlinx-coroutines-android:1.6.4'

    // Testing
    testImplementation 'junit:junit:4.13.2'
    androidTestImplementation 'androidx.test.ext:junit:1.1.5'
    androidTestImplementation 'androidx.test.espresso:espresso-core:3.5.1'
}
```

---

### 2. `app/src/main/AndroidManifest.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools">

    <!-- Bluetooth Permissions -->
    <uses-permission android:name="android.permission.BLUETOOTH" />
    <uses-permission android:name="android.permission.BLUETOOTH_ADMIN" />
    <uses-permission android:name="android.permission.BLUETOOTH_CONNECT" />
    <uses-permission android:name="android.permission.BLUETOOTH_SCAN" />
    
    <!-- Location Permission -->
    <uses-permission android:name="android.permission.ACCESS_FINE_LOCATION" />
    <uses-permission android:name="android.permission.ACCESS_COARSE_LOCATION" />

    <application
        android:allowBackup="true"
        android:dataExtractionRules="@xml/data_extraction_rules"
        android:fullBackupContent="@xml/backup_rules"
        android:icon="@mipmap/ic_launcher"
        android:label="@string/app_name"
        android:supportsRtl="true"
        android:theme="@style/Theme.BluetoothAccess"
        tools:targetApi="31">

        <activity
            android:name=".MainActivity"
            android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
        </activity>

    </application>

</manifest>
```

---

### 3. `app/src/main/res/values/strings.xml`

```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <string name="app_name">Bluetooth Access</string>
    <string name="app_title">🔐 Control de Acceso Bluetooth</string>
    
    <!-- Buttons -->
    <string name="btn_scan">Buscar Dispositivos</string>
    <string name="btn_connect">Conectar</string>
    <string name="btn_request_access">Solicitar Acceso</string>
    <string name="btn_disconnect">Desconectar</string>
    
    <!-- Status -->
    <string name="connected">✓ Conectado</string>
    <string name="disconnected">✗ Desconectado</string>
    <string name="connecting">Conectando...</string>
    <string name="sending_token">Enviando token...</string>
    <string name="access_granted">✓ ACCESO CONCEDIDO</string>
    <string name="access_denied">✗ ACCESO DENEGADO</string>
    <string name="unknown_response">? Respuesta desconocida</string>
    
    <!-- Labels -->
    <string name="available_devices">Dispositivos Disponibles:</string>
    <string name="token_label">Token de Acceso:</string>
    <string name="response_label">Respuesta del Servidor:</string>
    
    <!-- Messages -->
    <string name="no_device_selected">No hay dispositivo seleccionado</string>
    <string name="scanning">Escaneando...</string>
    <string name="scanning_devices">Buscando dispositivos Bluetooth...</string>
    <string name="no_devices_found">No se encontraron dispositivos</string>
    <string name="no_bluetooth">Este dispositivo no tiene Bluetooth</string>
    <string name="permissions_required">Se requieren permisos de Bluetooth</string>
    <string name="select_device">Por favor selecciona un dispositivo</string>
    <string name="enter_token">Por favor ingresa un token</string>
    <string name="not_connected">No está conectado</string>
    <string name="connection_error">Error de conexión: </string>
    <string name="connection_failed">Falló la conexión</string>
    <string name="connected_to_device">Conectado a: </string>
    <string name="send_error">Error al enviar</string>
    <string name="send_failed">Falló el envío</string>
    <string name="disconnect_error">Error al desconectar</string>
    <string name="disconnected">Desconectado</string>
    <string name="error_colon">Error: </string>
</resources>
```

---

### 4. `app/src/main/res/layout/activity_main.xml`

Ver el archivo XML en `android/app/src/main/res/layout/activity_main.xml`

---

### 5. `app/src/main/java/com/example/bluetoothaccess/MainActivity.kt`

Copiar del archivo `MainActivity.kt` generado.

---

## 🔧 CONFIGURACIÓN E INSTALACIÓN

### Paso 1: Preparar estructura
```bash
cd c:\Users\Eduardo Garcia\Desktop\Proyecto2\android
python setup_android.py
```

### Paso 2: Abrir en Android Studio
1. File → Open
2. Seleccionar: `c:\Users\Eduardo Garcia\Desktop\Proyecto2\android`
3. Esperar a que se indexe

### Paso 3: Compilar y ejecutar
```bash
./gradlew build          # Compilar
./gradlew installDebug   # Instalar en dispositivo
```

O desde Android Studio:
- Run → Run 'app' (botón verde)

---

## 📲 PRUEBAS

### 1. Verificar permisos
- La app pedirá permisos la primera vez
- Aceptar todos (Bluetooth, ubicación)

### 2. Buscar dispositivos
- Clic en "Buscar Dispositivos"
- ESP32 debe estar encendido y en modo descubrimiento
- Debe aparecer "ESP32-Acceso" en la lista

### 3. Conectar
- Seleccionar ESP32-Acceso
- Clic en "Conectar"
- Esperar confirmación

### 4. Solicitar acceso
- Ingresa un token: `TOKEN123` o `INVALID`
- Clic en "Solicitar Acceso"
- Observar respuesta:
  - `GRANTED` = acceso concedido (texto verde)
  - `DENIED` = acceso denegado (texto rojo)

### 5. Verificar servidor
```bash
curl http://localhost:5000/log
```
Debe mostrar los intentos registrados.

---

## 🐛 TROUBLESHOOTING

| Problema | Solución |
|----------|----------|
| "No se puede encontrar ESP32" | Verificar que ESP32 está encendido y bluetoothEnabled |
| "Permiso denegado" | Ir a Configuración → Permisos de la app → Permitir Bluetooth |
| "Conexión rechazada" | ESP32 debe estar esperando conexiones (SPP iniciado) |
| "Token no enviado" | Verificar que hay \ n al final del string |
| "Respuesta vacía" | Verificar conexión Wi-Fi del ESP32 y disponibilidad del servidor |

---

## 💡 MEJORAS OPCIONALES

1. **Interfaz mejorada**
   - Agregar colores personalizados
   - Animaciones
   - Material Design 3

2. **Historial de intentos**
   - Guardar intentos locales
   - Mostrar en lista con timestamp

3. **Múltiples dispositivos**
   - Conectar a varios ESP32 secuencialmente
   - Guardar dispositivos favoritos

4. **Sincronización con servidor**
   - Descargar lista de usuarios
   - Verificar tokens disponibles

5. **Notificaciones**
   - Alertas de acceso concedido/denegado
   - Sonidos personalizados

---

## 📚 REFERENCIAS

- [Android Bluetooth Docs](https://developer.android.com/guide/topics/connectivity/bluetooth)
- [Kotlin Coroutines](https://kotlinlang.org/docs/coroutines-overview.html)
- [Material Design](https://material.io/design)

