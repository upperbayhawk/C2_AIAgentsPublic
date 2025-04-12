# runsink.py

# Copyright (C) Upperbay Systems, LLC - All Rights Reserved
# Unauthorized copying of this file, via any medium is strictly prohibited
# Proprietary and confidential
# Written by Dave Hardin <dave@upperbay.com>, 2023

import os
import sys
import asyncio
import queue
import threading
import logbook

import time
import datetime
import arrow

from pathlib import Path
import openai
# speech
import pygame

clientAI = openai.OpenAI()

#=============================================
# voices = alloy,echo,fable,onyx,nova,shimmer
def speak_message(message):
    try:
        speech_file_path = "data/testspeech.mp3"
        response = clientAI.audio.speech.create(
        model="tts-1-hd",
        voice="nova",
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


if __name__ == "__main__":
    speak_message("My name is Natasha. Alexa, turn off hall.")
