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
        self.home_urls = ['http://www.cau.edu.cn']
    
    def judgeUrl(self,newurl):
        '''
        judge whether a newurl belongs to sites
        '''
        for url in self.home_urls:
            length = len(url)
            if len(newurl) >= length and newurl[:length] == url:
                return True
        return False
    
    def transToStdUrl(self,homeurl,newurl):
        '''
        transfer a new url to a right format url 
        '''
        if newurl[:7] != 'http://':
            '''
            测试是否已经为绝对地址
            '''
            return newurl
        return urlparse.urljoin(homeurl, newurl)


if __name__ == "__main__":
    j = Judger()
    print j.judgeUrl("http://www.cau.edu.cn/hoz")
    print j.judgeUrl("http://google.com")
    print j.transToStdUrl("http://www.cau.edu.cn/hsz/pray", "../index.html")
        
            
                
        
