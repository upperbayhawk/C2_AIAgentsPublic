# ==============================================================================
# Module: runclient.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Console app that sends MQTT prompt messages to 
#   and from runserver.py
# Notes:
# ==============================================================================

import asyncio
import sys
import queue
import threading
from concurrent.futures import ThreadPoolExecutor

import logbook
import paho.mqtt.client as mqtt

import config

agent_name = config.agent_name

logging_level = config.logging_level

agent_output_file = "./data/client_output.txt"
agent_log_file = "./logs/client_log.txt"

MQTT_BROKER = config.MQTT_BROKER
MQTT_PORT = config.MQTT_PORT
MQTT_TOPIC_TOASSISTANT = config.MQTT_TOPIC_TOASSISTANT
MQTT_TOPIC_TOCLIENT = config.MQTT_TOPIC_TOCLIENT
SEPARATOR = "========================="

#-----------------------------------------------------

#logbook.FileHandler(agent_log_file,level=logging_level).push_application()
logHandler = logbook.TimedRotatingFileHandler(agent_log_file,level=logging_level,backup_count=30).push_application()
logbook.set_datetime_format("local")
log = logbook.Logger("runclient", 0)
log.debug("Hello From Below: " + agent_name)

in_queue = queue.Queue()
out_queue = queue.Queue()

clientMQ = mqtt.Client()

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

def process_incoming_message(message):
    log.trace("Processing Incoming: " + message)
    in_queue.put(message)

def process_outgoing_message(message):
    log.trace("Processing Outgoing: " + message)
    out_queue.put(message)

def process_local_message(message):
    log.trace("Processing Local: " + message)
    clientMQ.publish(MQTT_TOPIC_TOASSISTANT, message)

def incoming_worker_thread():
    while True:
        message = in_queue.get()
        if message is None:
            break
        log.debug(message)
        print(message)        

def outgoing_worker_thread():
    while True:
        message = out_queue.get()
        if message is None:
            break
        log.debug(message)
        print(message)

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
    
    log.debug(SEPARATOR)
    log.debug("Connected to MQTT")
      
    # Start the MQTT client loop in a separate thread
    executer2 = ThreadPoolExecutor(max_workers=3)
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