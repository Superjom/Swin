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

class Collector():
    '''
    从html中提取相关tag内容
    并组合为一定格式  并进行存储
    主要作用为转化为xml格式
    '''
    def __init__(self):
        self.htmlparser = HtmlParser()

    def init(self, html):
        '''
        显式刷新缓存内容
        '''
        self.html=html
        self.d=pq(html)
        self.d('script').remove()
        self.d('style').remove()
        self.htmlparser.init(html)
        
    def clear_other_node(self):
        '''
        删除无用标签
        '''
        self.d('head').remove()
        self.d('h1').remove()
        self.d('h2').remove()
        self.d('h3').remove()
        self.d('b').remove()
        self.d('a').remove()
        
    def getTitleText(self):
        '''
        提取 title
        '''
        return self.d('title').text()

    def getNodes(self,tag_name):
        '''
        get a list of certain tag nodes
        '''
        return self.d(tag_name)
        
    
    def XmlAppendNodesTextList(self, xmlnode, tagname):
        '''
        xml节点为list中每个元素添加记录
        注意需要提前将链接化为 绝对链接
        如 <b> 
            <item>hello</item>
            <item>world</item>
          </b>
        '''
        html_node_text_list = self.d(tagname)
        print html_node_text_list
        childnode = self.dd.createElement(tagname)
        print childnode
        for i in range(len(html_node_text_list)):
            '''
            为每个元素添加一个item
            '''
            text_node = self.dd.createElement('item')
            text_node.setAttribute('text', html_node_text_list.eq(i).text())
            childnode.appendChild(text_node)
        xmlnode.appendChild(childnode)

    def transXml_Str(self,url):
        '''
        返回xml源码 以此格式储存
        '''
        str='<html></html>'
        titleText = self.getTitleText()
        self.dd = dom.parseString(str)
        html = self.dd.firstChild
        #为如下标签设立记录
        for tag in ['title','b', 'h1', 'h2', 'h3']:
            self.XmlAppendNodesTextList(html, tag)
        #生成a
        aa=self.htmlparser.getALink_Dic()
        a=self.dd.createElement('a')
        for i in aa:
            #i=self.transurl.trans_d(i) #对url转化为标准绝对地址
            aindex=self.dd.createElement('item')
            aindex.setAttribute('name',i)
            #aindex.setAttribute('href',self.a_trav(aa[i]))
            aindex.setAttribute('href',self.judger.transToStdUrl(url, aa[i]))
            a.appendChild(aindex)
        html.appendChild(a)
        #加入content
        #htmltext=self.d.html().decode('gbk','ignore').encode('utf-8')
        #ht=pq(htmltext)
        #bug 说明
        #此处  需啊注意 其中有html的特殊字符   &# 等等
        #在分词的时候另外说明
        content=self.d.text()
        cc=self.dd.createElement('content')
        ctext=self.dd.createTextNode(content)
        cc.appendChild(ctext)
        html.appendChild(cc)
        #print self.dd.toprettyxml()
        return html

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
        strr = 'CREATE TABLE IF NOT EXISTS "img%d" ("id" CHAR PRIMARY KEY  NOT NULL , "source" CHAR)' % siteID
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

    def saveHtml(self, info, source, parsed_source):
        '''
        save html source
        info = {
            url:    urlstr,
            title:  titlestr,
            date:   date
        }
        '''
        print '-------------------------------------'
        print 'saveHtml'
        print 'save html source'
        strr = 'insert into source_info%d (url, title, date) values("%s", "%s", "%s")' % (self.siteID, info['url'], info['title'], info['date'])
        print strr
        self.cu.execute(strr)
        strr = "insert into source%d (source, parsedSource) values('%s', '%s')" % (self.siteID, source, parsed_source)
        print strr
        self.cu.execute(strr)
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
        strr = "insert into %d_img_info (url, width, height) values ('%s', '%s', '%s')" % (self.siteID, info['url'], info['width'], info['height'])
        self.cu.execute(strr)
        #save image source
        strr = "insert into img%d (source) values ('%s')" % (self.siteID, sq.Binary(source))
        self.cu.execute(strr)
        self.cx.commit()
        

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

if __name__ == '__main__':
    '''
    d = DBConfig()
    home_urls = [
        {'name':'cau',
         'url':'http://www.cau.edu.cn'
        },
        {
        'name':'baidu',
        'url':'http://www.baidu.com'
        }
    ]
    d.init(home_urls)
    d.initConfig()
    d.initSites()
    '''

    c = DBSource()
    c.init(0)
    info = {
        'url':"www.cau.edu.cn",
        'title':"i你好，我就是试试啊",
        'date':"2012-02-12",
    }
    source = "<html><b>hello world</b></html>"
    parsedSource = "<html><b>right parsedSource</html>"
    c.saveHtml(info, source, parsedSource)
    
    
    
    




