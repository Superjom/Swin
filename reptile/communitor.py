# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2012

@author: chunwei
'''
import socket
import configure
import threading

from pyquery import PyQuery as pq

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
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def initIpList(self):
        '''
        初始化ip列表
        '''
        self.ips = [
            ('127.0.0.1',21567),
        ]
        
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




class Signal:
    '''
    信号相关的处理
    '''
    def __init__(self, ip_list):
        self.transfer = DataTransfer()
        self.transfer.initIpList(ip_list)

    def __parse_new_url(self,signal):
        '''
        读入xml signal
        S_new_url 
        C_new_url
        信号的解析
        最终返回格式:
        {
            home_url: home_url_str,
            urls: [
                    ['title','url'],
                    ['title','url'],
                  ]
        }
        '''
        data = signal('data')
        home_url = data.attr('homeurl')
        urlnodes = signal('url')
        urls = []
        for i in range(len(urlnodes)):
            url = ['','']
            url[0] = urlnodes.eq(i).attr('title')
            url[1] = urlnodes.eq(i).attr('url')
            urls.append(url)
        res = {}
        res.setdefault('home_url',home_url)
        res.setdefault('url',urls)
        return res

    def __parse_sigle_signal(self,signal):
        '''
        单命令的解析 如init halt等
        '''
        return signal('signal').attr('type')

        

    def parseSignal(self,source):
        '''
        利用pyquery对命令xml进行解析
        '''
        signal = pq(source)
        stype = signal('type')
        #对各种不同的命令进行解析
        if stype == 'S_new_url' or stype == 'C_new_url':
            '''
            CentreServ 和 Client 交换新url的命令
            '''
            return self.__parse_new_url(signal)
        else:
            '''
            单命令:
                如 init halt等
            '''
            return self.__parse_sigle_signal(signal)

    def sendSingleSignal_Serv(self,stype):
        '''
        主服务器群发简单信号
        '''
        signal = "<signal type='%s'/>"%stype
        self.transfer.sendData(ALL, signal)

    def sendStatus_Client(self):
        '''
        将本平台信息上传到主平台处理
        '''
        pass

class Server(threading.Thread):
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
                clientsock.send('[%s] %s'% (ctime(),data))
        clientsock.close()


class ClientServ(Server):
    '''
    用于接收主服务器命令
    '''
    def __init__(self, addr):
        Server.__init__(addr)
        self.signal = Signal()

    def getConnection(self,clientsock):
        '''
        重载连接后操作
        '''
        print 'get connection'
        source = clientsock.recv(4096)

    def getConnection(self,clientsock):
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
