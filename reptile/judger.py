# -*- coding: utf-8 -*-
import urlparse
'''
Created on Feb 12, 2012

@author: chunwei
'''
class Judger:
    '''
    传入测试到url必须都为绝对地址
    '''
    def __init__(self, home_urls):
        '''
        home_urls:     传入完整的绝对url 站点根目录
        如：http://www.cau.edu.cn
        '''
        self.home_urls = home_urls
        self.home_netlocs = []
        print self.home_urls


    def __findSiteID(self, url):
        '''
        url: 
        '''
        length = 0
        for i,u in enumerate(self.home_urls):
            length = len(u)
            if len(url) > length and url[:length] == u:
                return i
        return -1
    
    def judgeUrl(self, page_url, newurl):
        '''
        judge whether a newurl belongs to sites
        '''
        #转化为绝对地址
        url = self.transToStdUrl(page_url, newurl)
        #判断是否为收录范围内的
        #对url进行解析
        return self.__findSiteID(url)
   
    def transToStdUrl(self,homeurl,newurl):
        '''
        transfer a new url to a right format url 
        '''
        if newurl[:7] == 'http://':
            '''
            测试是否已经为绝对地址
            '''
            return newurl
        return urlparse.urljoin(homeurl, newurl)


