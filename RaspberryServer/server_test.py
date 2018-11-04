import socket
import os
from scipy.io import wavfile
import pygame, pygame.sndarray
import numpy
import scipy.signal
import time
import threading
import re, urllib
from http.server import * # HTTPServer,BaseHTTPRequestHandler

def release_port():
    ret = os.popen("lsof -i:10000")
    all_list = ret.read()
    line_list = all_list.split('\n')
    for i in range(len(line_list)-2):
        each_list = line_list[i+1].split(' ')
        process_num = each_list[2]
        command_line = "kill -9 "+process_num
        os.system(command_line)

def receive_data(sock, addr):
    while True:
        data = sock.recv(1024)
        print (addr)
        print (data.decode())

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
server.listen(4)

##    #----------http server--------------
##class httpServer(BaseHTTPRequestHandler):
##    #小程序端使用的http方法为GET方法 这里就是处理过来的GET请求
##    def do_GET(self):
##        templateStr='Failed!'
##        #这里的self.path就是小程序端发来的数据 是一个字符串类型
##        getData=self.path
##        print ('URL=',getData)
##
##        glove = 0
##        
##        #下面是对收到的请求进行解析 我觉得可以在每个if下添加脚本调用的操作
##        if(re.search('Solo',getData)!=None):
##            templateStr='Now:Solo!'
##        if(re.search('Duet',getData)!=None):
##            templateStr='Now:Duet!'
##        if (re.search('Piano', getData) != None):
##            templateStr = 'Now:Piano!'
##        if (re.search('Guitar', getData) != None):
##            templateStr = 'Now:Guitar!'
##        if (re.search('Midi', getData) != None):
##            templateStr = 'Now:Midi!'
##        #下面是设置返回给小程序的报文格式和内容
##        self.protocol_version='HTTP/1.1'
##        self.send_response(200)
##        self.send_header("Welcome","Contect")
##        self.end_headers()
##        self.wfile.write(templateStr)
##
###这个就是开启http服务的函数
##def start_server(port):
##        http_server=HTTPServer(('',int(port)),httpServer)
##        http_server.serve_forever()
###使用2500端口 开启服务
##start_server(2500)
##    #------------------------------------


print("Start!")

try:
    while True:
        new_sock, new_addr = server.accept()
        t = threading.Thread(target=receive_data,args=(new_sock, new_addr))
        t.start()
finally:
    print ("server closing")
    server.close()
#------------------------------------



