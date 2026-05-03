package com.example.btaccess

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.Intent
import android.content.pm.PackageManager
import android.os.Bundle
import android.widget.Button
import android.widget.EditText
import android.widget.TextView
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import kotlinx.coroutines.*
import java.io.InputStream
import java.io.OutputStream
import java.util.*

class MainActivity : AppCompatActivity() {

    private lateinit var bluetoothAdapter: BluetoothAdapter
    private val sppUuid = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")
    private lateinit var statusText: TextView
    private lateinit var tokenEdit: EditText
    private lateinit var connectButton: Button

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        // Asumir layout simple
        statusText = TextView(this)
        tokenEdit = EditText(this)
        connectButton = Button(this)
        setContentView(statusText) // Simplificado

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()

        connectButton.setOnClickListener {
            if (bluetoothAdapter.isEnabled) {
                CoroutineScope(Dispatchers.IO).launch {
                    connectAndSend()
                }
            } else {
                val enableBtIntent = Intent(BluetoothAdapter.ACTION_REQUEST_ENABLE)
                startActivityForResult(enableBtIntent, 1)
            }
        }

        checkPermissions()
    }

    private fun checkPermissions() {
        val permissions = arrayOf(
            Manifest.permission.BLUETOOTH,
            Manifest.permission.BLUETOOTH_ADMIN,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.ACCESS_FINE_LOCATION
        )
        permissions.forEach {
            if (ActivityCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED) {
                ActivityCompat.requestPermissions(this, permissions, 1)
            }
        }
    }

    private suspend fun connectAndSend() {
        try {
            val device = bluetoothAdapter.bondedDevices.firstOrNull { it.name == "ESP32-Acceso" }
            if (device == null) {
                runOnUiThread { statusText.text = "Dispositivo no encontrado" }
                return
            }

            val socket = device.createRfcommSocketToServiceRecord(sppUuid)
            socket.connect()

            val output = socket.outputStream
            val token = tokenEdit.text.toString()
            output.write("$token\n".toByteArray())
            output.flush()

            val input = socket.inputStream
            val buffer = ByteArray(64)
            val bytes = input.read(buffer)
            val response = String(buffer, 0, bytes).trim()

            runOnUiThread { statusText.text = response }

            socket.close()
        } catch (e: Exception) {
            runOnUiThread { statusText.text = "Error: ${e.message}" }
        }
    }
}