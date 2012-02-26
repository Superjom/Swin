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
from judger import Judger

class HtmlParser:
    '''
    从html中提取出相关tag
    '''
    def init(self,html):
        self.d=pq(html)
        if not len(self.d('body')):
            print 'not html'
            return False
        return True

    def getNodeText_List(self, tagname):
        nodes = self.d(tagname)
        nodelist = []
        for i in range(len(nodes)):
            node = nodes.eq(i)
            nodelist.append(node.text())
        return nodelist

    def getALink_list(self):
        '''
        返回 url [name:url]
        '''
        a=self.d('a')
        aa = []
        for i in range(len(a)):
            aindex=a.eq(i)
            href = aindex.attr('href')
            aa.append( [aindex.text(), href])
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
            srcidx = src.eq(i)
            ads.append(srcidx.attr('src'))
        return ads
       
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
        self.configure.init('PicParser')
        #get width
        max_width = self.configure.getint('max_width')
        max_height = self.configure.getint('max_height')
        self.__maxsize = (max_width, max_height)
        print 'get maxsize',self.__maxsize
        #压缩的尺寸
        self.__compressed_size = None
    
    def init(self, source):
        print 'image open'
        imgData = StringIO(source)
        #the initial size
        self.img = Image.open(imgData)
    
    def getSize(self):
        return self.img.size
    
    def getCompressSize(self):
        #the pic size
        width = self.img.size[0]
        height = self.img.size[1]
        ppn = width / height 
        #the compressed size
        print '__maxsize', self.__maxsize
        mwidth = self.__maxsize[0]
        mheight = self.__maxsize[1]
        if ppn > (mwidth / mheight):
            width = self.__maxsize[0]
            height = width / ppn
        else:
            height = self.__maxsize[1]
            width = ppn * height
        return (width, height)

    def getCompressedPic(self):
        '''
        compress picture
        {size: size, source: source}
        '''
        size = self.getCompressSize()
        _size = (int(size[0]), int(size[1]))
        source = self.img.resize(_size).tostring()
        return {'size':size, 'source':source}

class Collector:
    '''
    从html中提取相关tag内容
    并组合为一定格式  并进行存储
    主要作用为转化为xml格式
    '''
    def __init__(self, homeurls):
        self.htmlparser = HtmlParser()
        self.judger = Judger(homeurls)

    def init(self, html):
        '''
        显式刷新缓存内容
        '''
        self.html=html
        if not self.htmlparser.init(html):
            return False
        self.d = self.htmlparser.d
        self.d=pq(html)
        self.d('script').remove()
        self.d('style').remove()
        return True
        
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
        
    
    def __xmlAppendNodesTextList(self, xmlnode, tagname):
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
        strr='<html></html>'
        titleText = self.getTitleText()
        self.dd = dom.parseString(strr)
        html = self.dd.firstChild
        html.setAttribute('url', url)
        #为如下标签设立记录
        for tag in ['title','b', 'h1', 'h2', 'h3']:
            self.__xmlAppendNodesTextList(html, tag)
        #生成a
        aa=self.htmlparser.getALink_list()
        a=self.dd.createElement('a')
        for u in aa:
            #i=self.transurl.trans_d(i) #对url转化为标准绝对地址
            aindex=self.dd.createElement('item')
            aindex.setAttribute('title',u[0])
            #aindex.setAttribute('href',self.a_trav(aa[i]))
            aindex.setAttribute('href',self.judger.transToStdUrl(url, u[1]))
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
        return html.toxml()


