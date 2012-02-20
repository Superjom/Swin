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
from socket import *
from time import ctime
import threading
#---------------------------------------------------------
import configure
from signal import Signal
import communitor
#---------------------------------------------------------

HOST = ''
PORT = 21569
BUFSIZ = 1024
ADDR = (HOST,PORT)

class CentreServ(threading.Thread):
    def __init__(self):
        Name="chun"
        threading.Thread.__init__(self, name = Name )  
        self.tcpSerSock = socket(AF_INET, SOCK_STREAM)
        self.tcpSerSock.bind(ADDR)
        self.tcpSerSock.listen(5)
        self.num = 0

    def run(self):
        print 'serv'
        while True:
            print 'waiting for connection...'
            tcpCliSock,addr = self.tcpSerSock.accept()
            print '...connected from:',addr

            print 'start a new thread'
            #start new thread to serve client
            t = threading.Thread(target = self.getConnection, args=[tcpCliSock])
            t.setDaemon(True)
            t.start()
            print 'thread is ended'
            if self.num == 3:
                print 'self.num ',self.num
                print 'it is going to end the server program'
                break
        self.tcpSerSock.close()

    def frame(self):
        '''
        显示图形界面
        '''
        pass

    def getConnection(self, clientsock):
        self.num += 1 
        while True:
            data = clientsock.recv(4096)
            if not len(data):
                print 'received empty data'
                print 'thread is to end'
                break
            else:
                print data
                clientsock.send('[%s] %s'% (ctime(),data))
        clientsock.close()



'''
class Cal(threading.Thread):
    def __init__(self):
        Name = "shasha"
        threading.Thread.__init__(self, name = Name )  

    def run(self):
        while True:
            2**200
            print 'cal'

th = CentreServ()
sh = Cal()
th.start()
sh.start()
'''

