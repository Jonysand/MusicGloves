#coding=utf-8
import os
import re
import urllib
from BaseHTTPServer import HTTPServer,BaseHTTPRequestHandler

class httpServer(BaseHTTPRequestHandler):
    #小程序端使用的http方法为GET方法 这里就是处理过来的GET请求
    def do_GET(self):
        templateStr='Failed!'
        #这里的self.path就是小程序端发来的数据 是一个字符串类型
        getData=self.path
        print 'URL=',getData
        #下面是对收到的请求进行解析 我觉得可以在每个if下添加脚本调用的操作
        if(re.search('Solo',getData)!=None):
            templateStr='Now:Solo!'
        if(re.search('Duet',getData)!=None):
            templateStr='Now:Duet!'
        if (re.search('Piano', getData) != None):
            templateStr = 'Now:Piano!'
        if (re.search('Guitar', getData) != None):
            templateStr = 'Now:Guitar!'
        if (re.search('Midi', getData) != None):
            templateStr = 'Now:Midi!'
        if (re.search('1', getData) != None):
            templateStr = 'Now:Glove1!'
        if (re.search('2', getData) != None):
            templateStr = 'Now:Glove2!'
        if (re.search('3', getData) != None):
            templateStr = 'Now:Glove3!'
        #下面是设置返回给小程序的报文格式和内容
        self.protocol_version='HTTP/1.1'
        self.send_response(200)
        self.send_header("Welcome","Contect")
        self.end_headers()
        self.wfile.write(templateStr)

#这个就是开启http服务的函数
def start_server(port):
        http_server=HTTPServer(('',int(port)),httpServer)
        http_server.serve_forever()
#使用2500端口 开启服务
start_server(2500)
