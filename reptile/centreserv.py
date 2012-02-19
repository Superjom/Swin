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

