import os
from scipy.io import wavfile
import pygame, pygame.sndarray
import numpy
import scipy.signal
import time

note_list = []

pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
fs, do_array = wavfile.read('do.wav')
do = pygame.sndarray.make_sound(do_array)
fs, re_array = wavfile.read('re.wav')
re = pygame.sndarray.make_sound(re_array)
fs, mi_array = wavfile.read('mi.wav')
mi = pygame.sndarray.make_sound(mi_array)

note_list.append([do_array,do])
note_list.append([re_array,re])
note_list.append([mi_array,mi])

note_list[0][1].play(0)
record = numpy.zeros(shape = [882000,2], dtype = numpy.int16)
ten_sec_flag = 1 # to extend reacord with 0
record_flag = 0
print ("recording start now!")
print ("input '1' for do, '2' for re, '3' for mi")
print ("input '0' to save recording")
start_time = time.time()

zero_list = numpy.zeros(shape = [220500,2], dtype = numpy.int16)

while True:
    interval = time.time() - start_time
    if interval >= (10*ten_sec_flag):
        record = numpy.vstack((record,zero_list))
        ten_sec_flag+=1;
    s = int(input())
    if s==9:
        record_flag = 1
        print ("start recording...")
        continue
    if s==0:
        print ("saving...")
        zero_num = 0
        i = 1
        while True:
            if (record[len(record)-i] == record[0]).any():
                zero_num+=1
                i+=1
            else:
                break
        record = record[:len(record)-1-zero_num]
        now = time.time()
        now_time = time.strftime("%Y%m%d_%H%M%S")
        path = (now_time+".wav")
        wavfile.write(path, 44100, record)
        record = numpy.zeros(shape = [882000,2], dtype = numpy.int16)
        print("saved!")
        continue
    if (s!=1 and s!=2 and s!=3):
        print ("invalid input!")
        continue
    note_list[s-1][1].play(0)
    if record_flag == 1:
        tick = int(interval*44100)
        print ("recording")
        print (len(record[tick:(tick+len(note_list[s-1][0]))]))
        record[tick:(tick+len(note_list[s-1][0]))] += note_list[s-1][0]






