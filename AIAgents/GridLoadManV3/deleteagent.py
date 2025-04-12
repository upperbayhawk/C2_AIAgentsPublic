# ==============================================================================
# Module: deleteagent.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: Delete an OpenAI Assistant
# Notes: # 
# ==============================================================================

import sys
import logbook

from openai import OpenAI

import config

agent_name = config.agent_name

if len(sys.argv) > 1:
    agent_name = sys.argv[1]
    print(f"Agent Name: {agent_name}")

client = OpenAI()

#print("Listing all assistants")
my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)

print("Assistants")
for item in my_assistants.data:
    print(item)
    substring = agent_name
    # Check if substring exists in text
    if substring in str(item):
        print("Agent found!")
        #my_assistant = item
        response = client.beta.assistants.delete(item.id)
        print(response)
        print("Agent deleted\n")
        break
    else:
        print("Assistant not found.")

print("BYE")


