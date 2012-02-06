# -*- coding: utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import os
import threading  
import time  
import urllib2  
import StringIO  
import gzip  
import string  
from Queue import Queue
#导入配置文件
import config
#导入核心库
#import communitor
import urlist
#导入IO库
from judger import Judger
from saver import Saver
from urlist cimport Urlist

'''
Project:	Reptile.py
Function:	核心库，动态下载网页
调用:		

问题:
	关于分站点的问题：
		在爬取进行储存时，便用数据库区分出来（存储到不同表中）
		在judger和saver中进行确定
		原始页面需要保存,将不能够保存的页面抛弃

'''

class reptile(threading.Thread):
    '''
    子线程爬虫具体实现
    '''
    def __init__(self,Gurlist,Rqueue,Name,Flcok,\
            Saver,Judger):
        '''
        init 
        Gurlist:	本平台公共的urlist(自己实现的urlist)
        Name:		线程的名称
        Flcok:		锁
        Rqueue:		运行时共享库
        ---------------------------------------
        Saver:		IO 存储库

        运行方式：
            urlist:         储存所有有效的url（判断一个url是否已经被下载）
            Rqueue:         储存所有有效但是未下载的url
            self.raw_url    储存本网页新得到的href 
                            href均为原生态的url 需要有一些处理之后才能够放入Rqueue
        '''
        threading.Thread.__init__(self,name = Name)
        self.urlist = Gurlist
        #下载页面数
        self.pages = 0
        self.Flcok = Flcok
        self.Rqueue = Rqueue
        self.judger = Judger    #url判断
        self.tem_home_url=''    #局部主地址
        #对每个页面得到的urls进行存储 会在新页面里面进行刷新
        self.raw_url=[]
        #存储库
        self.saver = Saver

    def cg_tem_url_stdurl(self):
        '''
        将临时url（如果是相对url）转化为绝对地址
        同时判断是否为有效url
        此处会返回所有再 home_urls范围内的链接
        如果需要再分配，需要其他函数作处理
        '''
        for i,url in enumerate(self.raw_url):
            '''
            为了能够兼容communitor的功能
            将raw_url中所有url绝对化
            之后进行分类 把部分加入到准备由communitor的公共数据池中
            '''
            #将url转换为 绝对地址

            url = self.judger.url_combine(self.tem_home_url,url)
            self.raw_url[i] = url
            #直接更改raw_url
            #判断是否为收录网站范围内 
            #!!!如果要判断是否为本平台范围内的网页 需要另外进行判断
            #!!!需要和communicator方面的判断
           
            j = self.judger.judge(url)
            if j != -1:
                '''
                是否在需要收录的站点群集中
                '''
                #在收录网站范围内
                #由communicator进行判断 是否加到本网页urlist中 
                #如果为TCP 那么消耗的资源较多 也许不能够及时传递    可以考虑采用 UDP进行传播 但是需要有反馈信息保证稳定
                #TCP适合在大规模内容的时候进行传递
                #-----此处做单平台配置!!!在分布式计算中需要另外配置-------
                #-----DNS查询也需要做相关配置
                if self.judger.judge_this_pc(url):
                    '''
                    是本站点收录的url
                    '''
                    if not self.urlist[self.urlist[-1]].Find(url):
                        self.Rqueue.put(url)
                else:
                    '''
                    其他站点收录的内容
                    存储到各个咱点的urlist池中
                    '''
                    #self.urlist[j].Find(url)
                    #存储到一定的数量，需要与其他平台联系

    def run(self):  
        '''
		下载主程序

        '''
        opener = urllib2.build_opener()     

        while True:  
            print 'queue size:',self.runtime_queue.qsize()
            if self.runtime_queue.qsize()==0:
                print 'the queue is empty break the while'
                #!!!!!!此处应该让线程阻断一段时间
                break
            #从公共queue中取出url 进行下载准备
            url = self.Rqueue.get()          
            
            if url == None:                 
                break
            #中断处理 如果取出一个中断标志 进行中断操作
            #需要重视 模块化 封装
            if url == config.INTERPRET_SIGN:
                '''
                中断操作
                '''
                pass
            
            print 'get from runtime',url
            
            request = urllib2.Request(url) 
            request.add_header('Accept-encoding', 'gzip')

            #局部未处理url存储
            self.raw_url=[]
                
            try:            
                page = opener.open(request,timeout=2) #设置超时为2s
                
                if page.code == 200:      
                    predata = page.read()
                    pdata = StringIO.StringIO(predata)
                    gzipper = gzip.GzipFile(fileobj = pdata)  
                    
                    try:  
                        data = gzipper.read()  
                    except(IOError):  
                        data = predata
                        
                    try:  
                        if len(data)<300:
                            continue
                        #------------------------
                        #------SAVE FILE---------
                        #------IO--SAVE----------
                        #-------SAVE--TEMP--URLS-
                        #------------------------
                        print "saving files" 
                        self.saver.save(data)
                        #saver 应该将源码进行存储，同时对源码进行一定的处理进行储存
                    except:  
                        print 'not a useful page'
                    #获取页面中url 加入到inqueue 和 Urlist中    
                    #------------------------
                    #--将url添加到tem_url中--
                    #------------------------
                    #!!!!!!!!!!!!!!!!!!!!!!!!!
                    for item in self.htmlparser.get_url():
                        if item.find('#')<0:
                            self.raw_url.append(item)
                            #raw_url加入到运行时queue中，和urlist，必须要进行前期加工和判断
                            #此部分再Judger模块中
                            
                    self.pages += 1 

                page.close()  

                if self.pages >= self.max_page_num:
                    return True
                    
            except:  
                print 'end error'  


cdef class Reptile:
    '''
	本平台爬虫系统
	向下管理多线程爬虫  
	水平管理分布式系统 管理数据池
    '''
    def __init__(self):
        '''
        per_max_pages:	每一个线程下载的最大页面数目
        thread_num:		线程数目
        '''
        #相关的共用数据池 
        self.Rqueue = Queue()
        self.thlist = []
        #需要为每个站点设置一个urlist 作为公共数据池
        self.urlist = []
        self.Flock = [] 
        for i in range( self.judger.get_home_num() ):
            '''
            为每一个站点准备一个urlist
            '''
            self.urlist.append( Urlist() )
            #为线程方面同步而使用
            self.Flock.append(threading.RLock())
        #将本站点的url的下标也存储在末尾
        #!!!此处需由communitor分配本平台任务时确定
        self.urlist.append(1)

        self.saver = Saver()
        self.judger = Judger()

    def run(self):
        '''
        运行主程序
        配置多线程运行
        '''
        Flock = threading.RLock()

        for i in range(config.THREAD_NUM):
            #reptile(Gurlist,Rqueue,Name,Flock,Saver)
            th = reptile(self.urlist,config.THREAD_NAME+str(i),Flock,self.saver)
            self.thlist.append(th)
        for th in self.thlist:
            th.start()
        #需要设定 startpage
        startpage="http://www.cau.edu.cn"
        self.Rqueue.put(startpage)

    #--------------------------------------------------
    #--------------------------------------------------
    #开始设定开始的分布式交流的程序
    #在此处添加communitor的和中断的一个线程
            
cdef Reptile rep = Reptile()



