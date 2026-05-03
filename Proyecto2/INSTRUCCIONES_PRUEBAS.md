# Guía de Ejecución de Pruebas - Sistema de Control de Acceso

## Problema Detectado
El entorno del sistema requiere pwsh (PowerShell Core) que no está instalado.
**Solución**: Ejecutaremos las pruebas manualmente en CMD (terminal nativa de Windows).

---

## PASO 1: Abrir Terminal CMD

1. Presiona: `Win + R`
2. Escribe: `cmd`
3. Presiona: `Enter`

---

## PASO 2: Instalar Dependencias

En la terminal CMD, ejecuta:

```cmd
python -m pip install flask requests --quiet
```

Esperado: `Successfully installed flask` (sin errores)

---

## PASO 3: Iniciar el Servidor

En la MISMA terminal CMD, ejecuta:

```cmd
cd c:\Users\Eduardo Garcia\Desktop\Proyecto2\server
python app.py
```

Verás algo como:
```
 * Running on http://127.0.0.1:5000
 * Debug mode: off
 * WARNING in app.run() [...]
```

**IMPORTANTE**: Deja esta terminal abierta. Abra OTRA terminal (Paso 4).

---

## PASO 4: Ejecutar Pruebas (Nueva Terminal)

Abre OTRA terminal CMD nueva (Sin cerrar la anterior):

1. Presiona: `Win + R`
2. Escribe: `cmd`
3. Presiona: `Enter`

En esta NUEVA terminal, ejecuta:

```cmd
cd c:\Users\Eduardo Garcia\Desktop\Proyecto2\server
python test_api.py
```

---

## RESULTADO ESPERADO

Deberías ver algo como:

```
============================================================
  PRUEBA DEL SERVIDOR DE CONTROL DE ACCESO
============================================================

[*] Esperando a que el servidor esté listo...
[✓] Servidor disponible en http://localhost:5000

[1/6] Verificando token AUTORIZADO...
✓ GET /check?token=TOKEN123
  └─ Respuesta: {"autorizado": true, "nombre": "Usuario Autorizado"}

[2/6] Verificando token NO AUTORIZADO...
✓ GET /check?token=INVALID
  └─ Respuesta: {"autorizado": false}

[3/6] Listando usuarios registrados...
✓ GET /usuarios
  └─ Usuarios encontrados: 2
    [
      {
        "token": "TOKEN123",
        "nombre": "Usuario Autorizado"
      },
      {
        "token": "INVALID",
        "nombre": "No Autorizado"
      }
    ]

[4/6] Registrando nuevo usuario...
✓ POST /usuarios (nuevo usuario)
  └─ Respuesta: {"status": "agregado"}

[5/6] Registrando evento de acceso...
✓ POST /log (evento de acceso)
  └─ Respuesta: {"status": "registrado"}

[6/6] Verificando nuevo usuario agregado...
✓ GET /check?token=TOKEN_NUEVO
  └─ Respuesta: {"autorizado": true, "nombre": "Usuario Prueba"}

============================================================
  ✓ TODAS LAS PRUEBAS COMPLETADAS
============================================================
```

Si ves esto: ✅ **TODAS LAS PRUEBAS PASARON**

---

## Alternativa: Automatizar (Batch Script)

Si prefieres todo automático, doble-clic en este archivo:
`c:\Users\Eduardo Garcia\Desktop\Proyecto2\test_endpoints.bat`

---

## Próximos Pasos

✅ **Servidor validado**

Ahora puedes:
1. Configurar el firmware del ESP32
2. Desarrollar la app Android
3. Integrar todo el sistema

---

## URLs Disponibles

Una vez que el servidor esté corriendo, puedes probar manualmente:

- http://localhost:5000/usuarios
- http://localhost:5000/check?token=TOKEN123
- http://localhost:5000/check?token=INVALID

O usar `curl`:
```cmd
curl http://localhost:5000/usuarios
curl "http://localhost:5000/check?token=TOKEN123"
```
