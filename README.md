# Cloud4RPi Library and Examples for [ESP8266](https://en.wikipedia.org/wiki/ESP8266) with [MicroPython](https://micropython.org/)

## Running the Sample Code

1. Connect your ESP8266 to your Wi-Fi and configure it for the [WebREPL](https://github.com/micropython/webrepl).
2. Download the [MQTT library](https://github.com/micropython/micropython-lib/blob/master/umqtt.simple/umqtt/simple.py) and put it to your ESP8266 with the name `mqtt.py`. 
3. Clone this repository or download [cloud4rpi.py](cloud4rpi.py) and [main.py](main.py) files.
4. [Log into your Cloud4RPi account](https://cloud4rpi.io/signin) or [create a new one](https://cloud4rpi.io/register).
5. Copy [your device](https://cloud4rpi.io/devices)'s **Device Token**.
4. Edit the [main.py](main.py). Put your Wi-Fi data and the **Device Token** to the required variables. 
11. Connect the LED to GPIO12 and a button to GPIO16. If you need to use another pins, change the required variables. <!--Note that the code assumes permanent connection to **Vcc** and the high logical level on standby in both cases.-->
5. Transfer the [cloud4rpi.py](cloud4rpi.py) file and edited [main.py](main.py) file to your ESP8266.
6. Reset the ESP8266.
8. Notice that the [device](https://cloud4rpi.io/devices) went online and started sending data.
9. Go to the [Control Panels](https://cloud4rpi.io/control-panels/) page and add a new control panel.
10. Add two **Switch** widgets and bind them to the `LED` and `Button` variables.

You can use this control panel to see when the button was pressed and control the LED.
