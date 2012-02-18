# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from iofile import *

class testInitConfig:
    '''
    initConfig
    '''
    def __init__(self):
        '''
        init
        '''
        self.config = DBConfig()
        self.home_urls = [
            {'name':'cau',
             'url':'http://www.cau.edu.cn'
            },
            {
            'name':'baidu',
            'url':'http://www.baidu.com'
            }
        ]

    def init_test(self):
        '''
        init_config
        '''
        print '>>>>>>init config'
        self.config.init(self.home_urls)
        self.config.initConfig()
        self.config.initSites()

class DBSource_test:
    def __init__(self):
        self.dbsource = DBSource()
        self.dbsource.init(0)

    def saveHtml(self, 
                info = {'url':"www.baidu.com",'title':"baidu",'date':"2012-02-12"},source = "<html>source</html>",\
                parsedSource = "<html>parsedSource</html>"\
                ):
        '''
            info = {
                'url':"www.baidu.com",
                'title':"baidu",
                'date':"2012-02-12",
            }
        '''
        self.saveHtml(info, source, parsedSource)

if __name__ == '__main__':
    dbs = DBSource_test()
    info = {
            'url':'www.cau.edu.cn',
            'title':'¹þ¹þ£¬ÎÒÊÇ´ºÎ¬',
            'date':'2012-02-18'
    }
    source = '<div>2343233</div>'
    parsedSource = '<div>parsed</div>'
    dbs.saveHtml(info, source, parsedSource)
