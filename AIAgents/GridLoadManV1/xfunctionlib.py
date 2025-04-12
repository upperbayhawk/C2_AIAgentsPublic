# ==============================================================================
# Module: xfunctionlib.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Library that implements the call-back functions 
#   from the AI Assistant.
# Notes: Must include functions defined in makeagent.py and openailib.py
# ==============================================================================

import json

import logbook
import paho.mqtt.client as mqtt

from xnetworklib import XNetwork
from xcachelib import data_cache_instance
import config

agent_name = config.agent_name

class XFunction:
    def __init__(self):
        self.mqtt_broker_host = config.MQTT_BROKER
        self.mqtt_broker_port = config.MQTT_PORT
        self.log = logbook.Logger("xfunction")
        self.log.debug("Hello From Below")

        self.base_topic = config.mqtt_base_topic + agent_name + "/"
        self.base_topic_c2agent = config.mqtt_base_topic_c2agent
 
    def sendGridPeakDetected(self, network_node, message, start_date_time,duration_mins,peak_lmp,grid_node,award_level,game_type):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        topic = self.base_topic_c2agent
        grid_peak_detected = config.GridPeakDetected("GridPeakDetected", agent_name, message, start_date_time, duration_mins,peak_lmp, grid_node,award_level,game_type)
        message_json = json.dumps(grid_peak_detected.__dict__)
        #my_message = message + "'" + start_date_time + "'" + duration_mins + "," + peak_lmp + "," + grid_node
        print("TO: " + topic + "," + message_json)       
        xnet.send_mqtt_event(topic, message_json)
        xnet.disconnect_from_broker()               
        self.log.debug("sendGridPeakedDetected: " + message + " to " + topic)
        return "OK"

    def sendCommandSignalToNetworkNode(self, network_node, message):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        topic = self.base_topic + network_node
        xnet.send_mqtt_event(topic, message)
        xnet.disconnect_from_broker()               
        self.log.debug("sendCommandSignalToNetworkNode: " + message + " to " + topic)
        return "OK"

    def sendAlarmSignalToNetworkNode(self, network_node, message):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        topic = self.base_topic + network_node
        xnet.send_mqtt_event(topic, message)
        xnet.disconnect_from_broker()               
        self.log.debug("sendAlarmSignalToNetworkNode: " + message + " to " + topic)
        return "OK"

    def sendControlSignalToNetworkNode(self, network_node, message):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        topic = self.base_topic + network_node
        xnet.send_mqtt_event(topic, message)
        xnet.disconnect_from_broker()               
        self.log.debug("sendControlSignalToNetworkNode: " + message + " to " + topic)
        return "OK"

    def sendNoticeSignalToNetworkNode(self, network_node, message):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        topic = self.base_topic + network_node
        xnet.send_mqtt_event(topic, message)
        xnet.disconnect_from_broker()               
        self.log.debug("sendNoticeSignalToNetworkNode: " + message + " to " + topic)
        return "OK"

    def sendDataToAgent(self, topic, message):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        xnet.send_mqtt_event(topic, message)
        xnet.disconnect_from_broker()               
        self.log.debug("sendDataToAgent: " + message + " to " + topic)
        return "OK"
    
    def sendErrorToClient(self, topic, message):
        xnet = XNetwork(self.mqtt_broker_host, self.mqtt_broker_port)
        xnet.connect_to_broker()
        while xnet.connected == False:
            pass
        xnet.send_mqtt_event(topic, message)
        xnet.disconnect_from_broker()               
        self.log.debug("sendErrorToClient: " + message + " to " + topic)
        return "OK"
    
    def getNickname(self, location):
        self.log.debug("getNickname: " + location)
        return "A Sandy Place"

    def getMagicNumber(self, name):
        self.log.debug("getMagicNumber: " + name)
        json_string = data_cache_instance.read(name)
        if json_string:
            self.log.debug("json = " + json_string)
            my_data = json.loads(json_string)
            value = my_data["value"]
            self.log.debug("Magic = " + str(value))
            return str(value)
        else:
            return "NOTFOUND"

    def getSensorValuebyName(self, name):
        self.log.debug("getSensorValuebyName: " + name)
        json_string = data_cache_instance.read(name)
        if json_string:
            self.log.debug("json = " + json_string)
            my_data = json.loads(json_string)
            value = my_data["value"]
            self.log.debug("Sensor = " + str(value))
            return str(value)
        else:
            return "NOTFOUND"
    
    def putSensorValuebyName(self, name, value):
        self.log.debug("putSensorValuebyName: " + name)
        data_cache_instance.write(name,value, "OK")
        return "OK"
        
    def getNickname3(self, location):
        self.log.debug("getNickname: " + location)
        return "SandyPlace3"
