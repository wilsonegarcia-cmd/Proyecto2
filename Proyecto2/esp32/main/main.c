#include <string.h>
#include "esp_log.h"
#include "esp_bt.h"
#include "esp_bt_main.h"
#include "esp_bt_device.h"
#include "esp_gap_bt_api.h"
#include "esp_spp_api.h"
#include "esp_wifi.h"
#include "esp_event.h"
#include "esp_netif.h"
#include "esp_http_client.h"
#include "cJSON.h"
#include "driver/gpio.h"
#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "nvs_flash.h"
#include <time.h>

#define SSID "TU_SSID"
#define PASSWORD "TU_CONTRASENA"
#define SERVER "http://192.168.1.100:5000"
#define LED_R 25
#define LED_G 26
#define LED_B 27
#define BUZZER 32
#define DEVICE_NAME "ESP32-Acceso"

static const char *TAG = "BT_ACC";

//----LED y Buzzer---
static void set_led(bool r, bool g, bool b) {
    gpio_set_level(LED_R, r);
    gpio_set_level(LED_G, g);
    gpio_set_level(LED_B, b);
}
static void beep(uint32_t ms) {
    gpio_set_level(BUZZER, 1);
    vTaskDelay(pdMS_TO_TICKS(ms));
    gpio_set_level(BUZZER, 0);
}

//----Verificar acceso via HTTP---
static bool verificar_acceso(const char *token) {
    char url[128];
    snprintf(url, sizeof(url), "%s/check?token=%s", SERVER, token);
    char buf[256] = {0};
    esp_http_client_config_t cfg = {.url = url,
                                    .user_data = buf, .buffer_size_tx = 256};
    esp_http_client_handle_t c = esp_http_client_init(&cfg);
    esp_err_t err = esp_http_client_perform(c);
    esp_http_client_cleanup(c);
    if (err != ESP_OK) return false;
    cJSON *root = cJSON_Parse(buf);
    bool ok = cJSON_IsTrue(cJSON_GetObjectItem(root, "autorizado"));
    cJSON_Delete(root);
    return ok;
}

//----Log acceso---
static void log_acceso(const char *token, const char *resultado) {
    char url[128];
    snprintf(url, sizeof(url), "%s/log", SERVER);
    char post_data[256];
    time_t now = time(NULL);
    struct tm *tm_info = localtime(&now);
    char timestamp[32];
    strftime(timestamp, sizeof(timestamp), "%Y-%m-%d %H:%M:%S", tm_info);
    snprintf(post_data, sizeof(post_data), "{\"token\":\"%s\",\"timestamp\":\"%s\",\"resultado\":\"%s\"}", token, timestamp, resultado);
    esp_http_client_config_t cfg = {.url = url, .method = HTTP_METHOD_POST};
    esp_http_client_handle_t c = esp_http_client_init(&cfg);
    esp_http_client_set_post_field(c, post_data, strlen(post_data));
    esp_http_client_set_header(c, "Content-Type", "application/json");
    esp_err_t err = esp_http_client_perform(c);
    esp_http_client_cleanup(c);
    if (err == ESP_OK) {
        ESP_LOGI(TAG, "Log enviado");
    }
}

//----Callback SPP---
static void spp_callback(esp_spp_cb_event_t event,
                         esp_spp_cb_param_t *param) {
    switch (event) {
        case ESP_SPP_INIT_EVT:
            esp_bt_dev_set_device_name(DEVICE_NAME);
            esp_bt_gap_set_scan_mode(ESP_BT_CONNECTABLE,
                                     ESP_BT_GENERAL_DISCOVERABLE);
            esp_spp_start_srv(ESP_SPP_SEC_AUTHENTICATE,
                              ESP_SPP_ROLE_SLAVE, 0, "SPP_SERVER");
            break;
        case ESP_SPP_START_EVT:
            ESP_LOGI(TAG, "Servidor SPP iniciado");
            break;
        case ESP_SPP_SRV_OPEN_EVT:
            ESP_LOGI(TAG, "Cliente conectado");
            set_led(1, 1, 1); // Blanco: procesando
            break;
        case ESP_SPP_DATA_IND_EVT: {
            char token[64] = {0};
            int len = param->data_ind.len < 63 ? param->data_ind.len : 63;
            memcpy(token, param->data_ind.data, len);
            token[len] = '\0';
            while (len > 0 && (token[len - 1] == '\n' || token[len - 1] == '\r'))
                token[--len] = '\0';
            ESP_LOGI(TAG, "Token recibido: %s", token);

            bool ok = verificar_acceso(token);
            const char *resp;
            if (ok) {
                ESP_LOGI(TAG, "ACCESO CONCEDIDO");
                set_led(0, 1, 0);
                beep(150);
                resp = "GRANTED\n";
            } else {
                ESP_LOGI(TAG, "ACCESO DENEGADO");
                set_led(1, 0, 0);
                beep(600);
                resp = "DENIED\n";
            }
            log_acceso(token, ok ? "GRANTED" : "DENIED");
            esp_spp_write(param->data_ind.handle,
                          strlen(resp), (uint8_t *)resp);
            vTaskDelay(pdMS_TO_TICKS(2500));
            set_led(0, 0, 1); // Azul: en espera
            break;
        }
        case ESP_SPP_CLOSE_EVT:
            ESP_LOGI(TAG, "Cliente desconectado");
            set_led(0, 0, 1);
            break;
        default:
            break;
    }
}

void app_main(void) {
    // GPIOs
    gpio_config_t io = {.pin_bit_mask = (1ULL << LED_R) | (1ULL << LED_G) | (1ULL << LED_B) | (1ULL << BUZZER),
                        .mode = GPIO_MODE_OUTPUT};
    gpio_config(&io);
    set_led(1, 1, 0); // Amarillo: inicializando

    // NVS (requerido por BT y Wi-Fi)
    nvs_flash_init();

    // Wi-Fi
    esp_netif_init();
    esp_event_loop_create_default();
    esp_netif_create_default_wifi_sta();
    wifi_init_config_t wcfg = WIFI_INIT_CONFIG_DEFAULT();
    esp_wifi_init(&wcfg);
    esp_wifi_set_mode(WIFI_MODE_STA);
    wifi_config_t wsta = {.sta = {.ssid = SSID, .password = PASSWORD}};
    esp_wifi_set_config(WIFI_IF_STA, &wsta);
    esp_wifi_start();
    esp_wifi_connect();
    vTaskDelay(pdMS_TO_TICKS(3000));
    ESP_LOGI(TAG, "Wi-Fi conectado");

    // Bluetooth Classic
    esp_bt_controller_config_t bt_cfg = BT_CONTROLLER_INIT_CONFIG_DEFAULT();
    esp_bt_controller_init(&bt_cfg);
    esp_bt_controller_enable(ESP_BT_MODE_CLASSIC_BT);
    esp_bluedroid_init();
    esp_bluedroid_enable();
    esp_spp_register_callback(spp_callback);
    esp_spp_init(ESP_SPP_MODE_CB);

    set_led(0, 0, 1); // Azul: listo
    ESP_LOGI(TAG, "Sistema listo. Conecte desde la app Android.");
}