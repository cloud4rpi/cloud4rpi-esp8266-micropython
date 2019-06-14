from time import time, sleep
from machine import Pin, reset
from network import WLAN, STA_IF
from onewire import OneWire
from ds18x20 import DS18X20

import cloud4rpi

# Enter the name of your Wi-Fi and its password here.
# If you have an open Wi-Fi, simply remove the second item.
WIFI_SSID_PASSWORD = '__SSID__', '__PWD__'

# Enter your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = '__YOUR_DEVICE_TOKEN__'

LED_PIN = 12
BUTTON_PIN = 16
ONEWIRE_PIN = 14

WIFI_CONNECTION_TIMEOUT = 10  # seconds
PUBLISH_INTERVAL = 60  # seconds

# --------------------------------------------------------------------------- #

led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN)
button_state_prev = button.value()
button_state_now = button_state_prev
btn_value = False

ds18 = DS18X20(OneWire(Pin(ONEWIRE_PIN)))
thermometers = ds18.scan()
print("Found", len(thermometers), "thermometers:", thermometers)


def on_led(value):
    led.value(not value)
    return not led.value()


def get_btn(value):
    global btn_value
    return btn_value


def read_thermometers():
    global ds18
    if thermometers:
        print("Getting temperatures from DS18B20 sensors...")
        ds18.convert_temp()
        sleep(0.75)


def get_temperature(value):
    global thermometers
    return ds18.read_temp(thermometers[0]) if thermometers else None


read_thermometers()

STA = WLAN(STA_IF)
STA.active(True)

while not STA.isconnected():
    print("Connecting to Wi-Fi...")
    wifi_reconnect_time = time() + WIFI_CONNECTION_TIMEOUT
    STA.connect(*WIFI_SSID_PASSWORD)
    while not STA.isconnected() and time() < wifi_reconnect_time:
        sleep(0.5)
    if not STA.isconnected():
        print("Connection FAILED!")
        continue

    print("Connected!")

    device = None
    while not device:
        if not STA.isconnected():
            print("Wi-Fi Connection failed!")
            break
        print("Connecting to Cloud4RPi...")
        device = cloud4rpi.connect(DEVICE_TOKEN)
        if not device:
            continue
        print("Connected!")

        # Available types: 'bool', 'numeric', 'string'
        device.declare({
            'LED': {
                'type': 'bool',
                'value': False,
                'bind': on_led
            },
            'Button': {
                'type': 'bool',
                'value': False,
                'bind': get_btn
            },
            'Temperature': {
                'type': 'numeric',
                'value': None,
                'bind': get_temperature
            }
        })
        device.declare_diag({
            'IP Address': STA.ifconfig()[0]
        })

        device.publish_diag()
        device.publish_config()
        device.publish_data()

        print("Waiting for messages...")

        next_publish = time() + PUBLISH_INTERVAL

        while True:
            try:
                device.check_commands()
                button_state_prev = button_state_now
                button_state_now = button.value()

                # Falling edge detection
                if button_state_prev == 1 and button_state_now == 0:
                    btn_value = not btn_value
                    device.publish_data()

                if time() >= next_publish:
                    print("Scheduled publishing...")
                    read_thermometers()
                    device.publish_data()
                    next_publish = time() + PUBLISH_INTERVAL
                sleep(0.1)

            except Exception as e:
                print("%s: %s" % (type(e).__name__, e))
                device = None
                break
