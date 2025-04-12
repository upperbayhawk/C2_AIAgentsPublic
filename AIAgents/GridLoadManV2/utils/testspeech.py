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
        #os.remove(speech_file_path)
    finally:
        pass
#=============================================


if __name__ == "__main__":
    #speak_message("Our Father who art in heaven, hallowed be thy name. Thy kingdom come, your will be done, on earth as it is in heaven. Give us this day our daily bread, and forgive us our debts, as we also have forgiven our debtors. And lead us not into temptation, but deliver us from evil")
    msg = "Hi Dave. My name is Natasha. I live near you. How are you today? \
        I know it's hard, but why don't you try to come out and play. \
        The weather is beautiful and the sun is shining. \
            We have plenty of time to stroll on the boardwalk and get some thrasher's fries and a piece of Grotto's pizza. \
                "
    
    msg1 = "Our Father, which art in heaven, Hallowed be thy Name. \
        Thy Kingdom come. Thy will be done in earth, As it is in heaven. \
            Give us this day our daily bread. And forgive us our trespasses, \
                As we forgive them that trespass against us. \
                    And lead us not into temptation, But deliver us from evil. \
                        For thine is the kingdom, The power, and the glory, For ever and ever.\
                        Amen"
    #speak_message(msg)
    speak_message(msg1)
