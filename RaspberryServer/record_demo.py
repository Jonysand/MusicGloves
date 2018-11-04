#coding=utf-8
import socket
import os
from scipy.io import wavfile
import pygame, pygame.sndarray
import numpy
import scipy.signal
import time
import threading
import re, urllib
from http.server import *
import subprocess
from bypy import ByPy

#-------recording config------------
global record_enable, record_flag, record_jud_flag, record_jud
record_enable = 1 # only when 1 can recording be activate
record_flag = 1 # 1 -> not recording, -1 -> recording
record_jud_flag = 0 # to flag if the timer start to judge whether to start/stop recording
#-----------------------------------

def add_new_sound(List, dir_path):
    note_list = []
    cue_file = open(dir_path+"/"+"cue.txt")
    filenames = cue_file.readlines()
    for filename in open(dir_path+"/"+"cue.txt"):
        filename = filename.strip('\n')
        fs, array = wavfile.read(dir_path+"/"+filename+".wav")
        sound = pygame.sndarray.make_sound(array)
        note_list.append([array,sound])
    List.append(note_list)
    return List
        

def test_ping():
    global ping_test_flag, IP_list, record_flag
    ping_test_flag = 0
    while True:
        if ping_test_flag == 0:
            for gloves in IP_list:
                proc = subprocess.Popen(['ping', gloves[1]],stdout=subprocess.PIPE)
                time.sleep(2)
                proc.kill()
                result = proc.stdout.read().decode()
                if '64 bytes' not in result:
                    noti_disconnected.play(0)
                    print (gloves[1]," disconnected") # send notification to WeApp
                    IP_list.remove(gloves)
                    if IP_list == []:
                        record_flag = 1
        else:
            break

def release_port():
    ret = os.popen("lsof -i:10000")
    all_list = ret.read()
    line_list = all_list.split('\n')
    for i in range(len(line_list)-2):
        each_list = line_list[i+1].split(' ')
        process_num = each_list[2]
        command_line = "kill -9 "+process_num
        os.system(command_line)

global record, ten_sec_flag, start_time
record = numpy.zeros(shape = [882000,2], dtype = numpy.int16)
start_time = 0
ten_sec_flag = 1
def record_start_stop():
    global record_enable, record_flag, record_jud_flag, record_jud, record, start_time, tone_list, tone_flag, ten_sec_flag
    record_jud_flag = 0
    record_flag = (-1) * record_flag
    if record_flag == -1:
        print ("record start!")
        noti_rec_start.play(0)
        record = numpy.zeros(shape = [882000,2], dtype = numpy.int16)
        ten_sec_flag = 1 # to extend reacord with 0
        start_time = time.time()
        record_jud.cancel()
    elif record_flag == 1:
        noti_rec_stop.play(0)
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
        now_time = time.strftime("%Y-%m-%d_%H:%M:%S")
        path = (now_time+".wav")
        wavfile.write(path, 44100, record)
        print ("local saved!")

        proc = subprocess.Popen(['ping','www.baidu.com'],stdout=subprocess.PIPE)
        time.sleep(2)
        proc.kill()
        result = proc.stdout.read().decode()
        if '64 bytes' in result:
            bp = ByPy()
            bp.mkdir(remotepath='music')
            bp.upload(localpath=path, remotepath='music',ondup='newcopy')
            print ("uploaded!")
        else:
            print ("network disconnected!")

    record_jud.cancel()
    record = numpy.zeros(shape = [882000,2], dtype = numpy.int16)
    
def acpt_proc():
    while True:
        new_sock, new_addr = server.accept()
        print ("new glove connected!")
        t = threading.Thread(target=receive_data,args=(new_sock, new_addr))
        t.start()

global interval
def receive_data(sock, addr):
    global record_enable, record_flag, record_jud_flag, record_jud, start_time, record, ten_sec_flag
    
    while True:
        data = sock.recv(1024)
        mes_type = data.decode()[0]
        #------mes of getting IP from gloves-----
        if mes_type == '0':
            noti_connected.play(0)
            glove = data.decode()[1]
            ip = addr[0]
            IP_list.append([glove, ip])
        #--------------------------------
        
        #------mes of playing------------
        if mes_type == '1':
            glove = int(data.decode()[1])
            hand = data.decode()[2]
            note = data.decode()[3:8]
            press_index = 0
        
            if hand == '1': # right hand
                if record_jud_flag == 1: #receive aother right hand mes, stop record judge
                    record_jud.cancel()
                    record_jud_flag = 0
                if note == "01000" and record_enable == 1: #start counting till 5s, then record start/stop
                    record_jud_flag = 1
                    record_jud = threading.Timer(5, record_start_stop)
                    record_jud.daemon = True
                    record_jud.start()
                for press in note:
                    if press == '1':
                        tone_list[tone_flag[glove]][press_index+2][1].play()
                        if record_flag == -1:
                            # recording this note
                            interval = time.time() - start_time
                            tick = int(interval*44100)
                            record[tick:(tick+len(tone_list[tone_flag[glove]][press_index+2][0]))] += tone_list[tone_flag[glove]][press_index+2][0]
                    press_index+=1
                
            elif hand == '0': # left hand
                for press in note:
                    if press == '1':
                        tone_list[tone_flag[glove]][3-press_index][1].play()
                        if record_flag == -1:
                            # recording this note
                            interval = time.time() - start_time
                            tick = int(interval*44100)
                            record[tick:(tick+len(tone_list[tone_flag[glove]][3-press_index][0]))] += tone_list[tone_flag[glove]][3-press_index][0]
                    press_index+=1
        #------------------------------
        #print (addr)
        #print (data.decode())

#--------server information---------
# get local device name
myname = socket.getfqdn(socket.gethostname())
# get this ip address
myaddr = socket.gethostbyname(myname)
print ("NAME: ",myname)
print ("IP: ",myaddr)
print ("")
#------------------------------------

#--------server main-----------------
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
release_port()

server.bind(('192.168.1.101', 10000))
server.listen(1)

    #--------load wav file--------------
global tone_list, tone_flag
tone_list = [] #to store different tones, use tone_flag to rep different tones
tone_flag = [] # 0:guitar_chor, 1:piano_chor, 2:piano_note
for i in range(10):
    tone_flag.append(0)
pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)

fs, noti_connected_array = wavfile.read("connected.wav")
noti_connected = pygame.sndarray.make_sound(noti_connected_array)
fs, noti_disconnected_array = wavfile.read("disconnected.wav")
noti_disconnected = pygame.sndarray.make_sound(noti_disconnected_array)
fs, rec_start_array = wavfile.read("record_start.wav")
noti_rec_start = pygame.sndarray.make_sound(rec_start_array)
fs, rec_stop_array = wavfile.read("record_stop.wav")
noti_rec_stop = pygame.sndarray.make_sound(rec_stop_array)

tone_list = add_new_sound(tone_list, "star")
    #-----------------------------------


print("Start!")
tone_list[0][0][1].play(0)

# left hand setting
left_offset = [] # only get multiple of 5, initially 0
for i in range(10):
    left_offset.append(0)

global IP_list
IP_list = [] # to save IP addrs from gloves

ping_threat = threading.Thread(target = test_ping, name="Ping_Test")
ping_threat.start()

acpt = threading.Thread(target=acpt_proc, name = "ACCEPTING")
acpt.start()

zero_list = numpy.zeros(shape = [220500,2], dtype = numpy.int16)
ten_sec_flag = 1
try:
    while True:
        # if recording, following code used to extend record array
        if record_flag == -1:
            interval = time.time() - start_time
            if interval >= (5*ten_sec_flag):
                record = numpy.vstack((record,zero_list))
                ten_sec_flag+=1;
        
finally:
    print ("server closing")
    ping_test_flag = 1
    ping_threat.join(timeout=0)
    server.close()
#------------------------------------



