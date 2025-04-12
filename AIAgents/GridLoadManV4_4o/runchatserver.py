# ==============================================================================
# Module: runchatserver.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Console app, the main proxy server for the OpenAI Assistant
# Notes:
# ==============================================================================

import asyncio
import sys
import os
import queue
import threading
import json
from concurrent.futures import ThreadPoolExecutor

import logbook
import arrow
import paho.mqtt.client as mqtt
import openai
import pygame

from xcachelib import data_cache_instance
import openaichatlib
#from openaichatlib import openaichatlib_instance
import config
from xfunctionlib import XFunction

agent_name = config.agent_name

logging_level = config.logging_level

agent_output_file = "./data/server_output.txt"
agent_log_file = "./logs/server_log.txt"
agent_init_prompt_file = "./prompts/InitialPrompt.txt"
agent_init_instructions_file = "./prompts/InitialInstructions.txt"

MQTT_BROKER = config.MQTT_BROKER
MQTT_PORT = config.MQTT_PORT
MQTT_TOPIC_TOASSISTANT = config.MQTT_TOPIC_TOASSISTANT
MQTT_TOPIC_TOCLIENT = config.MQTT_TOPIC_TOCLIENT
MQTT_TOPIC_DATAFEED = config.MQTT_TOPIC_DATAFEED
MQTT_TOPIC_OPCUA = config.MQTT_TOPIC_OPCUA
SEPARATOR = "======================"

#-----------------------------------------------------

#logbook.FileHandler(agent_log_file,level=logging_level).push_application()
logHandler = logbook.TimedRotatingFileHandler(agent_log_file,level=logging_level,backup_count=30).push_application()
logbook.set_datetime_format("local")
log = logbook.Logger("runserver")
log.debug("Hello From Below: " + agent_name)
#-----------------------------------------------------
in_queue = queue.Queue()
datafeed_queue = queue.Queue()
opcua_queue = queue.Queue()

clientMQ = mqtt.Client()
clientAI = openai.OpenAI()

openaichatlib_instance = openaichatlib.OpenAIChatLib()

# MQTT Callbacks
def on_connect(client, userdata, flags, rc):
    log.debug(f"Connected with result code {rc}")

def on_message(client, userdata, msg):
    log.debug(f"Received message '{msg.payload.decode()}' on topic '{msg.topic}'")
    pipe_input = str(msg.payload.decode())
    if msg.topic == MQTT_TOPIC_TOASSISTANT:
        log.debug("To Assistant Inbound: " + msg.topic + " " + pipe_input)
        print("To Assistant Inbound: " + msg.topic + " " + pipe_input)
        process_incoming_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_TOCLIENT:
        log.debug("To Client Outbound: " + msg.topic + " " + pipe_input)
        print("To Client Outbound: " + msg.topic + " " + pipe_input)
        process_outgoing_message(pipe_input)
        pass
    elif msg.topic == MQTT_TOPIC_DATAFEED:
        #log.debug("To DataFeed: " + msg.topic + " " + pipe_input)
        #print("To DataFeed: " + msg.topic + " " + pipe_input)
        process_datafeed_message(pipe_input)
        pass
    elif msg.topic == MQTT_TOPIC_OPCUA:
        #log.debug("To OPCUA: " + msg.topic + " " + pipe_input)
        #print("To OPCUA: " + msg.topic + " " + pipe_input)
        process_opcua_message(pipe_input)
        pass

# Asynchronous function to read from stdin
async def async_input(prompt):
    with ThreadPoolExecutor(1) as executor:
        return await asyncio.get_event_loop().run_in_executor(executor, input, prompt)

# Message Processors
def process_incoming_message(message):
    log.trace("Processing Incoming: " + message)
    in_queue.put(message)

def process_outgoing_message(message):
    log.trace("Processing Outgoing: " + message)
    #out_queue.put(message)

def process_local_message(message):
    log.trace("Processing Local: " + message)
    in_queue.put(message)

def process_datafeed_message(message):
    log.trace("Processing DataFeed: " + message)
    datafeed_queue.put(message)

def process_opcua_message(message):
    log.trace("Processing OPCUA: " + message)
    opcua_queue.put(message)

def datafeed_worker_thread():
    while True:
        message = datafeed_queue.get()
        if message is None:
            break
        data = json.loads(message)
        tagname = data["name"]
        tagvalue = data["value"]
        tagstatus = data["status"]
        data_cache_instance.write(tagname, tagvalue,tagstatus)
        value =  data_cache_instance.read(tagname)
        #log.debug("value from cache = "  + value)

def opcua_worker_thread():
    while True:
        message = opcua_queue.get()
        if message is None:
            break
        data = json.loads(message)
        payload = data["Payload"]
        for tagname, tagvalue in payload.items():
            tagstatus = "OK"
            data_cache_instance.write(tagname, tagvalue,tagstatus)
            value =  data_cache_instance.read(tagname)
            #print (tagname + " = " + str(tagvalue) + ":" + value)
            #log.debug("value from cache = "  + value)

# Main worker thread
def main_worker_thread():
    while True:
        try:
            message = in_queue.get()
            if message is not None:
                if len(message) > 2:
                    openaichatlib_instance.initialize(agent_name,agent_init_prompt_file,agent_init_instructions_file,agent_output_file)
                    msg_return = openaichatlib_instance.run(message)
                    if msg_return == "OK":
                        last_message = openaichatlib_instance.last_message
                        if last_message != "NULL":
                            log.debug("Finished and publishing results to client: " + last_message)

                            clientMQ.publish(MQTT_TOPIC_TOCLIENT, last_message)
                            log.debug("last_message: " + last_message)
                        else:
                            log.error("WORKER ERROR. Last message is null.")
                            clientMQ.publish(MQTT_TOPIC_TOCLIENT,"ERROR")
                    else:
                        log.error("WORKER ERROR PROCESSING INPUT")
                        clientMQ.publish(MQTT_TOPIC_TOCLIENT,"ERROR")
        except Exception as ex:
            log.error("Exception " + str(ex))
            print ("Exception " + str(ex))
#-------------------------------------------------------
# voices = alloy,echo,fable,onyx,nova,shimmer
def speak_message(message):
    try:
        speech_file_path = "data/runserver.mp3"
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
# Main async function
async def main():
    # Set up MQTT client
    clientMQ.on_connect = on_connect
    clientMQ.on_message = on_message
    clientMQ.connect(MQTT_BROKER, MQTT_PORT, 60)
    clientMQ.subscribe(MQTT_TOPIC_TOCLIENT)
    clientMQ.subscribe(MQTT_TOPIC_TOASSISTANT)
    clientMQ.subscribe(MQTT_TOPIC_DATAFEED)
    clientMQ.subscribe(MQTT_TOPIC_OPCUA)

    with open(agent_output_file, "a", encoding="utf-8") as file:
        file.write("\n" + SEPARATOR + "\n\n")
    
    # Start the MQTT client loop in a separate thread
    executer2 = ThreadPoolExecutor(max_workers=10)
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(executer2, clientMQ.loop_start)

    # Start worker in separate thread
    my_main_thread = threading.Thread(target=main_worker_thread)
    my_main_thread.daemon = True
    my_main_thread.start()
    
    # Start worker in separate thread
    my_datafeed_thread = threading.Thread(target=datafeed_worker_thread)
    my_datafeed_thread.daemon = True
    my_datafeed_thread.start()

    # Start worker in separate thread
    my_opcua_thread = threading.Thread(target=opcua_worker_thread)
    my_opcua_thread.daemon = True
    my_opcua_thread.start()

    
    #try:
    #    openaichatlib_instance.initialize(agent_name,agent_init_prompt_file,agent_init_instructions_file,agent_output_file)
    #except Exception as ex:
    #    log.error("Exception openaichatlib_instance.initialize: " + str(ex))
    #    print ("Exception openaichatlib_instance.initialize: " + str(ex))
   
    try:
        speak_message("Hello. The server agent is starting")
        while True:
            
            user_input = await async_input("Enter message (or type 'x' to quit): ")
            if user_input.lower() == 'x':
                break

            print(user_input)
            log.debug(user_input)

            utc= arrow.utcnow()
            local=utc.to('US/Eastern')
            print ("Time " + str(local) + "\n")

            process_local_message(user_input)

    finally:
        clientMQ.loop_stop()
        clientMQ.disconnect()
        

if __name__ == "__main__":

    if len(sys.argv) > 1:
        agent_name = sys.argv[1]
    else:
        pass
    
    print(f"Agent Name: {agent_name}")        
    asyncio.run(main())