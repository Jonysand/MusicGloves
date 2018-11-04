import os
from scipy.io import wavfile
import pygame, pygame.sndarray
import numpy
import scipy.signal

def add_new_sound(List, dir_path):
    note_list = []
    cue_file = open(dir_path+"/"+"cue.txt")
    filenames = cue_file.readlines()
    for filename in open(dir_path+"/"+"cue.txt"):
        filename = filename.strip('\n')
        fs, array = wavfile.read(filename+".wav")
        sound = pygame.sndarray.make_sound(array)
        note_list.append([array,sound])
    List.append(note_list)
    return List


pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
tone_list = []
tone_list = add_new_sound(tone_list, "penta")

while True:
    tone_list[0][0][1].play(0)
    print('do')
    pygame.time.delay(300)
    tone_list[0][1][1].play(0)
    print('re')
    pygame.time.delay(300)
    tone_list[0][2][1].play(0)
    print('mi')
    pygame.time.delay(300)
