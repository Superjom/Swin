# -*- coding: utf-8 -*-
'''
Created on Feb 12, 2012

@author: chunwei
'''
import os.path
#-----reptile-------------------
#delay time of a page
TIME_OUT = 2
#-----signal--------------------
#-----CentreServ----------------
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST, PORT)
#-----ClientServ----------------
C_HOST = ''
C_PORT = 21568
C_BUFSIZ = 1024
C_ADDR = (C_HOST, C_PORT)
#-----image---------------------
#max size of image
#both the width and height shall not exceed max_size
IMG_MAX_SIZE = (200,200)
#proportion of height and width
IMG_SIZE_PPN = IMG_MAX_SIZE[0] / IMG_MAX_SIZE[1]
#-----database------------------
DB_FILE_DIR = '/home/chunwei/workspace/Swin/Data'
DB_CONFIG_PATH = os.path.join(DB_FILE_DIR, 'config.sqlite')







