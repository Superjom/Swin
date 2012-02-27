# -*- coding: utf-8 -*-

######################## BEGIN LICENSE BLOCK ########################
# The Initial Developer of the Original Code is
# Chunwei from China Agricual University
# Portions created by the Initial Developer are Copyright (C) 2012
# the Initial Developer. All Rights Reserved.
#
# Contributor(s):
# Chunwei  Mail: superjom@gmail.com
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA
# 02110-1301 USA
######################### END LICENSE BLOCK #########################
'''
Created on Feb 12, 2012

@author: chunwei
'''
#-------------------------------------------------------------
import os
import threading  
import time  
import StringIO  
import string  
import chardet
import httplib
import datetime as datetime
import urlparse
#-------------------------------------------------------------
from judger import Judger
from debug import *
from List import Urlist
from List import UrlQueue
from List import Queue

from sourceparser import HtmlParser
from sourceparser import PicParser
from sourceparser import Collector

from iofile import DBSource
#-------------------------------------------------------------

'''
新特性：
    从urlib2 更替为 httplib 一次分配一个站点的爬取任务 重复利用DNS缓存
'''
class Reptile(threading.Thread):
    '''
    单个线程
    '''
    @dec
    def __init__(self, name, url_queue, url_list, url_in_queue, Flock, home_urls ,tem_siteID = [0]):
        '''
        name
        url_queue       从主服务器中分配到的url
        url_list        本地区分是否重复
        url_in_queue    解析得到的新url    将为每一个站点分配一个 UrlQueue
        Flock
        home_urls       测试是否符合爬取集合
        tem_conn        初始的DNS 缓存
        is_new_task     通过引用传递 由communitor修改  以判断是否需要修改
        tem_home_url    
        old_home_url    引用传递
        '''
        threading.Thread.__init__(self, name = name )  
        #本地测试url队列 如果在本地重复 则直接舍弃
        #如果不重复 加入临时队列 将来传输到中央服务器进行测试
        #为每个站点分配了一个list对象 分开进行url的分辨
        self.__url_list = url_list
        self.__url_queue = url_queue
        #默认为每一个站点分配一个inqueue
        #本地临时记录队列 在url_list中测试不重复后 加入in_queue
        #在积累到一定量后 传输给中央服务器管理
        #Queue()
        self.__url_in_queue = url_in_queue
        #----------------------------------------------------------------
        self.__Flock = Flock
        self.__home_urls = home_urls
        #强制刷新 DNS
        self.__tem_siteID = None
        #引用传递 方便进行对照
        self.__tem_siteID = tem_siteID
        #----------------------------------------------------------------
        self.__Flock = Flock
        self.__htmlparser = HtmlParser()
        self.__picparser = PicParser()
        self.__judger = Judger(self.__home_urls)
        #init temporary home_url and siteID
        #both to determine weather to refresh DNS cache
        self.__dbsource = DBSource()
        self.__collector = Collector(home_urls)
    #------------------------------------------------------
    @dec
    def init(self, siteID):
        console('self.init()')
        self.siteID = -1
        self.__tem_siteID[0] = siteID
        self.__dbsource.init(siteID)
        self.__url_queue.init(siteID)
        netloc = self.transNetloc(self.__home_urls[siteID])
        print 'get netloc',netloc
        self.__conn = httplib.HTTPConnection(netloc, 80, timeout = 10)
    @dec 
    def conn(self):
        '''
        包含刷新DNS功能
        siteID引用传入  检测DNS改变
        '''
        if self.siteID != self.__tem_siteID[0]:
            '''
            更新DNS
            '''
            self.siteID = self.__tem_siteID[0]
            #netloc = (urlparse.urlsplit(self.__home_urls[self.__tem_siteID[0]])).netloc
            netloc = self.transNetloc(self.__home_urls[self.__tem_siteID[0]])
            print 'netloc',netloc
            self.__conn = httplib.HTTPConnection(netloc, 80, timeout = 10)
        return self.__conn
    
    def transcode(self, source):
        '''
        转码 自动转化为utf8
        '''
        res = chardet.detect(source)
        confidence = res['confidence']
        encoding = res['encoding']
        print 'transcode', res
        if confidence < 0.6:
            return False
        else:
            return unicode(source, encoding)
    @dec
    def transPath(self, page_url, path):
        '''
        将任意一个链接转化为 路径
        '''
        url = self.__judger.transToStdUrl(page_url, path)
        return urlparse.urlsplit(url).path
    @dec
    def transNetloc(self, url):
        '''
        传入绝对url  
        '''
        return urlparse.urlsplit(url).netloc
    #-------------------------------------------------------------
    @dec       
    def run(self):
        '''
        运行主程序
        '''
        console('self.run()')
        self.conn()
        home_url = self.__home_urls[self.siteID]
        print 'home_url',home_url
        while(True):
            #[title, path]
            urlinfo = self.getAUrl()
            print 'get urlinfo ',urlinfo
            if not urlinfo:
                print "No Task\nqueue is empty!"
                return
            #全局 页面信息
            page_path = urlinfo[1]
            page_url = self.__judger.transToStdUrl(home_url, page_path)
            print 'page_path',page_path
            source = self.getPage(home_url, page_path)
            print 'get source',source
            #判断是否为html源码
            if not self.__htmlparser.init(source):
                '''
                图片和其他文件单独处理
                此处不作解析
                '''
                continue
            #取得绝对地址
            #url = self.__judger.transToStdUrl(home_url, page_path)
            #url统一存储为绝对地址
            #save html source
            self.saveHtml(page_url, urlinfo[0])
            imgsrcs = self.getImgSrcs()
            #save images
            self.saveImgList(page_url, imgsrcs)
            newurls = self.__htmlparser.getALinkText_List()
            self.addNewInQueue(page_url, newurls)
    @dec 
    def requestSource(self, path):
        '''
        page_url    子页面 如 ./index.html
        url: 直接传入绝对url 包括home_url
        内部进行解析
        '''
        conn = self.conn()
        conn.request("GET", path)
        #print self.__conn
        r1 = conn.getresponse()
        #print r1
        print r1.status
        data = r1.read()
        '''
        if r1.status != 'OK':
            print 'status is ',r1.status
            print 'status not OK'
            print r1.reason
            return False
        data = r1.read()
        if not len(data):
            print 'length of data is 0'
            return False
        '''
        return data
    @dec 
    def getPage(self,page_url, url):
        '''
        任意传入url
        将自动转化为path 然后调用底层 requestSource()
        '''
        console('self.getPage()')
        path = self.transPath(page_url, url)
        data = self.requestSource(path)
        print 'page_url: url',page_url, url
        if len(data):
            data = self.transcode(data)
            print 'data',data
            if not len(data):
                return False
            if not self.__collector.init(data):
                print 'collector.init',
                return False
            #self.__htmlparser.init(data)
            self.__htmlparser = self.__collector.htmlparser
        return data
    @dec    
    def getImg(self,page_url, url):
        '''
        path
        img_path    './img/1.jpg'
        返回 [绝对url, source]
        '''
        url = self.transPath(page_url, url)
        return [url, self.requestSource(url)]
    @dec    
    def getAUrl(self):
        return self.__url_queue.get(timeout = 3)
    @dec 
    def getUrls(self):
        '''
        取得urls
        并且进行判断 
        '''
        return self.__htmlparser.getALink_list()
    @dec 
    def getImgSrcs(self):
        '''
        parse html source and return src_list
        '''
        return self.__htmlparser.getPicSrcs_List()
    @dec
    def addNewQueue(self, path_list):
        '''
        外界： 控制服务器传来的新的paths
        url_list = [
            ['cau','path'],
        ]
        '''
        #控制刷新
        for url in path_list:
            self.__url_queue.put(url)
    @dec    
    def addNewInQueue(self, page_url, url_list):
        '''
        url直接为原始的url   不需要另外进行处理
        将new_url添加到对应的queue中
        '''
        for urlinfo in url_list:
            #处理为绝对url
            url = self.__judger.transToStdUrl(page_url, urlinfo[1])
            siteID = self.__judger.judgeUrl(page_url, url)
            path = urlparse.urlsplit(url).path
            #判断是否为本平台url
            if siteID != -1:
                if not self.__url_list.find(siteID, path):
                    '''
                    not duplicate in url_list
                    '''
                    #将url减少
                    self.__url_in_queue.put(siteID, urlinfo[0], path)
        self.__url_in_queue.show()
    @dec
    def saveHtml(self, url, title):
        '''
        存储 source 和 parsedsource to database
        '''
        #得到绝对url
        assert self.siteID != -1
        #url = self.__judger.transToStdUrl(self.__home_urls[self.siteID], path)
        today = datetime.date.today()
        info = {
            'title' :   title,
            'url':      url,
            'date':     datetime.date.isoformat(today)
        }
        self.__dbsource.saveHtml(info, self.__collector.html, self.__collector.transXml_Str(url))

    def saveImg(self, url, source):
        imgsource = self.__picparser.getCompressedPic()
        size = imgsource['size']
        source = imgsource['source']
        print 'source',source
        info = {
            'url':url,
            'width':size[0],
            'height':size[1]
        }
        self.__dbsource.saveImg(info, source)

    def saveImgList(self, page_url, srcs):
        '''
        传入绝对src
        传入 srcs 系列存储
        '''
        for src in srcs:
            imgsource = self.getImg(page_url, src)
            url = imgsource[0]
            source = imgsource[1]
            self.__picparser.init(source)
            self.saveImg(url, imgsource)

class ReptileLib:
    '''
    线程库
    负责爬取任务
    对 halt 和 resume 提供接口
    '''
    def __init__(self):
        self.urlist = Urlist()
        self.queue = Queue()
        self.in_queue = UrlQueue()

    def init(self,home_list, reptile_num):
        '''
        所有动态初始化过程 
        '''
        #新建 queue  in_queue list
        home_num = len(home_list)
        #线程个数
        self.reptile_num = reptile_num
        self.urlist.init(home_num)
        self.in_queue.init(home_num)

    def reptilesRun(self):
        '''
        所有线程开始运行
        '''
        self.reptiles = []
        for i in range(self.reptile_num):
            t = Reptile()
            self.reptiles.append(t)
        for t in self.reptiles:
            t.start()

class ReptileCtrlRcv:
    '''
    爬虫控制线程  掌控一些公共信息 以作备份等
    接受信号 并作相应操作
    其属于ReptileLib 可以直接操作主程序
    与clientServ进程通过Queue实现交流
    可以在ReptileLib的爬虫线程运行前设置好环境
    Queue传输消息:
        [signal,[url,url,url]]
    '''
    def __init__(self, url_queue, url_list, url_in_queue, Flock, tem_siteID = [0]):
        '''
        '''
        self.url_queue = url_queue
        self.url_list = url_list
        self.url_in_queue = url_in_queuen
        self.flock = Flock
        self.tem_siteID = tem_siteID 

    def parseSignal(self, signal):
        '''
        中央程序 为相关signal调用一定的方法处理
        '''
        pass

    def recvNewUrls(self, signal):
        '''
        从CentreSev得到新的urls
        插入到ReptileLib的公共数据中
        signal = ['signaltype',
                  siteID,
                  [
                    [title, url],
                    [title, url],
                    [title, url],
                  ]
                ]
        '''
        self.tem_siteID[0] = int(signal[1])
        url_list = signal[2]
        for u in url_list:
            '''
            添加每个url如 url_queue
            '''
            self.url_queue.put(u)

    def halt(self):
        '''
        中断操作
        '''
        pass

    def stop(self):
        '''
        向公共队列插入停止消息 
        各线程得到消息后停止运行
        '''
        pass

    def resume(self):
        '''
        恢复断电继续运行
        '''
        pass
    
    def status(self):
        '''
        返回状态
        '''
        pass

    def run(self):
        '''
        各线程开始运行
        '''
        pass

    


