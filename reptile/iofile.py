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
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
'''
Created on Feb 12, 2012

@author: chunwei
'''
from sourceparser import HtmlParser
from pyquery import PyQuery as pq
import xml.dom.minidom as dom
from judger import Judger
from StringIO import StringIO
from PIL import Image
from configure import Configure

import sqlite3 as sq

class DBConfig:
    '''
    operation of database concerning file savage
    '''
    def __init__(self):
        #config database
        self.configure = Configure()
        dbpath = (self.configure.getDBPath())[1:-1]
        print "dbpath  ",dbpath
        self.cx = sq.connect(dbpath)
        self.cu = self.cx.cursor()

    def __del__(self):
        self.cx.commit()

    def init(self, home_list):
        '''
        mannual init
        '''
        self.home_list = home_list

    def initConfig(self):
        '''
        create table config and insert some data
        sitelist:
            [
                {
                    url:    urlstr,
                    name:   namestr,
                    date:   datestr
                },

            ]
        '''
        print 'init configure'
        #create configure table
        print 'init flag'
        self.__create_flag()
        strr = 'CREATE  TABLE IF NOT EXISTS configure ("siteID" INTEGER PRIMARY KEY  AUTOINCREMENT  NOT NULL , "url" CHAR NOT NULL , "name" CHAR NOT NULL)' 
        self.cu.execute(strr)
        #insert data
        for site in self.home_list:
            '''
            insert each site into configure table
            '''
            strr = "insert into configure (url, name) values('%s', '%s')" % (site['url'], site['name'])
            print strr
            self.cu.execute(strr)
            self.cx.commit()

    def __create_flag(self):
        '''
        存储中断后内存中的信息
        '''
        strr = 'CREATE TABLE IF NOT EXISTS "flag" ("id" INTEGER PRIMARY KEY NOT NULL, "info" TEXT)'
        print strr
        self.cu.execute(strr)

    def __create_source_info(self, siteID):
        '''
        create {siteID}_source_info table 
        '''
        strr = 'CREATE TABLE IF NOT EXISTS "source_info%d" ("docID" INTEGER PRIMARY KEY  NOT NULL , "url" CHAR, "title" CHAR, "date" DATETIME)' % siteID
        print strr
        self.cu.execute(strr)

    def __create_source(self, siteID):
        '''
        create {siteID}_source table
        '''
        strr = 'CREATE TABLE IF NOT EXISTS "source%d" ("docID" INTEGER PRIMARY KEY  NOT NULL , "source" CHAR, "parsedSource" CHAR)' % siteID
        print strr
        self.cu.execute(strr)

    def __create_img_info(self, siteID):
        '''
        create {siteID}_img_info
        '''
        strr = 'CREATE TABLE IF NOT EXISTS "img_info%d" ("id" INTEGER PRIMARY KEY  NOT NULL , "url" CHAR, "width" INTEGER, "height" INTEGER)' % siteID
        print strr
        self.cu.execute(strr)

    def __create_img(self, siteID):
        '''
        {siteID}_img
        '''
        strr = 'CREATE TABLE IF NOT EXISTS "img%d" ("id" INTEGER PRIMARY KEY  NOT NULL , "source" blob)' % siteID
        print strr
        self.cu.execute(strr)


    def initSites(self):
        '''
        init tables:
            {siteID}_source_info
            {siteID}_source
            {siteID}_img_info
            {siteID}_img
        '''
        print 'init Sites'
        for siteID in range(len(self.home_list)):
            #sourceinfo
            self.__create_img(siteID)
            self.__create_img_info(siteID)
            self.__create_source(siteID)
            self.__create_source_info(siteID)

    def getSiteUrls(self):
        '''
        get all site home_urls
        '''
        strr = "select url from sites"
        return self.cu.execute(strr)


class DBSource:
    '''
    Database operation of html image and other file source
    '''
    def __init__(self):
        self.configure = Configure()
        dbpath = (self.configure.getDBPath())[1:-1]
        self.cx = sq.connect(dbpath)
        self.cu = self.cx.cursor()
        self.siteID = -1

    def __del__(self):
        self.cx.commit()

    def init(self, siteID):
        '''
        read database connection
        '''
        self.siteID = siteID

    def saveFlag(self, info):
        '''
        存储中断后信息
        '''
        strr = "delete from flag"
        self.cu.execute(strr)
        strr = "insert into flag (info) values('%s')" % info
        self.cu.execute(strr)
        self.cx.commit()

    def saveHtml(self, info, source, parsed_source):
        '''
        save html source
        info = {
            url:    urlstr,
            title:  titlestr,
            date:   date #爬取的日期
        }
        '''
        print '-'*200
        strr = "insert into source_info%d (url, title, date) values('%s', '%s', '%s')" % (self.siteID, info['url'], info['title'], info['date'])
        self.cu.execute(strr)
        strr = "insert into source%d (source, parsedSource) values('%s', '%s')" % (self.siteID, "", parsed_source)
        print '-'*200
        #print strr
        self.cu.execute(strr)
        print '-'*200
        self.cx.commit()
        
    def saveImg(self, info, source):
        '''
        save image into database
        info = {
            url:    urlstr,
            width:  width,
            height: height
        }
        '''
        #save image info
        strr = "insert into img_info%d (url, width, height) values ('%s', '%s', '%s')" % (self.siteID, info['url'], info['width'], info['height'])
        print strr
        self.cu.execute(strr)
        self.cu.execute('insert into img%d (source) values (?) '%self.siteID,(sq.Binary(source),))
        self.cx.commit()

    def getImg(self, siteID, imgID):
        strr = "select source from img%d where id=%d" % (siteID, imgID)
        data = self.cu.execute(strr)
        print data
        return data.fetchone()
        

class File:
    '''
    对于外界io的一些方法
    用户可以自由修改
    '''
    def __init__(self):
        self.db = DBSource()

    def __parseSource(self,source):
        '''
        将html源码进行解析 
        并且输出为特定格式
        '''
        pass

    def saveCompressedPic(self, source):
        '''
        save compressed pictures
        '''
        data = self.__compressedPic(source)
        pass

    def saveSource(self, source):
        '''
        save source of html files to generate web cache
        '''
        pass

    def saveParsedSource(self,source):
        '''
        save parsed html source files in special format
        '''
        data = self.__parseSource(source)
        pass

    def saveFile(self,source,filename):
        '''
        save other files including pdf word
        '''
        pass


