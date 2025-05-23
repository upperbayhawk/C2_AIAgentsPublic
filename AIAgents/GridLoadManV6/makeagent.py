# ==============================================================================
# Module: makeagent.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Creates the OpenAI Assistant
# Notes:
# ==============================================================================


from openai import OpenAI

import config

agent_name = config.agent_name

# RETRIEVAL: These files are uploaded when agent is born if Assistant has retrieval
#agent_base_file = "./data/AgentBase.txt"
#agent_data_file = "./data/LMP_LOAD.csv"
#
agent_instructions_file = "./prompts/AgentInstructions.txt"
#agent_model="o1-preview"
#agent_model="o1-preview-2024-09-12"
#agent_model="o1-mini-2024-09-12"
#agent_model="gpt-4o"
#agent_model="gpt-4o-2024-08-06"
agent_model=config.AI_MODEL
#agent_model="gpt-3.5-turbo-0125"
#agent_model="gpt-4-0125-preview"
#agent_tools=[{"type": "code_interpreter"},{"type":"file_search"}],
#agent_tools=[{"type": "file_search"}]
#agent_tools=[{"type": "code_interpreter"}]
# code_interpreter with function callbacks

#agent_tools=[{"type": "code_interpreter"},{
agent_tools=[{
    "type": "function",
    "function": {
      "name": "sendAlarmSignalToNetworkNode",
      "description": "Send an alarm signal to a destination network node.",
      "parameters": {
        "type": "object",
        "properties": {
          "network_node": {"type": "string", "description": "The name of a node on the network. Network node names include AlarmPanel, ControlPanel, NoticePanel, AlertPanel, CommandCenter."},
          "message": {"type": "string", "description": "The contents of the alarm signal message."},
        },
        "required": ["network_node", "message"]
      }
    }
  }, {
    "type": "function",
    "function": {
      "name": "sendControlSignalToNetworkNode",
      "description": "Send a control signal to a destination network node.",
      "parameters": {
        "type": "object",
        "properties": {
          "network_node": {"type": "string", "description": "The name of a node on the network. Network node names include AlarmPanel, ControlPanel, NoticePanel, AlertPanel, CommandCenter."},
          "message": {"type": "string", "description": "The contents of the control signal message."},
        },
        "required": ["network_node", "message"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "sendNoticeSignalToNetworkNode",
      "description": "Send a notice signal to a destination network node.",
      "parameters": {
        "type": "object",
        "properties": {
          "network_node": {"type": "string", "description": "The name of a node on the network. Network node names include AlarmPanel, ControlPanel, NoticePanel, AlertPanel, CommandCenter."},
          "message": {"type": "string", "description": "The contents of the notice signal message."},
        },
        "required": ["network_node", "message"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "sendCommandSignalToNetworkNode",
      "description": "Send a command signal to a destination network node.",
      "parameters": {
        "type": "object",
        "properties": {
          "network_node": {"type": "string", "description": "The name of a node on the network. Network node names include AlarmPanel, ControlPanel, NoticePanel, AlertPanel, CommandCenter."},
          "message": {"type": "string", "description": "The contents of the command signal message."},
        },
        "required": ["network_node", "message"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "sendAlertSignalToNetworkNode",
      "description": "Send an alert signal to a destination network node.",
      "parameters": {
        "type": "object",
        "properties": {
          "network_node": {"type": "string", "description": "The name of a node on the network. Network node names include AlarmPanel, ControlPanel, NoticePanel, AlertPanel, CommandCenter."},
          "message": {"type": "string", "description": "The contents of the alert signal message."},
        },
        "required": ["network_node", "message"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "getNickname",
      "description": "Get the nickname of a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
        },
        "required": ["location"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "getMagicNumber",
      "description": "This number is magical.",
      "parameters": {
        "type": "object",
        "properties": {
          "tagname": {"type": "string", "description": "The name of the magic number"},
        },
        "required": ["tagname"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "getSensorValuebyName",
      "description": "Get the value of a sensor by its name. The value is NOTFOUND if the sensor is not available",
      "parameters": {
        "type": "object",
        "properties": {
          "tagname": {"type": "string", "description": "The name of the sensor."},
        },
        "required": ["tagname"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "putSensorValuebyName",
      "description": "Put the value of a sensor into the cache using its name.",
      "parameters": {
        "type": "object",
        "properties": {
          "tagname": {"type": "string", "description": "The name of the sensor."},
          "value": {"type": "string", "description": "The value of the sensor."},
        },
        "required": ["tagname","value"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "sendGridPeakDetected",
      "description": "Send a grid peak detected to a destination network node.",
      "parameters": {
        "type": "object",
        "properties": {
          "network_node": {"type": "string", "description": "The name of a node on the network. Network node names include C2Agent, AlarmPanel, ControlPanel, NoticePanel, AlertPanel, CommandCenter."},
          "message": {"type": "string", "description": "The description of the peak detected."},
          "start_date_time": {"type": "string", "description": "The datetime of the peak detected."},
          "duration_mins": {"type": "string", "description": "The duration in minutes of the peak detected."},
          "peak_lmp": {"type": "string", "description": "The LMP for a megawatt-hour during the peak detected."},
          "grid_node": {"type": "string", "description": "The grid pricing node for the peak detected ."},
          "award_level": {"type": "string", "description": "The award level of the game. Values can be BRONZE, SILVER and GOLD"},
          "game_type": {"type": "string", "description": "The type of game that is being played. The values can be SHEDPOWER or HARVESTPOWER"},
        },
        "required": ["network_node", "message","start_date_time","duration_mins","peak_lmp","grid_node","award_level","game_type"]
      }
    } 
  },{
    "type": "function",
    "function": {
      "name": "getNickname3",
      "description": "Get the nickname of a city",
      "parameters": {
        "type": "object",
        "properties": {
          "location": {"type": "string", "description": "The city and state e.g. San Francisco, CA"},
        },
        "required": ["location"]
      }
    } 
  }]


#-----------------------------------------------------
# Configure logging
agent_log_file = "./logs/make_log.txt"


client = OpenAI()


#-----------------------------------------------------
# Upload files for Retieval Agent
# Must add file ids to create below
#-----------------------------------------------------

# AgentBase = client.files.create(
#    file=open(agent_base_file, "rb"),
#    purpose='assistants'
# )

# AgentData = client.files.create(
#     file=open(agent_data_file, "rb"),
#     purpose='assistants'
# )

#-----------------------------------------------------

# Add instructions to agent
with open(agent_instructions_file, 'r', encoding='utf-8') as instructions_file:
    instructions = instructions_file.read()
print(instructions)

#agent_tool_resources={
#  "code_interpreter": {
#      "file_ids": [file1.id]
#  },
#  "file_search": {
#      "vector_store_ids": [file2.id]
#  }
#}
# Create an assistant
my_assistant = client.beta.assistants.create(
    instructions=instructions,
    name=agent_name,
    model=agent_model,
    tools=agent_tools,
    #tool_resources = agent_tool_resources,
)

print("New Assistant")
print(my_assistant)

print("\nAgent " + agent_name + " created.")
