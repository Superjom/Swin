# -*- coding: utf-8 -*-
'''
Created on Feb 15, 2012

@author: chunwei
'''
from ConfigParser import ConfigParser

class Configure:
    '''
    configure operation of reptile liberary
    '''
    def __init__(self):
        self.cp = ConfigParser()
        self.cp.read("reptile.conf")

    #----------reptile-------------------------
    def getTimeOut(self):
        '''
        reptile:    time_out
        '''
        return self.cp.getint("reptile","time_out")
    
    def setTimeOut(self, time):
        self.cp.set("reptile", "time_out", time)

    #----------server--------------------------
    def getServerAddr(self):
        '''
        (HOST, PORT)
        '''
        host = self.cp.get('server', 'HOST')
        port = self.cp.get('server', 'PORT')
        return (host, port)

    def setServerAddr(self, addr):
        self.cp.set('server', 'HOST', addr[0])
        self.cp.set('server', 'PORT', addr[1])

    def getClientAddr(self):
        '''
        (HOST, PORT)
        '''
        host = self.cp.get('client', 'HOST')
        port = self.cp.get('client', 'PORT')
        return (host, port)

    def setServerAddr(self, addr):
        self.cp.set('client', 'HOST', addr[0])
        self.cp.set('client', 'PORT', addr[1])

    #---------image----------------------------
    def getImageMaxSize(self):
        '''
        (width , height)
        '''
        width = self.cp.getint('image', 'max_width')
        height = self.cp.getint('image', 'max_height')
        print 'config'
        print 'get w/h ',width,'    ',height
        return [int(width), int(height)]

    def setImageMaxSize(self, size = (200, 200)):
        self.cp.set('image', 'max_width', size[0])
        self.cp.set('image', 'max_height', size[1])

    #---------database-------------------------
    def getDBPath(self):
        return self.cp.get('database', 'db_file_path')

if __name__ == '__main__':
    c = Configure()    
    print c.getDBPath()

