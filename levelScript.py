import aubio
import math
import numpy as np
import pyaudio
import random
import tkinter as tk
import time
from cmu_112_graphics import *

# button,start_time,end_time

buttons = ['left', 'right', 'up', 'down']

firstNote = 5
lastNote = 55

notes = 80
song = []

for i in range(notes):
    button = random.choice(buttons)
    startTime = str(firstNote + i * (lastNote - firstNote) / notes)
    endTime = ""
    song.append((button, startTime, endTime))

def writeSongToFile(song, filename):
    stringNotes = [f'{button},{startTime},{endTime}' for (button, startTime, endTime) in song]
    text = "\n".join(stringNotes)
    f = open(filename, "w")
    f.write(text)
    f.close()

writeSongToFile(song, "levels/level3.txt")
for i in range(100):
    writeSongToFile(song, f'levels/nonsense{i}.txt')