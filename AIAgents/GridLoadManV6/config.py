# ==============================================================================
# Module: config.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Agent configuration parameters
# Notes:
# ==============================================================================

import os
import logging
from logging.handlers import TimedRotatingFileHandler
from datetime import datetime

agent_name = "GridLoadMan-2-0-0"

# AI model and endpoint



models = [
    {"name": "OPENAI", 
        "model": "gpt-4.1", 
        "key": "VOID", 
        "url":"VOID"},
    {"name": "OPENAIMINI", 
        "model": "04-mini", 
        "key": "VOID", 
        "url":"VOID"},
    {"name": "OPENAIO3", 
        "model": "O3", 
        "key": "VOID", 
        "url":"VOID"},
    {"name": "GROK", 
        "model": "grok-3-mini-beta", 
        "key": "", 
        "url":"https://api.x.ai/v1"},
    {"name": "GOOGLE", 
        "model": "gemini-2.5-pro-exp-03-25", 
        "key": "", 
        "url":"https://generativelanguage.googleapis.com/v1beta/openai/"},
    {"name": "OPENAI45", 
        "model": "gpt-4.5-preview", 
        "key": "VOID", 
        "url":"VOID"},
    {"name": "LAMA",
        "model": "llama-4-scout-17b-16e-instruct",
        "key": "VOID",
        "url": "http://192.168.0.138:1234/v1/"},
    {"name": "CLAUDE",
        "model": "claude-3-7-sonnet-20250219 (claude-3-7-sonnet-latest)",
        "key": "",
        "url": "https://api.anthropic.com/v1/models"},
    {"name": "DEEPSEEK",
        "model": "deepseek-chat",
        "key": "",
        "url": "https://api.deepseek.com/"},
    {"name": "PHI",
        "model": "phi-4",
        "key": "VOID",
        "url": "http://192.168.56.1:1234/v1/"},
    {"name": "NEMO",
        "model": "openmath-nemotron-32b",
        "key": "VOID",
        "url": "http://192.168.0.138:1234/v1/"},
    {"name": "BABYNEMO",
        "model": "openmath-nemotron-14b",
        "key": "VOID",
        "url": "http://192.168.0.138:1234/v1/"},
    {"name": "GEMMA",
        "model": "gemma-3-27b-it-qat",
        "key": "VOID",
        "url": "http://192.168.0.138:1234/v1/"},
    {"name": "QWEN",
        "model": "qwen3-32b",
        "key": "VOID",
        "url": "http://192.168.0.198:1234/v1/"}
    ]

# Default Model

AI_NAME = "OPENAI"
AI_MODEL = "gpt-4o"
AI_KEY = "VOID"
AI_URL = "VOID"



# MQTT Broker settings. USE IP or "localhost".
MQTT_BROKER = "192.168.0.111"
MQTT_PORT = 1883
mqtt_base_topic = "openai/assistant/"
mqtt_base_topic_c2agent = "C2Agent"
mqtt_base_topic_c2agent_broker = "C2AgentBroker"

mqtt_message_broker_enable = False

MQTT_TOPIC_TOASSISTANT = mqtt_base_topic + agent_name + "/ToAssistant"
MQTT_TOPIC_TOCLIENT = mqtt_base_topic + agent_name + "/ToClient"
#
MQTT_TOPIC_COMMAND = mqtt_base_topic + agent_name + "/CommandCenter"
MQTT_TOPIC_CONTROL = mqtt_base_topic + agent_name + "/ControlPanel"
MQTT_TOPIC_ALARM = mqtt_base_topic + agent_name + "/AlarmPanel"
MQTT_TOPIC_NOTICE = mqtt_base_topic + agent_name + "/NoticePanel"
MQTT_TOPIC_ALERT = mqtt_base_topic + agent_name + "/AlertPanel"
MQTT_TOPIC_C2AGENT = mqtt_base_topic_c2agent
MQTT_TOPIC_C2AGENT_BROKER = mqtt_base_topic_c2agent_broker
#
MQTT_TOPIC_DATAFEED = mqtt_base_topic + agent_name + "/DataFeed"
MQTT_TOPIC_OPCUA = "Site_Riverdale/ProcessCell_South/Unit2_Boiler"
# Logger level DEBUG, INFO

logging_level = logging.INFO

ai_polling_interval = 1



class GridPeakDetected:
    def __init__ (self, type_name, agent_name, message, start_date_time, duration_mins, peak_lmp, grid_node,award_level,game_type):
        self.type_name = type_name
        self.agent_name = agent_name
        self.message = message
        self.start_date_time = start_date_time
        self.duration_mins = duration_mins
        self.peak_lmp = peak_lmp
        self.grid_node = grid_node
        self.award_level = award_level
        self.game_type = game_type

class PreExtensionTimedRotatingFileHandler(TimedRotatingFileHandler):
    def rotation_filename(self, default_name):
        # default_name = full path like logs/app.log.2025-05-16
        base, ext = os.path.splitext(self.baseFilename)
        d = datetime.now().strftime(self.suffix)
        return f"{base}.{d}{ext}"
    
def setupRootLogger(log_file="app.log", when="midnight", interval=1, backup_count=7):
    # Create log directory if it doesn't exist
    # Full path to the log file
    
 # Create root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(logging_level)

    # Define log format
    formatter = logging.Formatter(
        '%(asctime)s [%(levelname)s] %(name)s.%(funcName)s: %(message)s'
    )

    # Console handler
    # console_handler = logging.StreamHandler()
    # console_handler.setLevel(logging.INFO)
    # console_handler.setFormatter(formatter)

    # Timed rotating file handler
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when='midnight',
        interval=1,
        backupCount=7,
        encoding='utf-8'
    )

    # file_handler = PreExtensionTimedRotatingFileHandler(
    #     filename=log_file,
    #     when="midnight",
    #     backupCount=7,
    #     encoding="utf-8"
    # )

    file_handler.suffix = "%Y-%m-%d"  # Add date suffix to rotated logs
    file_handler.setLevel(logging_level)
    file_handler.setFormatter(formatter)

    # Avoid duplicate logs by clearing previous handlers
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    # Attach handlers
    #root_logger.addHandler(console_handler)
    root_logger.addHandler(file_handler)

    logging.getLogger("openai").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("asyncio").setLevel(logging.WARNING)
        