# -*- coding: utf-8 -*-
from __future__ import division
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


from pyquery import PyQuery as pq
import xml.dom.minidom as dom
import chardet 
from StringIO import StringIO
from configure import Configure
from PIL import Image

class HtmlParser():
    '''
    从html中提取出相关tag
    '''
    def init(self,html):
        self.d=pq(html)

    def getNodeText_List(self, tagname):
        nodes = self.d(tagname)
        nodelist = []
        for i in range(len(nodes)):
            node = nodes.eq(i)
            print 'tag ',tagname
            print node.text()
            nodelist.append(node.text())
        return nodes

    def getALink_Dic(self):
        '''
        返回 url 的字典 name:url
        '''
        a=self.d('a')
        aa={}
        for i in range(len(a)):
            aindex=a.eq(i)
            aa.setdefault(aindex.text(),aindex.attr('href'))
        return aa

    def getALinkText_List(self):
        '''
        取得链接列表
        '''
        a = self.d('a')
        aa = []
        for i in range(len(a)):
            aindex = a.eq(i)
            aa.append(aindex.attr('href'))
        return aa

    def getPicSrcs_List(self):
        '''
        取得图片的链接地址链表
        '''
        src = self.d('img')
        ads = []
        for i in range(len(src)):
            srcidx = ads.eq(i)
            ads.append(srcidx.attr('src'))

    def getALinksText_Str(self):
        '''
        返回 链接的名称文本
        '''
        a=self.d('a')
        text=''
        urls=''
        for i in range(len(a)):
            aindex = a.eq(i)
            #print aindex.text()
            text += aindex.text()+' '
        return text
       
    def getNodesText_Str(self,node):
        '''
        取得任意标签内的文本内容并累加返回
        '''
        b=self.d(node)
        bb=[]
        for i in range(len(b)):
            bb.append(b.eq(i).text())
        return bb

class PicParser:
    '''
    对图片的相关处理
    '''
    def __init__(self):
        self.configure = Configure()
        self.size = self.configure.getImageMaxSize()
    
    def init(self,source):
        print 'image open'
        imgData = StringIO(source)
        self.img = Image.open(imgData)
        print self.img.size
    
    def getSize(self):
        print 'get size: ', self.img.size
        return self.img.size
    
    def getCompressedSize(self):
        return self.size

    def compressedPic(self,source):
        '''
        compress picture
        '''
        size = self.getSize()
        print 'get size',size
        width = int(size[0])
        height = int(size[1])
        #proportion of width and height
        ppn = width / height  
        print 'width/height',width,height,width/height
        print 'ppn',ppn
        img_max_size = self.configure.getImageMaxSize()

        mwidth = img_max_size[0]
        mheight = img_max_size[1]

        if ppn > (mwidth / mheight):
            '''
            width is longer
            limit width
            '''
            width = img_max_size[0]
            height = width / ppn
        else:
            '''
            limit height
            '''
            height = img_max_size[1]
            width = ppn * height
        self.size = (int(width), int(height))
        print 'size  ',self.size
        source = self.img.resize(self.size).tostring()
        return {'size':self.size, 'source':source}

if __name__ == '__main__':
    print 'start'
    hp = HtmlParser()
    f = open('hello.html','r')
    source = f.read()
    f.close()
    hp.init(source)
    print 'a dic', hp.getALink_Dic()






