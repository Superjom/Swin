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
'''
新特性：
    从urlib2 更替为 httplib 一次分配一个站点的爬取任务 重复利用DNS缓存
'''

class Reptile:
    '''
    单个线程
    '''
    def __init__(self, name, url_queue, url_list, url_in_queue, Flock, home_urls ,tem_conn, tem_home_url):
        '''
        name
        url_queue       从主服务器中分配到的url
        url_list        本地区分是否重复
        url_in_queue    解析得到的新url
        Flock
        home_urls       测试是否符合爬取集合
        tem_conn        初始的DNS 缓存
        tem_home_url    
        '''
        #本地测试url队列 如果在本地重复 则直接舍弃
        #如果不重复 加入临时队列 将来传输到中央服务器进行测试
        self.url_list = url_list
        #本地临时记录队列 在url_list中测试不重复后 加入in_queue
        #在积累到一定量后 传输给中央服务器管理
        self.url_queue = url_queue
        self.url_in_queue = url_in_queue
        self.Flock = Flock
        self.judger = Judger()
        threading.Thread.__init__(self, name = name )  
        self.home_urls = home_urls
        self.tem_conn = tem_conn
        self.tem_home_url = ''
        
    def run(self):
        '''
        运行主程序
        '''
        opener = urllib2.build_opener()
        while True:
            pass

    def getPage(page):
        '''
        page    子页面 如 ./index.html
        '''
        self.conn.request("GET", page)
        r1 = self.conn.getresponse()
        print r1.status
        if r1.status != 'OK':
            print r1.reason
            return False
        data = r1.read()
        if not len(data):
            return False
        return data

    def getConn(self, home_url):
        '''
        从CentreServ取得新的主站点地址
        刷新DNS缓存
        '''
        if home_url != self.tem_home_url:
            '''
            CentreServ分配了一个新的站点任务
            需要对本地DNS缓存进行刷新
            '''
            self.tem_conn.close()
            try:
                self.tem_conn = httplib.HTTPCoection(home_url)
                return True
            except:
                return False

    def parseSourceAddTemUrls(self, html_source):
        '''
        传入html_source 进行解析 
        取得其中的urls 加入到相应队列中
        '''
        pass





    
