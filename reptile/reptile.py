# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2012

@author: chunwei
'''
import os
import threading  
import time  
import urllib2  
import StringIO  
import gzip  
import string  

import httplib

from judger import Judger
from List import List
from List import UrlQueue
from sourceparser import HtmlParser
from sourceparser import PicParser

from iofile import DBSource
from iofile import Collector

import datetime as datetime
'''
新特性：
    从urlib2 更替为 httplib 一次分配一个站点的爬取任务 重复利用DNS缓存
'''
class Reptile:
    '''
    单个线程
    '''
    def __init__(self, name, url_queue, url_list, url_in_queue, Flock, home_urls , is_new_task, tem_conn, tem_siteID):
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
        #本地测试url队列 如果在本地重复 则直接舍弃
        #如果不重复 加入临时队列 将来传输到中央服务器进行测试
        self.__url_list = url_list
        #本地临时记录队列 在url_list中测试不重复后 加入in_queue
        #在积累到一定量后 传输给中央服务器管理
        self.__url_queue = url_queue
        self.htmlparser = HtmlParser()
        self.picparser = PicParser
        #默认为每一个站点分配一个inqueue
        self.__url_in_queue = url_in_queue
        self.__Flock = Flock
        self.__judger = Judger()
        threading.Thread.__init__(self, name = name )  
        self.__home_urls = home_urls
        self.__conn = tem_conn
        #init temporary home_url and siteID
        #both to determine weather to refresh DNS cache
        #引用传递 方便进行对照
        self.__tem_siteID = tem_siteID
        self.__old_siteID = self.__tem_siteID
        self.__dbsource = DBSource()
        self.__collector = Collector()
        
    def run(self):
        '''
        运行主程序
        '''
        while(True):
            urlinfo = self.getAUrl()
            self.getPage(urlinfo[1])
            self.saveHtml(urlinfo[1], urlinfo[0])
            imgsrcs = self.getImgUrls()
            for src in imgsrcs:
                imgsource = self.getImg(src)
                self.picparser.init(imgsource)
                size = self.picparser.getSize()
                info = {
                    'url':src,
                    'width':size[0],
                    'height':size[1]
                }
                self.saveImg(info, imgsource)
                newurls = self.htmlparser.getALinkText_List()
            self.AddNewInQueue(newurls)

    def requestSource(self, url):
        '''
        page_url    子页面 如 ./index.html
        '''
        self.__conn.request("GET", url)
        r1 = self.__conn.getresponse()
        print r1.status
        if r1.status != 'OK':
            print r1.reason
            return False
        data = r1.read()
        if not len(data):
            return False
        return data
    
    def getPage(self, page_url):
        '''
        path_url     './home/index.php'
        '''
        data = self.requestSource(page_url)
        if data:
            self.__collector.init(data)
        return data
        
    
    def getImg(self, img_url):
        '''
        img_url    './img/1.jpg'
        '''
        return self.getPage(img_url)
        

    def updateConn(self):
        '''
        从CentreServ取得新的主站点地址
        刷新DNS缓存
        '''
        '''
        communitor 传入新的url
        '''
        if self.__old_siteID != self.__tem_siteID[0]:
            '''
            CentreServ分配了一个新的站点任务
            需要对本地DNS缓存进行刷新
            '''
            self.old_home_url = self.__tem_home_url[0]
            #更新数据库source操作
            self.__dbsource.init(self.old_home_url)
            
            if len(self.__tem_home_url):
                self.conn.close()
                
            try:
                self.conn = httplib.HTTPConnection(self.__tem_home_url)
                return True
            except:
                return False
    
    def getAUrl(self):
        if self.__url_queue.size() > 0:
            return self.__url_queue.pop()
        else:
            return False
    
    def getImgUrls(self):
        '''
        parse html source and return src_list
        '''
        return self.htmlparser.getPicSrcs_List()
        

    def AddNewInQueue(self, url_list):
        '''
        将new_url添加到对应的queue中
        '''
        for url in url_list:
            if not self.__url_list.find(url):
                '''
                not duplicate in url_list
                '''
    ################################################注意此处不能用siteID直接区分
    ################!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!需要进一步判断
                self.__url_in_queue[self.__tem_siteID].append(url)

    def saveHtml(self, url, title):
        '''
        存储 source 和 parsedsource to database
        '''
        today = datetime.date.today()
        info = {
            'title' :   title,
            'url':      url,
            'date':     datetime.date.isoformat(today)
        }
        self.__dbsource.saveHtml(info, self.__collector.html, self.__collector.transXml_Str(url))

    def saveImg(self, info, source):
        imgsource = self.picparser.compressedPic(source)
        self.__dbsource.saveImg(info, imgsource)
        





    
