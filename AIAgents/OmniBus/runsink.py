# ==============================================================================
# Module: runsink.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Console app that receives and acts on 
#   MQTT messages from the OpenAI Assistant.
# Notes:
# ==============================================================================

import os
import sys
import asyncio
import queue
import threading
from pathlib import Path
import time
from concurrent.futures import ThreadPoolExecutor

import logbook
import arrow
import paho.mqtt.client as mqtt
from thingspeaklib import XThingspeak
from openai import OpenAI
# for speech
import pygame

import config

agent_name = config.agent_name

logging_level = config.logging_level

# 10 min
agent_period_secs = 120

enable_mqtt_speech = False
enable_command_speech = False
enable_notice_speech = False
enable_control_speech = False
enable_alert_speech = True
enable_alarm_speech = False

agent_output_file = "./data/sink_output.txt"
agent_log_file = "./logs/sink_log.txt"

MQTT_BROKER = config.MQTT_BROKER
MQTT_PORT = config.MQTT_PORT
MQTT_TOPIC_TOASSISTANT = config.MQTT_TOPIC_TOASSISTANT
MQTT_TOPIC_TOCLIENT = config.MQTT_TOPIC_TOCLIENT

MQTT_TOPIC_COMMAND = config.MQTT_TOPIC_COMMAND
MQTT_TOPIC_CONTROL = config.MQTT_TOPIC_CONTROL
MQTT_TOPIC_ALARM = config.MQTT_TOPIC_ALARM
MQTT_TOPIC_NOTICE = config.MQTT_TOPIC_NOTICE
MQTT_TOPIC_ALERT = config.MQTT_TOPIC_ALERT
SEPARATOR = "========================="

#-----------------------------------------------------

logbook.FileHandler(agent_log_file,level=logging_level).push_application()
log = logbook.Logger("runsink", 0)
log.debug("Hello From Below: " + agent_name)

in_queue = queue.Queue()
out_queue = queue.Queue()
command_queue = queue.Queue()
control_queue = queue.Queue()
alarm_queue = queue.Queue()
notice_queue = queue.Queue()
alert_queue = queue.Queue()

clientMQ = mqtt.Client()

clientAI = OpenAI()

#-----------------------------------------------------

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    log.debug(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    log.trace(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    pipe_input = str(msg.payload.decode())
    if msg.topic == MQTT_TOPIC_TOASSISTANT:
        log.trace("To Assistant Inbound: " + msg.topic + " " + pipe_input)
        print("To Assistant Inbound: " + msg.topic + " " + pipe_input)
        process_outgoing_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_TOCLIENT:
        log.trace("To Client Outbound: " + msg.topic + " " + pipe_input)
        print("To Client Outbound: " + msg.topic + " " + pipe_input)
        process_incoming_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_COMMAND:
        log.trace("To Command: " + msg.topic + " " + pipe_input)
        print("To Command: " + msg.topic + " " + pipe_input)
        process_commandcenter_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_CONTROL:
        log.trace("To Control: " + msg.topic + " " + pipe_input)
        print("To Control: " + msg.topic + " " + pipe_input)
        process_control_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_ALARM:
        log.trace("To Alarm: " + msg.topic + " " + pipe_input)
        print("To Alarm: " + msg.topic + " " + pipe_input)
        process_alarm_message(pipe_input)        
    elif msg.topic == MQTT_TOPIC_NOTICE:
        log.trace("To Notice: " + msg.topic + " " + pipe_input)
        print("To Notice: " + msg.topic + " " + pipe_input)
        process_notice_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_ALERT:
        log.trace("To Alert: " + msg.topic + " " + pipe_input)
        print("To Alert: " + msg.topic + " " + pipe_input)
        process_alert_message(pipe_input)

# Message Processors
def process_incoming_message(message):
    log.trace("Processing Incoming: " + message)
    in_queue.put(message)

def process_outgoing_message(message):
    log.trace("Processing Outgoing: " + message)
    out_queue.put(message)

def process_commandcenter_message(message):
    log.trace("Processing Command: " + message)
    command_queue.put(message)

def process_control_message(message):
    log.trace("Processing Control: " + message)
    control_queue.put(message)

def process_alarm_message(message):
    log.trace("Processing Alarm: " + message)
    alarm_queue.put(message)

def process_notice_message(message):
    log.trace("Processing Notice: " + message)
    notice_queue.put(message)    

def process_alert_message(message):
    log.trace("Processing Alert: " + message)
    alert_queue.put(message)  

def process_local_message(message):
    log.trace("Processing Local: " + message)
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
#Application functions
def dispatch_incoming_message(message):
    if enable_mqtt_speech == True:
        speak_message(message)
    else:
        pass

#Application functions
def dispatch_outgoing_message(message):
    if enable_mqtt_speech == True:
        speak_message(message)
    else:
        pass

def dispatch_command_message(message):
    if enable_command_speech == True:
        my_message = "Command message " + message
        print (my_message)
        speak_message(my_message)
    else:
        pass

def dispatch_control_message(message):
    if enable_control_speech == True:
        my_message = "Control message " + message
        print (my_message)
        speak_message(my_message)
    else:
        pass

def dispatch_alarm_message(message):
    if enable_alarm_speech == True:
        my_message = "Alarm message " + message
        print (my_message)
        speak_message(my_message)
    else:
        pass

def dispatch_notice_message(message):
    if enable_notice_speech == True:
        my_message = "Notice message " + message
        print (my_message)
        speak_message(my_message)
    else:
        pass

def dispatch_alert_message(message):
    if enable_alert_speech == True:
        my_message = "Alert message " + message
        print (my_message)
        speak_message(my_message)
    else:
        pass

#=============================================
# voices = alloy,echo,fable,onyx,nova,shimmer
def speak_message(message):
    try:
        speech_file_path = "data/runsink.mp3"
        response = clientAI.audio.speech.create(
        model="tts-1-hd",
        #voice="nova",
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
        print("Running...")
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
        while True:
            user_input = await async_input("Enter message (or type 'x' to quit): \n")
            if user_input.lower() == 'x':
                break

            process_local_message(user_input)
            
    finally:
        clientMQ.loop_stop()
        clientMQ.disconnect()

if __name__ == "__main__":

    if len(sys.argv) > 1:
        agent_name = sys.argv[1]
    else:
        pass

    print(f"Assistant Name: {agent_name}")
    asyncio.run(main())