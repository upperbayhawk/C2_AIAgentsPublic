# ==============================================================================
# Module: readme.txt
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Python installation and dependencies
# Notes: 
# ==============================================================================


Create openAI API account
https://platform.openai.com/

Set the environment variable
setx OPENAI_API_KEY sk-NG9XUhS4hONCH0ZkW9Y3Txxxxxxxxxxxxxxxxxxxxxxxx

Download mosquitto for windows 64bit
https://mosquitto.org/download/


Packages needed

install python3
https://www.python.org/downloads/

install pip
https://pip.pypa.io/en/stable/installation/

pip install openai
pip install logbook
pip install paho-mqtt
pip install thingspeak
pip install arrow
pip install pygame
pip install cachetools
pip install random2
---------------------------------------------

Log Levels, Trace, debug, info

---------------------------------------------

MQTT messages
openai/assistant/agentname/

ToClient
ToAssistant
DataFeed
alarms
Alerts
Command
Control
Notices


From Volttron for consideration
• alerts - Base topic for alerts published by agents and subsystems, such as agent health alerts
• analysis - Base topic for analytics being used with building data
• config - Base topic for managing agent configuration
• devices - Base topic for data being published by drivers
• datalogger - Base topic for agents wishing to record time series data
• heartbeat - Topic for publishing periodic “heartbeat” or “keep-alive”
• market - Base topics for market agent communication
• record - Base topic for agents to record data in an arbitrary format
• weather - Base topic for polling publishes of weather service agents



