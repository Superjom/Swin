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
        self.section = None
#-------------------------------------------------------------
    def init(self, section):
        '''
        set the seciton
        '''
        self.section = section
    
    def set(self,option, value):
        '''
        设定属性值
        '''
        self.cp.set(self.section, option, value)

    def get(self,option):
        '''
        取得属性值
        '''
        return self.cp.get(self.section, option)

    def getint(self, option):
        return self.cp.getint(self.section, option)
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
    c.init("PicParser")
    print c.get("max_width")

