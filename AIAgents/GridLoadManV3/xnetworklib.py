# ==============================================================================
# Module: xnetworklib.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Library that implements MQTT messaging to other agents and apps
# Notes:
# ==============================================================================

import logbook
import paho.mqtt.client as mqtt
class XNetwork:
    def __init__(self, mqtt_broker_host, mqtt_broker_port):
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.mqtt_broker_host = mqtt_broker_host
        self.mqtt_broker_port = mqtt_broker_port
        self.connected = False

        self.log = logbook.Logger("XNetwork", 0)
        #self.log.debug("Hello From Below")

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            self.connected = True
            self.log.debug("Connected to MQTT broker")
        else:
            self.log.debug(f"Connection failed with error code {rc}")

    def on_message(self, client, userdata, msg):
        self.log.debug(f"Received message on topic {msg.topic}: {msg.payload.decode('utf-8')}")

    def send_mqtt_event(self, topic, message):
        if self.connected:
            self.client.publish(topic, message)
        else:
            self.log.debug("Not connected to MQTT broker")

    def receive_mqtt_event(self, topic):
        if self.connected:
            self.client.subscribe(topic)
        else:
            self.log.debug("Not connected to MQTT broker")

    def connect_to_broker(self):
        self.client.connect(self.mqtt_broker_host, self.mqtt_broker_port, 60)
        self.client.loop_start()

    def disconnect_from_broker(self):
        self.client.loop_stop()
        self.client.disconnect()

    def hello_funky_stuff(self, message):
        self.log.debug("FunkyStuff: " + message)

#if __name__ == "__main__":
#    mqtt_broker_host = "localhost"  # Replace with your MQTT broker host
#    mqtt_broker_port = 1883  # Replace with your MQTT broker port

#    xfunc = XFunction(mqtt_broker_host, mqtt_broker_port)
#    xfunc.connect_to_broker()

    # Example usage:
#    xfunc.talk_to_Dave("Hello, Dave!")
#    xfunc.send_command_to_house("Turn on the lights")

#    xfunc.disconnect_from_broker()
