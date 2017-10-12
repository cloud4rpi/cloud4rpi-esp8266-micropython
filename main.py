from machine import Pin, idle, reset
from network import WLAN, STA_IF

import cloud4rpi

# Enter the name of your Wi-Fi and its password here.
# If you have an open Wi-Fi, simply remove the second item.
WIFI_SSID_PASSWORD = '__SSID__', '__PWD__'

# Enter your device token here. To get the token,
# sign up at https://cloud4rpi.io and create a device.
DEVICE_TOKEN = '__YOUR_DEVICE_TOKEN__'

LED_PIN = 12
BUTTON_PIN = 16

# --------------------------------------------------------------------------- #

STA = WLAN(STA_IF)
STA.active(True)
STA.connect(*WIFI_SSID_PASSWORD)

while not STA.isconnected():
    idle()
print("Connected to Wi-Fi")

led = Pin(LED_PIN, Pin.OUT)
button = Pin(BUTTON_PIN, Pin.IN)
button_state_prev = button.value()
button_state_now = button_state_prev
btn_value = False


def on_led(value):
    led.value(not value)
    return not led.value()


def get_btn(value):
    global btn_value
    return btn_value

device = cloud4rpi.connect(DEVICE_TOKEN)

if not device:
    print("Failed to connect to Cloud4RPi")
else:
    print("Connected to Cloud4RPi")
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
        }
    })
    device.declare_diag({
        'IP Address': STA.ifconfig()[0]
    })

    device.publish_diag()
    device.publish_config()
    device.publish_data()

    print("Waiting for messages...")
    while True:
        try:
            device.check_commands()
        except Exception as e:
            print("%s: %s; Reconnecting..." % (type(e).__name__, e))
            if device.connect():
                print("Success!")
            else:
                print("Failed to reconnect")

        button_state_prev = button_state_now
        button_state_now = button.value()

        # Falling edge detection
        if button_state_prev == 1 and button_state_now == 0:
            btn_value = not btn_value
            device.publish_data()
