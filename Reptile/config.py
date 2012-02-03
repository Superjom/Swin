# -*- coding: utf-8 -*-
'''
Created:	2012-01-12
Author:		Chunwei
Project:	Reptile 配置文件
请不要随意更改本文件内容
'''
#---------------------------------------------------
#----Reptile------------------------
#线程数目
THREAD_NUM = 20
#每个子线程最大下载页面数目
PER_MAX_PAGES = 2000

#数据库文件地址
DATABASE_PATH = '/home/chunwei/swin/Data/chun.sqlite'

#数据库中标签分割符
DB_SPLIT_SYMB = '@.@'

#线程名称
THREAD_NAME = 'th'

#---------------------------------------------------
#-----communitor----------------
HOST = ''
PORT = 21567
BUFSIZ = 1024
ADDR = (HOST,PORT)
#先股传递时message的分割符
URLS_SPLIT_SG = '@~@'
#其他平台上积累的urls数量 达到这个数量就传递给其它平台
PER_SEND_URLS_NUM = 100

#消息标志长度
SIGN_LEN = 2
#TCP 交流标志 放置在消息首端
SIGN = {
        'init':     '00',  #初始化
        'add_url':  '01',  #其他平台向本平台发送urls
}
#本地储存其他平台的url池的最大数目
OTHER_URL_NUM = 100

