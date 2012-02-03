# -*- coding: utf-8 -*-
'''
Project:     judger.pyx
Author:      Chunwei
Date:        2012-01-14
!!!!!需要考虑DNS缓存方面的问题
'''
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import sqlite3 as sq

import urlparse
#导入配置文件
import config

class Judger:
    def __init__(self):
        '''
        init
        从数据库或者配置文件中读取主url
        '''
        #此处应该从数据库读取相关配置
        #从数据库读取相关内容
        print config.DATABASE_PATH
        self.cx = sq.connect(config.DATABASE_PATH)
        print self.cx

        self.cu = self.cx.cursor()

        strr = "select url from sites"
        #self.home_urls=['http://www.cau.edu.cn',]
        print strr
        self.home_urls = self.cu.execute(strr)
        #在进行分布式时，判断一个url是否为本平台的url
        self.this_pc_site_url = ['http://www.cau.edu.cn']

    def get_home_num(self):
        return len(self.home_urls)

	
    def url_trans_d(self,baseurl,url):
        '''
        将url 不管是相对还是绝对地址 最终转换为绝对地址
        '''
        if len(url)>4:
            if url[:4]!='http':
                return urlparse.join(baseurl,url)
        return url
				
	
    def judge(self,newurl):
        '''
        判断一个url是否有效
        是否为需要收录的站点范围内
        '''
        for i,url in enumerate(self.home_urls):
            l=len(url)
            if newurl[:l]==url:
                return i
        return -1

    def judge_this_pc(self,newurl):
        '''
        判断是否为这个平台的url
        每个平台分配一个或多个站点的url
        判断是否为这个站点的url
        如果不是本平台url 考虑传送给其他平台进行处理
        '''
        for url in self.this_pc_home_url:
            if newurl[:len(url)] == url:
                return True
        return False

    def debug(self) :
        '''
        测试
        '''
        print '!>get_home_num'
        print 'num of sites',self.get_home_num() 
        hurl='http://www.google.com/home/'
        burl='../index.php'
        print 
        
        print '!>url_trans_d'
        print 'trans_d: ',hurl,' ',burl
        print self.url_trans_d(hurl,burl) 
        print



    


