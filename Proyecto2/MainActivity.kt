package com.example.bluetoothaccess

import android.Manifest
import android.bluetooth.BluetoothAdapter
import android.bluetooth.BluetoothDevice
import android.bluetooth.BluetoothSocket
import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.content.IntentFilter
import android.content.pm.PackageManager
import android.os.Build
import android.os.Bundle
import android.widget.Toast
import androidx.activity.result.contract.ActivityResultContracts
import androidx.appcompat.app.AppCompatActivity
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import androidx.lifecycle.lifecycleScope
import com.example.bluetoothaccess.databinding.ActivityMainBinding
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.launch
import kotlinx.coroutines.withContext
import java.io.IOException
import java.util.*

/**
 * MainActivity - Control de Acceso con Bluetooth
 * Conecta a ESP32 vía SPP y envía token para verificación
 */
class MainActivity : AppCompatActivity() {

    private lateinit var binding: ActivityMainBinding
    private lateinit var bluetoothAdapter: BluetoothAdapter
    
    private var bluetoothSocket: BluetoothSocket? = null
    private var outputStream: java.io.OutputStream? = null
    private var inputStream: java.io.InputStream? = null
    private var isConnected = false

    private val devices = mutableListOf<BluetoothDevice>()
    private val deviceNames = mutableListOf<String>()
    private var selectedDevice: BluetoothDevice? = null

    private val SPP_UUID = UUID.fromString("00001101-0000-1000-8000-00805F9B34FB")

    private val bluetoothReceiver = object : BroadcastReceiver() {
        override fun onReceive(context: Context?, intent: Intent?) {
            when (intent?.action) {
                BluetoothDevice.ACTION_FOUND -> {
                    val device = intent.getParcelableExtra<BluetoothDevice>(BluetoothDevice.EXTRA_DEVICE)
                    if (device != null && !devices.contains(device)) {
                        devices.add(device)
                        val name = device.name ?: device.address
                        deviceNames.add("$name\n${device.address}")
                        binding.devicesListView.adapter?.notifyDataSetChanged()
                    }
                }
                BluetoothAdapter.ACTION_DISCOVERY_FINISHED -> {
                    binding.scanButton.isEnabled = true
                    binding.scanButton.text = "Buscar Dispositivos"
                }
            }
        }
    }

    private val permissions = if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.S) {
        arrayOf(
            Manifest.permission.BLUETOOTH_SCAN,
            Manifest.permission.BLUETOOTH_CONNECT,
            Manifest.permission.ACCESS_FINE_LOCATION
        )
    } else {
        arrayOf(Manifest.permission.ACCESS_FINE_LOCATION)
    }

    private val permissionLauncher = registerForActivityResult(
        ActivityResultContracts.RequestMultiplePermissions()
    ) { /* Permisos solicitados */ }

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        binding = ActivityMainBinding.inflate(layoutInflater)
        setContentView(binding.root)

        bluetoothAdapter = BluetoothAdapter.getDefaultAdapter()
            ?: run {
                Toast.makeText(this, "Bluetooth no disponible", Toast.LENGTH_SHORT).show()
                finish()
                return@onCreate
            }

        requestPermissionsIfNeeded()
        setupUI()

        val filter = IntentFilter().apply {
            addAction(BluetoothDevice.ACTION_FOUND)
            addAction(BluetoothAdapter.ACTION_DISCOVERY_FINISHED)
        }
        registerReceiver(bluetoothReceiver, filter, Context.RECEIVER_EXPORTED)
    }

    override fun onDestroy() {
        super.onDestroy()
        try { unregisterReceiver(bluetoothReceiver) } catch (e: Exception) {}
        disconnect()
    }

    private fun requestPermissionsIfNeeded() {
        val missing = permissions.filter {
            ContextCompat.checkSelfPermission(this, it) != PackageManager.PERMISSION_GRANTED
        }.toTypedArray()
        if (missing.isNotEmpty()) permissionLauncher.launch(missing)
    }

    private fun setupUI() {
        val adapter = android.widget.ArrayAdapter(this, android.R.layout.simple_list_item_1, deviceNames)
        binding.devicesListView.adapter = adapter

        binding.devicesListView.setOnItemClickListener { _, _, pos, _ ->
            selectedDevice = devices[pos]
            binding.selectedDeviceText.text = "✓ ${selectedDevice?.name ?: selectedDevice?.address}"
            binding.connectButton.isEnabled = true
        }

        binding.scanButton.setOnClickListener { scanForDevices() }
        binding.connectButton.setOnClickListener { 
            selectedDevice?.let { connectToDevice(it) }
        }
        binding.requestAccessButton.setOnClickListener { sendAccessRequest() }
        binding.disconnectButton.setOnClickListener { disconnect() }

        updateUI()
    }

    private fun scanForDevices() {
        binding.scanButton.isEnabled = false
        binding.scanButton.text = "Escaneando..."
        devices.clear()
        deviceNames.clear()
        binding.devicesListView.adapter?.notifyDataSetChanged()

        if (ActivityCompat.checkSelfPermission(this, Manifest.permission.BLUETOOTH_SCAN) 
            == PackageManager.PERMISSION_GRANTED
        ) {
            bluetoothAdapter.cancelDiscovery()
            bluetoothAdapter.startDiscovery()
        }
    }

    private fun connectToDevice(device: BluetoothDevice) {
        lifecycleScope.launch {
            try {
                binding.statusText.text = "Conectando..."

                withContext(Dispatchers.IO) {
                    bluetoothSocket = device.createRfcommSocketToServiceRecord(SPP_UUID)
                    if (ActivityCompat.checkSelfPermission(
                            this@MainActivity, Manifest.permission.BLUETOOTH_CONNECT
                        ) == PackageManager.PERMISSION_GRANTED
                    ) {
                        bluetoothSocket?.connect()
                    }
                    outputStream = bluetoothSocket?.outputStream
                    inputStream = bluetoothSocket?.inputStream
                    isConnected = true
                }

                binding.statusText.text = "✓ Conectado"
                binding.requestAccessButton.isEnabled = true
                binding.tokenEditText.isEnabled = true
                binding.connectButton.isEnabled = false
                binding.scanButton.isEnabled = false
                binding.disconnectButton.isEnabled = true

                Toast.makeText(this@MainActivity, "Conectado a ${device.name}", Toast.LENGTH_SHORT).show()

            } catch (e: IOException) {
                isConnected = false
                binding.statusText.text = "✗ Error"
                Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            }
        }
    }

    private fun sendAccessRequest() {
        val token = binding.tokenEditText.text.toString().trim()
        if (token.isEmpty()) {
            Toast.makeText(this, "Ingresa un token", Toast.LENGTH_SHORT).show()
            return
        }
        if (!isConnected) {
            Toast.makeText(this, "No conectado", Toast.LENGTH_SHORT).show()
            return
        }

        lifecycleScope.launch {
            try {
                binding.statusText.text = "Enviando..."
                binding.requestAccessButton.isEnabled = false

                withContext(Dispatchers.IO) {
                    outputStream?.write(("$token\n").toByteArray())
                    outputStream?.flush()

                    val buffer = ByteArray(64)
                    val bytes = inputStream?.read(buffer) ?: 0
                    val response = String(buffer, 0, bytes).trim()

                    withContext(Dispatchers.Main) {
                        binding.responseText.text = response
                        binding.statusText.text = "Respuesta: $response"
                        
                        if (response.contains("GRANTED", ignoreCase = true)) {
                            binding.responseText.setTextColor(
                                ContextCompat.getColor(this@MainActivity, android.R.color.holo_green_dark)
                            )
                            Toast.makeText(this@MainActivity, "✓ ACCESO CONCEDIDO", Toast.LENGTH_SHORT).show()
                        } else if (response.contains("DENIED", ignoreCase = true)) {
                            binding.responseText.setTextColor(
                                ContextCompat.getColor(this@MainActivity, android.R.color.holo_red_dark)
                            )
                            Toast.makeText(this@MainActivity, "✗ ACCESO DENEGADO", Toast.LENGTH_SHORT).show()
                        }
                    }
                }

            } catch (e: IOException) {
                binding.statusText.text = "Error"
                Toast.makeText(this@MainActivity, "Error: ${e.message}", Toast.LENGTH_SHORT).show()
            } finally {
                binding.requestAccessButton.isEnabled = true
            }
        }
    }

    private fun disconnect() {
        lifecycleScope.launch {
            try {
                withContext(Dispatchers.IO) {
                    outputStream?.close()
                    inputStream?.close()
                    bluetoothSocket?.close()
                }
                isConnected = false
                updateUI()
            } catch (e: Exception) {
                // Ignorar errores
            }
        }
    }

    private fun updateUI() {
        if (isConnected) {
            binding.scanButton.isEnabled = false
            binding.devicesListView.isEnabled = false
            binding.connectButton.isEnabled = false
            binding.requestAccessButton.isEnabled = true
            binding.tokenEditText.isEnabled = true
            binding.disconnectButton.isEnabled = true
            binding.statusText.text = "✓ Conectado"
        } else {
            binding.scanButton.isEnabled = true
            binding.devicesListView.isEnabled = true
            binding.connectButton.isEnabled = selectedDevice != null
            binding.requestAccessButton.isEnabled = false
            binding.tokenEditText.isEnabled = false
            binding.disconnectButton.isEnabled = false
            binding.statusText.text = "✗ Desconectado"
            binding.responseText.text = ""
        }
    }
}
