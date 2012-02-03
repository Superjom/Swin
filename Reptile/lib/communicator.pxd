from socket import *
from time import ctime
import threading
import sys
sys.path.append('../')

import config

cdef class Communitor(threading.Thread):
    cdef:
        object tcpSerSock
        object judger
        object Rqueue
        object urlist
        object site_ip_info

