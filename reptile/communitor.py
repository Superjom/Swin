# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2012

@author: chunwei
'''
import socket
import configure
import threading
from pyquery import PyQuery as pq
#--------------------------------------------------------------------
from List import UrlQueue

ALL = -1    #CentreServ向其他所有平台群发命令
SERV = 0    #CentreServ 的 id

class DataTransfer:
    '''
    关于信号传递
    向其他平台传递信息的操作
    '''
    
    def __init__(self):
        '''
        初始化 需要取得其他平台的ip
        '''
        pass

    def initIpList(self, ips = [('127.0.0.1',21567)]):
        '''
        初始化ip列表
        '''
        self.ips = ips
        
    def sendData(self, sid, data):
        '''
        向其他平台传递data
        由id对各平台进行区分
        '''
        if sid == ALL:
            for serv in self.ips:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.connect(serv)
                sock.sendall(data)
                sock.close()
            return
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(self.ips[sid])
        sock.sendall(data)
        sock.close()

from socket import *
HOST = ''
PORT = 21569
BUFSIZ = 1024
ADDR = (HOST,PORT)

class Server:
    def __init__(self, _continue):
        '''
        continue is a list which will send signal to server
        whether it continue to run
        '''
        self._continue = _continue
        Name="chun"
        threading.Thread.__init__(self, name = Name )  
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(ADDR)
        self.tcpSerSock.listen(5)
        self.num = 0

    def run(self):
        print 'serv'
        while True:
            print 'waiting for connection...'
            tcpCliSock,addr = self.tcpSerSock.accept()
            print '...connected from:',addr

            print 'start a new thread'
            #start new thread to serve client
            t = threading.Thread(target = self.getConnection, args=[tcpCliSock])
            t.setDaemon(True)
            t.start()
            print 'thread is ended'
            if self.num == 3 or self._continue[0] == False:
                print 'self.num ',self.num
                print 'it is going to end the server program'
                break
        self.tcpSerSock.close()

    def getConnection(self, clientsock):
        self.num += 1 
        while True:
            data = clientsock.recv(4096)
            if not len(data):
                print 'received empty data'
                print 'thread is to end'
                break
            else:
                print data
                #clientsock.send('[%s] %s'% (ctime(),data))
        clientsock.close()

class CentreServ:
    '''
    主服务器控制程序
    将以主程序方式运行于控制服务器 
    设立一个单独线程用于GUI的显示和控制
    '''
    def __init__(self):
        Server.__init__()
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(ADDR)
        self.tcpSerSock.listen(5)
        self.num = 0
        #继续运行信号
        self.running = True
        self.signal = Signal()

    def init(self):
        '''
        取得初始的home_lists    进行爬取
        得到各client的ip列表
        '''
        #取得home_lists
        #取得urlists
        self.home_list = [
            "http://www.cau.edu.cn",
            "http://www.sina.com.cn",
            ]
        #新建本地url存储队列
        #为每一个home_url建立一个队列存储收到的新链接 
        #由 UrlQueue统一管理
        self.queue = UrlQueue(self.home_list)
        #!!!!!!!!!!!!!!!!此处需要动态配置
        self.clientIPs = [
            ('127.0.0.1', 80),
        ]

    def run(self):
        while True:
            if not self.running:
                '''
                停止运行
                '''
                break
            print 'waiting for connection...'
            tcpCliSock,addr = self.tcpSerSock.accept()
            print '...connected from:',addr

            print 'start a new thread'
            #start new thread to serve client
            t = threading.Thread(target = self.getConnection, args=[tcpCliSock])
            t.setDaemon(True)
            t.start()
            print 'thread is ended'
        self.tcpSerSock.close()

    def parseSignal(self, signal):
        '''
        signal 解析
        '''
        d = pq(signal)
        _type = d('signal').attr('type')

    def __get_urls_from_queues(self):
        '''
        从本平台数据中提取一定量的url
        返回格式：
        {
            siteID: id
            urls:   [
                        [title, path],
                        [title, path],
                        [title, path],
                    ]
        }
        '''
        return self.queue.getUrlList(100)
    
    def __get_urls_from_client(self, data):
        '''
        receive urls from a client
         
        '''
        signal = pq(data)
        li = signal(url)
        urls = []
        for i in range(len(li)):
            url = []
            u = li.eq(i)
            url.append(u.attr('siteID'))
            url.append(u.attr('title'))
            url.append(u.attr('path'))
            urls.append(url)

    def __get_status(self, data):
        '''
        从客户端取得status信号
        '''
        signal = pq(data)
        res = {}
        res['pages_num'] = signal.attr('pages_num')
        res['urlist_num'] = signal.attr('urlist_num')
        res['queue_num'] = signal.attr('queue_num')
        return res
        
    #---------------------------------------------
    def __send_init(self, clientsock):
        '''
        向客户端发送init信号 
        '''
        signal = "<signal type='init'/>"
        clientsock.send(signal)

    def __send_halt(self, clientsock):
        '''
        向客户端发送halt信号 
        '''
        signal = "<signal type='halt'/>"
        clientsock.send(signal)

    def __send_stop(self, clientsock):
        '''
        向客户端发送stop信号 
        '''
        signal = "<signal type='stop'/>"
        clientsock.send(signal)

    def __send_resume(self, clientsock):
        '''
        向客户端发送resume信号 
        '''
        signal = "<signal type='resume'/>"
        clientsock.send(signal)

    def __send_urltask(self, clientsock):
        '''
        send more urltask to this client
        '''
        #pop urls from queue
        urldoc = self.__get_urls_from_queues()
        siteID = urldoc['siteID']
        urls = urldoc['urls']
        signal = pq('<signal></signal>')
        signal('signal').attr('type', 'urltask')
        signal('siteID').attr('siteID', siteID)
        for url in urls:
            u = pq('<url/>')
            u.attr('title', url[0])
            u.attr('path', url[1])
            signal.append(u)
        clientsock.send(signal)

#------------------------------------------------------

    def frame(self):
        '''
        显示图形界面
        '''
        pass

    def getConnection(self, clientsock):
        self.num += 1 
        while True:
            data = clientsock.recv(4096)
            if not len(data):
                print 'received empty data'
                print 'thread is to end'
                break
            else:
                print data

                #clientsock.send('[%s] %s'% (ctime(),data))
        clientsock.close()


class ReptileClientServ:
    '''
    客户端主程序
    负责除了爬取网页之外的所有管理工作
    与主服务器交流
    '''
    def __init__(self):
        self.url_list = None
        self.url_queue = None
        self.url_in_queue = None

    def init(self, addr):
        '''
        开启端口
        '''
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(addr)
        self.tcpSerSock.listen(5)

    def __get__init_signal(self, data_homelist):
        '''
        开始init
        建立 queue
             UrlQueue
             inqueue
        '''

        self.url_list = Urlist()


    def getConnection(self, clientsock):
        '''
        重载连接后操作
        '''
        print 'get connection'
        source = clientsock.recv(4096)

        if not len(source):
            print 'receiversignal'
        signal = self.signal.parseSignal(source)

        if signal['type'] == 'init':
            '''
            初始化操作
            '''
            self.__signal_Init()
        elif signal['type'] == 'status':
            '''
            被询问状态
            '''
            self.__signal_Status()
        elif signal['type'] == 'halt':
            '''
            中断操作
            '''
            self.__signal_Halt()
        elif signal['type'] == 'S_new_url':
            '''
            CentreServ传送过来新的url任务
            '''
            self.__signal_S_New_Url()
        elif signal['type'] == 'stop':
            '''
            终止系统操作
            '''
            self.__signal_Stop()
        elif signal['type'] == 'resume':
            '''
            中断恢复操作
            '''
            self.__signal_Resume()


if __name__ == "__main__":
    '''
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind("",8881)
    sock.listen(5)
    '''
