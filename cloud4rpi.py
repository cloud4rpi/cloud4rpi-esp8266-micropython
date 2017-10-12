# --------------------------------------------------------------------------- #
#  Cloud4RPi client library for ESP8266, https://github.com/cloud4rpi
# --------------------------------------------------------------------------- #

import json

# https://raw.githubusercontent.com/micropython/micropython-lib/mqtt/umqtt.simple/umqtt/simple.py
from mqtt import MQTTClient


C4R_BROKER_HOST = 'mq.cloud4rpi.io'
C4R_BROKER_PORT = 1883

C4R_TOPIC_FORMAT = b'devices/%s/%s'


class Device(object):
    def __init__(self, device_token):
        self.__device_token = bytes(device_token, 'utf-8')
        self.__variables = None
        self.__diag_variables = None
        self.__mqtt = None
        self.__bindings = dict()

    def __publish(self, topic, payload=None):
        if payload is None:
            return False
        msg = json.dumps({'payload': payload})
        self.__mqtt.publish(C4R_TOPIC_FORMAT %
                            (self.__device_token, topic), msg, qos=1)
        print(topic, "<--", msg)

    def __on_message(self, topic, msg):
        print(topic.decode().rsplit('/')[-1], "-->", msg.decode())
        data = json.loads(msg)
        for var_name, callback in self.__bindings.items():
            if var_name in data.keys():
                ret = callback(data[var_name])
                self.__publish('data', {var_name: ret})

    def connect(self):
        self.__mqtt = MQTTClient(client_id=self.__device_token,
                                 server=C4R_BROKER_HOST,
                                 port=C4R_BROKER_PORT)

        self.__mqtt.set_callback(self.__on_message)
        try:
            self.__mqtt.connect()
            self.__mqtt.subscribe(C4R_TOPIC_FORMAT %
                                  (self.__device_token, 'commands'), qos=1)
        except Exception as e:
            print("[Exception] %s: %s" % (type(e).__name__, e))
            return False
        return True

    def declare(self, variables):
        self.__variables = variables

    def declare_diag(self, diag_variables):
        self.__diag_variables = diag_variables

    def publish_config(self):
        cfg = []
        for var_name, var_config in self.__variables.items():
            cfg.append({'name': var_name, 'type': var_config['type']})
            self.__bindings[var_name] = var_config['bind']
        self.__publish('config', cfg)

    def publish_diag(self):
        self.__publish('diagnostics', self.__diag_variables)

    def publish_data(self):
        for var_name, callback in self.__bindings.items():
            self.__variables[var_name]['value'] = \
                                callback(self.__variables[var_name]['value'])

        cfg = {var_name: var_config['value']
               for var_name, var_config in self.__variables.items()}
        self.__publish('data', cfg)

    def check_commands(self):
        self.__mqtt.check_msg()


def connect(device_token):
    device = Device(device_token)
    if device.connect():
        return device
