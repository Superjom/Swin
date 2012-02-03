'''
分布式的交流库
    init:
        初始化的时候 设置一个主PC 将数据库文件进行分发 
        进行任务分配 将相关分配信息进行分发
        运行过程中：
            将相关的urlist到一定的量后，传输到相应的PC

        中断时，做相应的处理
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
考虑是否有必要将这个大类分成小类
'''
from socket import *
from time import ctime
import threading
import sys
sys.path.append('../')

import config


cdef class Communitor(threading.Thread):
    '''
    分布式的管理程序
    '''
    def __cinit__(self,judger,Rqueue,urlist):
        '''
        init
        judger: judger库
        所有交流的信息中 均需要结构化
        如 在前面加上前缀 以标识是那一个程序进行处理

        '''
        #自己的服务器地址为固定
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(config.ADDR)
        self.tcpSerSock.listen(5)
        
        self.judger = judger
        #本平台共用Rqueue
        self.Rqueue = Rqueue
        #本平台共用urlist
        #为各个站点准备了一个urlist
        self.urlist = urlist
        #各个平台的ip地址信息
        #!!!需要动态生成或人工配置
        #结构： [(HOST,PORT),(HOST,PORT)]
        self.site_ip_info =[]

    def __rcv_url(self,urls):
        '''
        处理接受其他平台发送过来的urls
        发送过来的urls通常连接为str 需要解码
        此类url均为句对url 
        '''
        print 'received urls from other PC'
        #直接对本平台的urls进行处理
        return urls.split(config.URLS_SPLIT_SG)

    def __add_head_sign(self,head,data):
        '''
        添加标志
        在TCP传输中标志相关的头部
        '''
        if config.SIGN.has_key(head):
            '''  
            如果有key
            '''  
            return config.SIGN[head]+data
        return False

    def __get_head_sign(self,data):
        '''
        接收到信息，返回头部的特定标志
        '''
        print '!>received head'
        print data[:config.SIGN_LEN ]
        return data[:config.SIGN_LEN ]
        

    def rcv_urls(self,urls):
        '''
        接受模块
        urls: 传输过来的url经过切割的字符串
        将其他PC传输过来的urls添加到平台urls
        需要使用Judger进行完整的url处理
        '''
        for url in self.__rcv_url():
            '''
            对每个url进行处理
            每个url肯定都是绝对url
            '''
            if self.judger.judge(url) != -1:
                '''
                judge 不符合 return -1
                    符合 返回站点下标
                '''
                if not self.urlist[self.urlist[-1]].Find(url):
                    '''
                    添加到本平台url库中
                    等待被爬虫处理
                    '''
                    self.Rqueue.put(url)

    def __connect_site_send_data(self,siteID,data):
        '''
        负责连接站点的所有工作
        并将一定信息传输出去
        '''
        #TCP连接相关的配置
        tcpCliSock = socket( AF_INET, SOCK_STREAM )
        #!!!此处地址需要动态生成
        try:
            if not tcpCliSock.connect(self.site_ip_info[siteID):
                '''
                连接到 siteID 所指向的平台
                '''
                print 'Error,can not connet to [%s %s]'%self.site_ip_info[siteID]
            if not tcpCliSock.send(data):
                print 'Error,can not send data'
            tcpCliSock.close()
        except:
            print 'Error,can not connect or  send data'


    def __send_url(self,siteID):
        '''
        需要得到siteID与地址的对应关系
        负责向特定站点siteID发送url
        完整的从转化到结束
        '''
        #取得本平台积累的相应平台的urls的字符串
        #并将之清空
        #再发送出去
        char *strr = self.urlist[siteID].get_urls_str()
        #添加头部发送出去
        return self.__connect_site_send_data(siteID,\
                self.__add_head_sign('add_url',data) ) 

    def Send_other_pc_url(self):
        '''
        判别本平台中公共池是否已经满
        如果满了开始向其他机器传送url
        '''
        for i in range(len(self.urlist)-1):
            '''
            对每个urlist进行扫描
            '''
            if i not self.urlist[-1] :
                '''
                非本平台的其他平台公共池
                进行扫描
                '''
                if self.urlist[i].get_list_length() >= config.OTHER_URL_NUM:
                    '''
                    其他url数据池达到一定的数量 开始传输
                    '''
                    #最好做一些回值判断
                    self.__send_url(i) 

    #----------------下面关于本地TCP服务程序的一些设置------------------
    def server(self):
        '''
        本地TCP服务程序
        一般服务程序需要有一个线程 一直等待进行连接
        需要在启动时便开始运行
        当有连接时，传送一个__single_server进行服务
        '''
        print 'waiting for connection...'
        clientsock,addr = self.tcpSerSock.accept()
        print '...connected from:',addr
        t = threading.Thread(target = self.__sigle_server,args=[clientsock])
        t.setDaemon(True)
        t.start()
        #服务性程序停止
        #tcpSerSock.close()


    def __single_server(self,clientsock):
        '''
        单个服务程序
        将对收到的信息进行解析 并做相应的操作
        '''
        print 'New Child',threading.currentThread().getName()
        print 'Got connection from',clientsock.getpeername()
        data = clientsock.recv(4096)
        if not len(data):
            print 'received empty data'
            print 'sever threading is going to end'
            head = self.__get_head_sign(data)
            
            if head == config.SIGN['init']:
                '''
                分布式初始化程序
                本平台作为被动平台 另外有一个平台作为主平台
                '''
                pass

            elif head == config.SIGN['add_url']:
                '''
                其他站点发来url 需要在本地进行处理
                '''
                self.rcv_urls(data[2:])

            #clientsock.sendall('--------%s'%data)
        clientsock.close()
        print 'clientsock is closed'
        
    
    

'''
def handlechild(clientsock):
    print 'New Child',threading.currentThread().getName()
    print 'Got connection from',clientsock.getpeername()
    while True:
        data = clientsock.recv(4096)
        if not len(data):
            print 'received empty data'
            print 'sever threading is going to end'
            break
        clientsock.sendall('--------%s'%data)
    clientsock.close()
    print 'clientsock is closed'
    print 'return False'
    return False

while True:
    print 'waiting for connection...'
    clientsock,addr = tcpSerSock.accept()
    print '...connected from:',addr
    t = threading.Thread(target = handlechild,args=[clientsock])
    t.setDaemon(True)
    t.start()
    tcpSerSock.close()

'''










