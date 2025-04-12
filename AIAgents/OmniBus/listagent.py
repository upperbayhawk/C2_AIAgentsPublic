# ==============================================================================
# Module: listagent.py
# Author: Dave Hardin, Upperbay Systems LLC
# Author URL: https://upperbay.com
# License: MIT
# Date: 1/2024
# Description: List all OpenAI Assistants
# Notes:
# ==============================================================================

from openai import OpenAI

client = OpenAI()

my_assistants = client.beta.assistants.list(
    order="desc",
    limit="20",
)

print("All Assistants")

for agent in my_assistants:
    print("Assistant: " + str(agent) + "\n")