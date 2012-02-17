# -*- coding: utf-8 -*-
'''
Created on Feb 13, 2012

@author: chunwei
'''
from signal import Signal
import socket
import configure
import threading  

class CentreServ:
    '''
    中央控制服务器
    控制其他子平台运行
    爬取时以顺序进行 不同站点 顺序进行 每次分配子平台
    一个站点的爬取任务
    '''
    def __init__(self):
        self.sg = Signal()
        self.__initServer()
    
    def __initServer(self):
        '''
        run server
        初始化服务器  接受其他平台询问及服务
        '''
        self.tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpSerSock.bind(config.ADDR)
        self.tcpSerSock.listen(5)
        
    def serverRun(self):
        '''
        本地TCP服务程序
        一般服务程序需要有一个线程 一直等待进行连接
        需要在启动时便开始运行
        当有连接时，传送一个__single_server进行服务
        相关信息:
            ask_for_urls        子平台要求新的链接任务
        '''
        print 'waiting for connection...'
        clientsock,addr = self.tcpSerSock.accept()
        print '...connected from:',addr
        t = threading.Thread(target = self.parseSignal, args=[clientsock])
        t.setDaemon(True)
        t.start()

    def getConnection(self, clientsock):
        '''
        基础的字符串型信号传递
        '''
        print "New Child", threading.current_thread().getName()
        print "Got connection from ",clientsock.getpeername()
        data = clientsock.recv(4096)
        if not len(data):
            print 'received empty data'
            print 'server threading is going to end'
            return
        head = self.sg.getSignal(data)
        
        if head == config.SIGN['send_other_pc_url']:
            '''
            为其他站点传递url
            '''
            print 'send other pc url'
