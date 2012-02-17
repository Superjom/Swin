# -*- coding: utf-8 -*-
import urlparse
'''
Created on Feb 12, 2012

@author: chunwei
'''
class Judger:
    '''
    测试url是否合格
    '''
    def __init__(self):
        '''
        get home_urls and other information
        '''
        self.home_urls = []

    def init(self, home_urls_list):
        '''
        更新home_urls
        '''
        self.home_urls = home_urls_list
    
    def judgeUrl(self,newurl):
        '''
        judge whether a newurl belongs to sites
        '''
        for siteID,url in enumerate(self.home_urls):
            length = len(url)
            if len(newurl) >= length and newurl[:length] == url:
                return siteID
        return -1
    
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

    def minusUrl_bool(self, siteID, url):
        '''
        将绝对url统一去除home_url 以剪短字符串
        '''
        le = len(self.home_urls[siteID])
        if len(url) < le :
            return False
        else:
            turl = url[le:]
            if turl[0] == '/':
                turl = turl[1:]
            return turl

if __name__ == "__main__":
    j = Judger()
    home_urls = ['http://www.cau.edu.cn', 
                    'http://www.google.com']
    j.init(home_urls)
    turl = "./tem/index.php"
    url = j.transToStdUrl('http://www.cau.edu.cn/page', turl)
    print 'url: ',url
    siteID = j.judgeUrl(url)
    print j.minusUrl_bool(siteID, url)

        
            
                
        
