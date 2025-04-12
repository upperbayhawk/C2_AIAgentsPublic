# ==============================================================================
# Module: config.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Agent configuration parameters
# Notes:
# ==============================================================================

import logbook

agent_name = "OmniBus-1-0-0"
# MQTT Broker settings
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
#
mqtt_base_topic = "openai/assistant/"
MQTT_TOPIC_TOASSISTANT = mqtt_base_topic + agent_name + "/ToAssistant"
MQTT_TOPIC_TOCLIENT = mqtt_base_topic + agent_name + "/ToClient"
#
MQTT_TOPIC_COMMAND = mqtt_base_topic + agent_name + "/CommandCenter"
MQTT_TOPIC_CONTROL = mqtt_base_topic + agent_name + "/ControlPanel"
MQTT_TOPIC_ALARM = mqtt_base_topic + agent_name + "/AlarmPanel"
MQTT_TOPIC_NOTICE = mqtt_base_topic + agent_name + "/NoticePanel"
MQTT_TOPIC_ALERT = mqtt_base_topic + agent_name + "/AlertPanel"
#
MQTT_TOPIC_DATAFEED = mqtt_base_topic + agent_name + "/DataFeed"
# Logger levels DEBUG, INFO
logging_level = logbook.DEBUG

ai_polling_interval = 1
