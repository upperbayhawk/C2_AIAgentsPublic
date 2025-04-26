# ==============================================================================
# Module: runbroker.py
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

import json
import argparse
import math

import logbook
import arrow
import paho.mqtt.client as mqtt
#from thingspeaklib import XThingspeak
import openai
# for speech
import pygame

from datetime import datetime

from xutilslib import JSONHashTableDB
from xutilslib import VoterTally
from xutilslib import Watchdog
from xutilslib import ConvertDateTime
import config

agent_name = config.agent_name

logging_level = config.logging_level

# 10 min
agent_period_secs = 120

enable_mqtt_speech = False
enable_command_speech = False
enable_notice_speech = False
enable_control_speech = False
enable_alert_speech = False
enable_alarm_speech = False
enable_c2agent_speech = False
enable_c2agent_broker_speech = False

agent_output_file = "./data/broker_output.txt"
agent_log_file = "./logs/broker_log.txt"

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
MQTT_TOPIC_C2AGENT_BROKER = config.MQTT_TOPIC_C2AGENT_BROKER
SEPARATOR = "========================="

#-----------------------------------------------------

#logbook.FileHandler(agent_log_file,level=logging_level).push_application()
logHandler = logbook.TimedRotatingFileHandler(agent_log_file,level=logging_level,backup_count=30).push_application()
logbook.set_datetime_format("local")
log = logbook.Logger("runbroker", 0)
log.debug("Hello From Below: " + agent_name)

in_queue = queue.Queue()
out_queue = queue.Queue()
command_queue = queue.Queue()
control_queue = queue.Queue()
alarm_queue = queue.Queue()
notice_queue = queue.Queue()
alert_queue = queue.Queue()
c2agent_queue = queue.Queue()
c2agent_broker_queue = queue.Queue()

clientMQ = mqtt.Client()

clientAI = openai.OpenAI()

pygame.init()
pygame.mixer.init()

# for broker processing
msg_store =JSONHashTableDB()
msg_votetally =VoterTally()
msg_confidence = "low" #low = 1 match, med = 2 matches, high= 3 matches, veryhigh = 4 matches
msg_timer = Watchdog()
msg_timeout_seconds = 30
msg_reset_flag = False

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
    elif msg.topic == MQTT_TOPIC_C2AGENT:
        log.trace("To C2Agent: " + msg.topic + " " + pipe_input)
        print("To C2Agent: " + msg.topic + " " + pipe_input)
        process_c2agent_message(pipe_input)
    elif msg.topic == MQTT_TOPIC_C2AGENT_BROKER:
        log.trace("To C2AgentBroker: " + msg.topic + " " + pipe_input)
        print("To C2AgentBroker: " + msg.topic + " " + pipe_input)
        process_c2agent_broker_message(pipe_input)

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

def process_c2agent_message(message):
    log.trace("Processing C2Agent: " + message)
    c2agent_queue.put(message)  

def process_c2agent_broker_message(message):
    log.trace("Processing C2AgentBroker: " + message)
    c2agent_broker_queue.put(message)

def process_local_message(message):
    log.trace("Processing Local: " + message)
    clientMQ.publish(MQTT_TOPIC_TOASSISTANT, message)

#Threads
def incoming_worker_thread():
    while True:
        message = in_queue.get()
        if message is None:
            break
        log.debug("Incoming: " + message)
        print("Incoming: " + message)
        dispatch_incoming_message(message)

def outgoing_worker_thread():
    while True:
        message = out_queue.get()
        if message is None:
            break
        log.debug("Outgoing: " + message)
        print("Outgoing: " + message)
        dispatch_outgoing_message(message)
        
def command_worker_thread():
    while True:
        message = command_queue.get()
        if message is None:
            break
        log.debug("Command: " + message)
        print("Command: " + message)
        dispatch_command_message(message)

def control_worker_thread():
    while True:
        message = control_queue.get()
        if message is None:
            break
        log.debug("Control: " + message)
        print("Control: " + message)
        dispatch_control_message(message)

def alarm_worker_thread():
    while True:
        message = alarm_queue.get()
        if message is None:
            break
        log.debug("Alarm: " + message)
        print("Alarm: " + message)
        dispatch_alarm_message(message)

def notice_worker_thread():
    while True:
        message = notice_queue.get()
        if message is None:
            break
        log.debug("Notice: " + message)
        print("Notice: " + message)
        dispatch_notice_message(message)

def alert_worker_thread():
    while True:
        message = alert_queue.get()
        if message is None:
            break
        log.debug("Alert: " + message)
        print("Alert: " + message)
        dispatch_alert_message(message)

def c2agent_worker_thread():
    while True:
        message = c2agent_queue.get()
        if message is None:
            break
        log.debug("C2Agent: " + message)
        print("C2Agent: " + message)
        dispatch_c2agent_message(message)

def c2agent_broker_worker_thread():
    while True:
        message = c2agent_broker_queue.get()
        if message is None:
            break
        log.debug("C2AgentBroker: " + message)
        print("C2AgentBroker: " + message)
        dispatch_c2agent_broker_message(message)        
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
    my_message = "Command message " + message
    print (my_message)
    if enable_command_speech == True:
        speak_message(my_message)
    else:
        pass

def dispatch_control_message(message):
    my_message = "Control message " + message
    print (my_message)
    if enable_control_speech == True:
        speak_message(my_message)
    else:
        pass

def dispatch_alarm_message(message):
    my_message = "Alarm message " + message
    print (my_message)
    if enable_alarm_speech == True:
        speak_message(my_message)
    else:
        pass

def dispatch_notice_message(message):
    my_message = "Notice message " + message
    print (my_message)
    if enable_notice_speech == True:
        speak_message(my_message)
    else:
        pass

def dispatch_alert_message(message):
    my_message = "Alert message " + message
    print (my_message)
    if enable_alert_speech == True:
        speak_message(my_message)
    else:
        pass

def dispatch_c2agent_message(message):
    my_message = "C2Agent message " + message
    print (my_message)
    if enable_c2agent_speech == True:
        speak_message(my_message)
    else:
        pass
#=======================================
def dispatch_c2agent_broker_message(message):
    global msg_reset_flag
    global msg_store
    global msg_timer
    global msg_timeout_seconds
    
    my_message = "C2AgentBroker message " + message
    print (my_message)
    if enable_c2agent_broker_speech == True:
        speak_message(my_message)
    #store count == 0-n
    #msg count == 1-n+1

    if msg_reset_flag is True:
        msg_store.clear_all()
        log.debug("Cleared store")
        log.debug("Store cnt: " + str(msg_store.count()))
        msg_reset_flag = False

    log.debug("Store cnt: " + str(msg_store.count()))
    my_index = msg_store.count() + 1
    msg_store.add(my_index, message)
    log.info("added: " + str(my_index) + "," + message)
    
    if my_index == 1:
        msg_timer.start(msg_timeout_seconds, broker_message_timeout)

#=======================================
def court_verdict():
    global msg_confidence
    global msg_store
    
    msg_min_matches = 0
    
    if msg_confidence == "low":
        msg_min_matches = 1

    if msg_confidence == "med":
        msg_min_matches = 2

    if msg_confidence == "high":    
        msg_min_matches = 3

    if msg_confidence == "veryhigh":    
        msg_min_matches = 4

    msg_count = msg_store.count()
    if msg_count == 1:
        log.info("court_verdict: HUNG JURY! Only 1 model received!")
        return "NONE"
    
    if msg_count > 1:
        # compare 1 and 2, if equal send C2Agent message
        #                                      
        # if quorum = 2, then max matches == 2, 2+2-2 = 2/2, 2*2-2/2 = 1
        # if quorum = 3, then max matches == 3, 3+3+3-3 =6/2=3, 3*3-3/2 =3
        # if quorum = 4, then max matches == 6, 4+4+4+4-4= 12/2=6, 4*4-4/2=6
        # if quorum = 5, then max matches == 10, 5+5+5+5+5-5= 20/2=10, 5*5-5/2=10
        
        good_msg = "NONE"
        matches = 0
        msg_votetally.clear_all()
        for i in range(1, msg_count + 1, 1):
            vote_counter = 0
            
            for j in range(1, msg_count + 1, 1):
                if i != j: # don't compare to self
                    
                   
                    log.debug("i: " + str(i))
                    log.debug("j: " + str(j))
                    msg1 = msg_store.read_one(i)
                    log.debug("msgi: " + msg1)
                    msg2 = msg_store.read_one(j)
                    log.debug("msgj: " + msg2)
                
                    if broker_compare_messages(msg1,msg2) == True:
                        good_msg = msg1
                        matches = matches + 1
                        vote_counter = vote_counter + 1
                    
            msg_votetally.add((i), vote_counter)

        highest_votes = 0
        for i in range(1, msg_count + 1, 1):
            num_of_votes = msg_votetally.read_one(i)
            msg = msg_store.read_one(i)
            data = json.loads(msg)
            model = data["agent_name"]
            log.info("VOTES for " + str(i) + " : " + model + " : " + str(num_of_votes))
            if num_of_votes > highest_votes:
                highest_votes = num_of_votes
        #get winner
        if highest_votes < msg_min_matches:
            log.info("NO WINNER!!!!")
            return "NONE"

        for i in range(1, msg_count + 1, 1):
            num_of_votes = msg_votetally.read_one(i)
            if num_of_votes == highest_votes:
                winner_msg = msg_store.read_one(i)
                log.info("THE WINNER IS: " + str(i) + " : " + winner_msg)
                return winner_msg

        #if something happened
        # log.debug("TOTAL MATCHES = " + str(matches)) # including reverse tests

        # if matches >= msg_min_matches:
        #     if good_msg != "NONE":
        #         log.debug("PASSED: Matches: " + str(matches/2))
        #         log.debug("PASSED: Minimum matches: " + str(msg_min_matches/2))
        #         log.debug("PASSED: Good_msg: " + good_msg)
        #         return good_msg
        # else:
        #     log.debug("FAILED: not enought matches: " + str(matches))
        #     return "NONE"

        # #3*3-3
       
        
        # if msg_min_matches * 2 > max_match_threshold:
        #     log.debug("msg_min_matches > max_match_threshold")
        #     log.debug(str(msg_min_matches), ">", str(max_match_threshold))

        # actual matches = /2
        # matches = matches/2
        # if matches >= msg_min_matches:
        #     log.debug("COURT VERDICT == TRUE")
        #     return msg1
        # else:
        #     log.debug("NO MATCHES")
        #     return "NONE"
    else:
        pass
        return "NONE"

def broker_compare_messages(msg1,msg2):
    
    try:
        data1 = json.loads(msg1)
        msg1_start_date_time = data1["start_date_time"]
        convertDateTime = ConvertDateTime()
        dt1 = convertDateTime.convert(msg1_start_date_time)
        msg1_peak_lmp = data1["peak_lmp"]
        flmp1 = float(msg1_peak_lmp)
        ilmp1 = int(flmp1)
        msg1_award_level = data1["award_level"]
        msg1_agent_name = data1["agent_name"]
        #--------------------
        data2 = json.loads(msg2)
        msg2_start_date_time = data2["start_date_time"]
        dt2 = convertDateTime.convert(msg2_start_date_time)
        msg2_peak_lmp = data2["peak_lmp"]
        flmp2 = float(msg2_peak_lmp)
        ilmp2 = int(flmp2)
        msg2_award_level = data2["award_level"]
        msg2_agent_name = data2["agent_name"]
        #---------------------
        failed_test = False
                    
        log.debug("STARTING TEST")
    
        if dt1 == dt2:
            if ilmp1 == ilmp2:
                if msg1_award_level == msg2_award_level:
                    log.debug("BINGO: " + msg1)
                    print("BINGO: " + msg1)
                else:
                    log.info("FAILED: AWARD LEVEL DOES NOT MATCH: " + msg1_agent_name + " != " + msg2_agent_name)
                    log.info("FAILED: AWARD LEVEL DOES NOT MATCH: " + msg1_award_level + " != " + msg2_award_level)
                    print("FAILED: AWARD LEVEL DOES NOT MATCH: " + msg1_award_level + " != " + msg2_award_level)
                    failed_test = True
            else:
                log.info("FAILED: PEAK LMP DOES NOT MATCH: " + msg1_agent_name + " != " + msg2_agent_name)
                log.info("FAILED: PEAK LMP DOES NOT MATCH: " + msg1_peak_lmp + " != " + msg2_peak_lmp)
                print("FAILED: PEAK LMP DOES NOT MATCH: " + msg1_peak_lmp + " != " + msg2_peak_lmp)
                failed_test = True
        else:
            log.info("FAILED: DATETIME DOES NOT MATCH: " + msg1_agent_name + " != " + msg2_agent_name)
            log.info("FAILED: DATETIME DOES NOT MATCH: " + msg1_start_date_time + " != " + msg2_start_date_time)
            print("FAILED: DATETIME DOES NOT MATCH: " + msg1_start_date_time + " != "  + msg2_start_date_time)
            failed_test = True
        
        log.debug("ENDING TEST")
        
        if failed_test == True:
            pass
            log.debug("BOGUS: " + msg1)
            log.debug("BOGUS: " + msg2)
            print("BOGUS: " + msg2)
            # print("BOGUS: " + msg1)
            # print("BOGUS: " + msg2)
            # print("all records: ", msg_store.read_all()
            return False
        else:
            pass
            log.debug("BINGO: " + msg1)
            log.debug("BINGO: " + msg2)
            print("BINGO: " + msg2)
            return True

    except Exception as e:
        print(f"FAILED: broker_compare_messages: An Exception occurred: {e}")
        log.error(f"FAILED: broker_compare_messages: An Exception occurred: {e}")
        return False


def broker_message_timeout():
    global msg_reset_flag
    #Just do it
    try:
        msg_reset_flag = True
        print("Message Timer Fired")
        log.debug("Message Timer Fired")
        verdict = court_verdict()
        if verdict != "NONE":
            log.info("TIMER_SENT C2AGENT Msg: " + verdict)
            print("TIMER_SENT C2AGENT Msg: " + verdict)
            clientMQ.publish(MQTT_TOPIC_C2AGENT, verdict)
        else:
            print("TIMER COURT VERDICT NONE: DON'T SEND MESSAGE")
            log.info("TIMER COURT VERDICT NONE: DON'T SEND MESSAGE")
    except Exception as e:
        print(f"broker_message_timeout: An Exception occurred: {e}")
        log.error(f"broker_message_timeout: An Exception occurred: {e}")

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

        #pygame.init()
        #pygame.mixer.init()
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
        #print("Broker Running...")
        #---------------------
        end_time = arrow.now()
        # Calculate the time difference in seconds
        time_difference_seconds = (end_time - start_time).total_seconds()
        my_sleep_time = agent_period_secs - time_difference_seconds
        #print("Sleeping for " + str(my_sleep_time) + " secs")
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
    clientMQ.subscribe(MQTT_TOPIC_C2AGENT)
    clientMQ.subscribe(MQTT_TOPIC_C2AGENT_BROKER)
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

    # Start worker in separate thread
    my_c2agent_thread = threading.Thread(target=c2agent_worker_thread)
    my_c2agent_thread.daemon = True
    my_c2agent_thread.start()

  # Start worker in separate thread
    my_c2agent_broker_thread = threading.Thread(target=c2agent_broker_worker_thread)
    my_c2agent_broker_thread.daemon = True
    my_c2agent_broker_thread.start()

   # Start main app function in separate thread
    my_main_run_thread = threading.Thread(target=main_run_thread)
    my_main_run_thread.daemon = True
    my_main_run_thread.start()

    try:
        speak_message("Hello. Broker agent is starting")

        

        while True:
            user_input = await async_input("Enter message (or type 'x' to quit): \n")
            if user_input.lower() == 'x':
                break

            process_local_message(user_input)
            
    finally:
        clientMQ.loop_stop()
        clientMQ.disconnect()

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Alien World")
    parser.add_argument("--name", help="Name of the Agent")
    parser.add_argument("--confidence", help="Confidence Level: low(1), med(2), high(3), veryhigh(4)")
    parser.add_argument("--timeout", help="Timeout in seconds")
    args = parser.parse_args()

    if args.name:
        print(f"Agent Name: {args.name}.")
        agent_name = args.name
    else:
        print(f"Agent Name: {agent_name}.")

    if args.confidence:
        print(f"Confidence Level: {args.confidence}.")
        msg_confidence = args.confidence
    else:
        print(f"Confidence Level Default: {msg_confidence}.")

    if args.timeout:
        print(f"Timeout Seconds: {args.timeout}.")
        msg_timeout_seconds = int(args.timeout)
    else:
        print(f"Timeout Seconds Default: {str(msg_timeout_seconds)}.")



    asyncio.run(main())