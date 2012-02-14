# -*- coding: utf-8 -*-
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

from ConfigParser import ConfigParser

class Configure:
    '''
    configure operation of reptile liberary
    '''
    def __init__(self):
        self.cp = ConfigParser()
        self.cp.read("../Data/reptile.conf")

    def getImgSize(self):
        pass
    
    def getDbDir(self):
        pass

class Collector():
    '''
    从html中提取相关tag内容
    并组合为一定格式  并进行存储
    '''
    def __init__(self):
        self.htmlparser = HtmlParser()
        self.judger = Judger()
        

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

    def transXml_Str(self,docID,url):
        '''
        返回xml源码 以此格式储存
        '''
        str='<html></html>'
        titleText=self.getTitleText()
        self.dd=dom.parseString(str)
        html=self.dd.firstChild
        #生成title
        title=self.dd.createElement('title')
        html.appendChild(title)
        title.setAttribute('text',titleText)
        #生成b
        self.XmlAppendNodesTextList(html, 'b')
        self.XmlAppendNodesTextList(html, 'h1')
        self.XmlAppendNodesTextList(html, 'h2')
        self.XmlAppendNodesTextList(html, 'h3')
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
        return html
        #print self.dd.toprettyxml()

import sqlite3 as sq
class DataBaseOperation:
    '''
    operation of database concerning file savage
    '''
    def __init__(self):
        #config database
		self.config_cx = sq.connect(config.DB_CONFIG_PATH)
		self.config_cu = self.cx.cursor()


        



class File:
    '''
    对于外界io的一些方法
    用户可以自由修改
    '''
    def __parseSource(self,source):
        '''
        将html源码进行解析 
        并且输出为特定格式
        '''
        pass

    def __compressedPic(self,source):
        '''
        compress picture
        '''
        imgData = StringIO(source)
        img = Image.open(imgData)
        print img.size
        size = img.size
        width = size[0]
        height = size[1]
        #proportion of width and height
        ppn = width / height  
        if ppn > config.IMG_SIZE_PPN:
            '''
            width is longer
            limit width
            '''
            width = IMG_MAX_SIZE[0]
            height = width / ppn
        else:
            '''
            limit height
            '''
            height = IMG_MAX_SIZE[1]
            width = ppn * height
        size = (width,height)
        return img.resize(size)

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
   c = Collector()  
   f = open('hello.html','r')
   content = f.read()
   f.close()
   c.init(content)
   print c.getTitleText()
   print c.getNodes('b')
   print c.transXml_Str(1,'http://google.com').toprettyxml()


