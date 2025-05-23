# ==============================================================================
# Module: runsource.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Console app that periodically 
#   sends tag/value data in JSON to the runserver.py cache.
# Notes: pip install weather-gov==0.1
# ==============================================================================

import os
import sys
import asyncio
import queue
import threading
import json
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

import time
import arrow
import logging
from logging.handlers import TimedRotatingFileHandler

import paho.mqtt.client as mqtt
from thingspeaklib import XThingspeak
from openai import OpenAI
# for speech
import pygame
import random

import config
from xfunctionlib import XFunction

agent_name = config.agent_name

logging_level = config.logging_level

# 10 min
agent_period_secs = 300

enable_mqtt_speech = False
enable_command_speech = True

agent_output_file = "./data/source_output.txt"
agent_log_file = "./logs/source_log.txt"

MQTT_BROKER = config.MQTT_BROKER
MQTT_PORT = config.MQTT_PORT
MQTT_TOPIC_TOASSISTANT = config.MQTT_TOPIC_TOASSISTANT
MQTT_TOPIC_TOCLIENT = config.MQTT_TOPIC_TOCLIENT

MQTT_TOPIC_COMMAND = config.MQTT_TOPIC_COMMAND
MQTT_TOPIC_CONTROL = config.MQTT_TOPIC_CONTROL
MQTT_TOPIC_ALARM = config.MQTT_TOPIC_ALARM
MQTT_TOPIC_NOTICE = config.MQTT_TOPIC_NOTICE
MQTT_TOPIC_ALERT = config.MQTT_TOPIC_ALERT
MQTT_TOPIC_C2AGENT = config.MQTT_TOPIC_C2AGENT


MQTT_TOPIC_DATAFEED = config.MQTT_TOPIC_DATAFEED
SEPARATOR = "========================="

#-----------------------------------------------------


in_queue = queue.Queue()
out_queue = queue.Queue()
command_queue = queue.Queue()
control_queue = queue.Queue()
alarm_queue = queue.Queue()
notice_queue = queue.Queue()
alert_queue = queue.Queue()

clientMQ = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

clientAI = OpenAI()

#-----------------------------------------------------

# MQTT Callbacks
def on_connect(client, userdata, flags, rc, properties):
    log.debug(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    log.debug(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    pipe_input = str(msg.payload.decode())
    if msg.topic == MQTT_TOPIC_TOASSISTANT:
        log.debug("To Assistant Inbound: " + msg.topic + " " + pipe_input)
        print("To Assistant Inbound: " + msg.topic + " " + pipe_input)
        process_outgoing_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_TOCLIENT:
        log.debug("To Client Outbound: " + msg.topic + " " + pipe_input)
        print("To Client Outbound: " + msg.topic + " " + pipe_input)
        process_incoming_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_COMMAND:
        log.debug("To Command: " + msg.topic + " " + pipe_input)
        print("To Command: " + msg.topic + " " + pipe_input)
        process_commandcenter_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_CONTROL:
        log.debug("To Control: " + msg.topic + " " + pipe_input)
        print("To Control: " + msg.topic + " " + pipe_input)
        process_control_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_ALARM:
        log.debug("To Alarm: " + msg.topic + " " + pipe_input)
        print("To Alarm: " + msg.topic + " " + pipe_input)
        process_alarm_message(pipe_input)        
    elif msg.topic == MQTT_TOPIC_NOTICE:
        log.debug("To Notice: " + msg.topic + " " + pipe_input)
        print("To Notice: " + msg.topic + " " + pipe_input)
        process_notice_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_ALERT:
        log.debug("To Alert: " + msg.topic + " " + pipe_input)
        print("To Alert: " + msg.topic + " " + pipe_input)
        process_alert_message(pipe_input)

# Message Processors
def process_incoming_message(message):
    log.debug("Processing Incoming: " + message)
    in_queue.put(message)

def process_outgoing_message(message):
    log.debug("Processing Outgoing: " + message)
    out_queue.put(message)

def process_commandcenter_message(message):
    log.debug("Processing Command: " + message)
    command_queue.put(message)

def process_control_message(message):
    log.debug("Processing Control: " + message)
    control_queue.put(message)

def process_alarm_message(message):
    log.debug("Processing Alarm: " + message)
    alarm_queue.put(message)

def process_notice_message(message):
    log.debug("Processing Notice: " + message)
    notice_queue.put(message)    

def process_alert_message(message):
    log.debug("Processing Alert: " + message)
    alert_queue.put(message)  

def process_local_message(message):
    log.debug("Processing Local: " + message)
    clientMQ.publish(MQTT_TOPIC_TOASSISTANT, message)

#Threads
def incoming_worker_thread():
    while True:
        message = in_queue.get()
        if message is None:
            break
        log.debug(message)
        print(message)
        dispatch_incoming_message(message)

def outgoing_worker_thread():
    while True:
        message = out_queue.get()
        if message is None:
            break
        log.debug(message)
        print(message)
        dispatch_outgoing_message(message)
        
def command_worker_thread():
    while True:
        message = command_queue.get()
        if message is None:
            break
        log.debug(message)
        print("Command: " + message)
        dispatch_command_message(message)

def control_worker_thread():
    while True:
        message = control_queue.get()
        if message is None:
            break
        log.debug(message)
        print("Control: " + message)
        dispatch_control_message(message)

def alarm_worker_thread():
    while True:
        message = alarm_queue.get()
        if message is None:
            break
        log.debug(message)
        print("Alarm: " + message)
        dispatch_alarm_message(message)

def notice_worker_thread():
    while True:
        message = notice_queue.get()
        if message is None:
            break
        log.debug(message)
        print("Notice: " + message)
        dispatch_notice_message(message)

def alert_worker_thread():
    while True:
        message = alert_queue.get()
        if message is None:
            break
        log.debug(message)
        print("Alert: " + message)
        dispatch_alert_message(message)

#=============================================
def dispatch_incoming_message(message):
    if enable_mqtt_speech == True:
        pass
        #speak_message(message)
    else:
        pass

def dispatch_outgoing_message(message):
    if enable_mqtt_speech == True:
        #speak_message(message)
        pass
    else:
        pass

def dispatch_command_message(message):
    if enable_command_speech == True:
        my_message = "Command message " + message
        print (my_message)
        #speak_message(my_message)
    else:
        pass

def dispatch_control_message(message):
    if enable_command_speech == True:
        my_message = "Control message " + message
        print (my_message)
        #speak_message(my_message)
    else:
        pass

def dispatch_alarm_message(message):
    if enable_command_speech == True:
        my_message = "Alarm message " + message
        print (my_message)
        #speak_message(my_message)
    else:
        pass

def dispatch_notice_message(message):
    if enable_command_speech == True:
        my_message = "Notice message " + message
        print (my_message)
        #speak_message(my_message)
    else:
        pass

def dispatch_alert_message(message):
    if enable_command_speech == True:
        my_message = "Alert message " + message
        print (my_message)
        #speak_message(my_message)
    else:
        pass

#=============================================
# voices = alloy,echo,fable,onyx,nova,shimmer
def speak_message(message):
    try:
        speech_file_path = "data/runsource.mp3"
        response = clientAI.audio.speech.create(
        model="tts-1-hd",
        voice="shimmer",
        input=message
        )
        response.write_to_file(speech_file_path)

        pygame.init()
        pygame.mixer.init()
        pygame.mixer.music.load(speech_file_path)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.music.unload()
        os.remove(speech_file_path)
    finally:
        pass

#=============================================

#Main app thread
def main_run_thread():
    while True:
        start_time = arrow.now()
        # Do some work then sleep
        #---------------------
        print("Source Running...")
        xfunc = XFunction()
        
        number = random.random()
        rando_string = str(number)
        my_data = {"name": "RANDO", "value": "xx", "status": "OK"}
        my_data["value"] = rando_string
        my_message = json.dumps(my_data)
        xfunc.sendDataToAgent(MQTT_TOPIC_DATAFEED, my_message)
        log.debug("sendDataToAgent: " + my_data["name"] + " = " + my_data["value"] + " on " + MQTT_TOPIC_DATAFEED)

        number = random.random()
        rando_string = str(number)
        my_data = {"name": "Dave", "value": "xx", "status": "OK"}
        my_data["value"] = rando_string
        my_message = json.dumps(my_data)
        xfunc.sendDataToAgent(MQTT_TOPIC_DATAFEED, my_message)
        log.debug("sendDataToAgent: " + my_data["name"] + " = " + my_data["value"] + " on " + MQTT_TOPIC_DATAFEED)

        my_data = {"name": "MasterSwitch", "value": "xx", "status": "OK"}
        my_data["value"] = "ON"
        my_message = json.dumps(my_data)
        xfunc.sendDataToAgent(MQTT_TOPIC_DATAFEED, my_message)
        log.debug("sendDataToAgent: " + my_data["name"] + " = " + my_data["value"] + " on " + MQTT_TOPIC_DATAFEED)

        my_data = {"name": "TemperatureInLewes", "value": "xx", "status": "OK"}
        my_data["value"] = "69"
        my_message = json.dumps(my_data)
        xfunc.sendDataToAgent(MQTT_TOPIC_DATAFEED, my_message)
        log.debug("sendDataToAgent: " + my_data["name"] + " = " + my_data["value"] + " on " + MQTT_TOPIC_DATAFEED)

        #---------------------
        end_time = arrow.now()
        # Calculate the time difference in seconds
        time_difference_seconds = (end_time - start_time).total_seconds()
        my_sleep_time = agent_period_secs - time_difference_seconds
        print("Sleeping for " + str(my_sleep_time) + " secs")
        time.sleep(my_sleep_time)
        
# Asynchronous function to read from stdin
async def async_input(prompt):
    with ThreadPoolExecutor(1) as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

#-----------------------------------------------------

# Main async function
async def main():
    # Set up MQTT client
    clientMQ.on_connect = on_connect
    clientMQ.on_message = on_message
    clientMQ.connect(MQTT_BROKER, MQTT_PORT, 60)
    clientMQ.subscribe(MQTT_TOPIC_TOCLIENT)
    clientMQ.subscribe(MQTT_TOPIC_TOASSISTANT)
    clientMQ.subscribe(MQTT_TOPIC_COMMAND)
    clientMQ.subscribe(MQTT_TOPIC_CONTROL)
    clientMQ.subscribe(MQTT_TOPIC_ALARM)
    clientMQ.subscribe(MQTT_TOPIC_NOTICE)
    clientMQ.subscribe(MQTT_TOPIC_ALERT)
    log.debug(SEPARATOR)
    log.debug("Connected to MQTT")
      
    # Start the MQTT client loop in a separate thread
    executer2 = ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executer2, clientMQ.loop_start)

   # Start worker in separate thread
    my_incoming_thread = threading.Thread(target=incoming_worker_thread)
    my_incoming_thread.daemon = True
    my_incoming_thread.start()

   # Start worker in separate thread
    my_outgoing_thread = threading.Thread(target=outgoing_worker_thread)
    my_outgoing_thread.daemon = True
    my_outgoing_thread.start()

    # Start worker in separate thread
    my_command_thread = threading.Thread(target=command_worker_thread)
    my_command_thread.daemon = True
    my_command_thread.start()

# Start worker in separate thread
    my_control_thread = threading.Thread(target=control_worker_thread)
    my_control_thread.daemon = True
    my_control_thread.start()

    # Start worker in separate thread
    my_alarm_thread = threading.Thread(target=alarm_worker_thread)
    my_alarm_thread.daemon = True
    my_alarm_thread.start()

    # Start worker in separate thread
    my_notice_thread = threading.Thread(target=notice_worker_thread)
    my_notice_thread.daemon = True
    my_notice_thread.start()

    # Start worker in separate thread
    my_alert_thread = threading.Thread(target=alert_worker_thread)
    my_alert_thread.daemon = True
    my_alert_thread.start()

   # Start main app function in separate thread
    my_main_run_thread = threading.Thread(target=main_run_thread)
    my_main_run_thread.daemon = True
    my_main_run_thread.start()

    try:
        speak_message("Hello. Source agent is starting.")
        while True:
            user_input = await async_input("Enter message (or type 'x' to quit): \n")
            if user_input.lower() == 'x':
                break

            process_local_message(user_input)
            
    finally:
        clientMQ.loop_stop()
        clientMQ.disconnect()

if __name__ == "__main__":

    config.setupRootLogger(log_file=agent_log_file)
    log = logging.getLogger("main")
    log.info("=============================")
    log.info("Logger initialized and ready.")

    if len(sys.argv) > 1:
        agent_name = sys.argv[1]
    else:
        pass

    print(f"Assistant Name: {agent_name}")
    asyncio.run(main())