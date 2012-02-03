# -*- coding: utf-8 -*-
'''
Created on 2012-01-12

@author: chunwei
'''
from pyquery import PyQuery as pq
import xml.dom.minidom as dom
import chardet as c
	
class HtmlParser:
    '''
    从html中提取出相关tag
    '''
        
    def init(self,html):
        '''
        init 
        为了能够进行切换 将其设为单独函数
        '''
        #编码判断-------------------------------------------------------
        dcode=c.detect(html)
        if dcode['confidence']>0.7:
            #此处 考虑到中文仅仅GBK GB2312
            if dcode['encoding']=='utf-8':
                pass
            elif dcode['encoding']=='gbk' or dcode['encoding']=='gb2312':
				#需要转码
                html=html.decode('gbk','ignore').encode('utf-8')	
            else:
                print '!>encoding error',
                print dcode
                return False
        else:
            print 'encoding error'
            print dcode
            return False

        self.d=pq(html)
        #先去除一些无用标签
        self.d('script').remove()
        self.d('style').remove()
    
    def get_a(self):
        '''
        返回 url 的字典 name:url
        '''
        a=self.d('a')
        aa={}
        for i in range(len(a)):
            aindex=a.eq(i)
            aa.setdefault(aindex.text(),aindex.attr('href'))
        return aa
    
    def get_as(self):
        '''
        返回 a文本
        '''
        print 'get_as running'
        a=self.d('a')
        text=''
        urls=''
        for i in range(len(a)):
            aindex=a.eq(i)
            #print aindex.text()
            text+=aindex.text()+' '
            if aindex.attr('href'):
                urls+=aindex.attr('href')+' '
        return [text,urls]
            
    def get_url(self):
        '''
        返回所有url的list
        对于理学院的网页 frame 的结构 加入了对iframe的提取
        '''
        a=self.d('a')
        aa=[]
        for i in range(len(a)):
            aindex=a.eq(i)
            href=aindex.attr('href')
            aa.append(href)
        frame=self.d('frame')
        for i in range(len(frame)):
            aindex=frame.eq(i)
            aa.append(aindex.attr('src'))
        return aa
        
    def get_node(self,node):
        b=self.d(node)
        bb=[]
        for i in range(len(b)):
            bb.append(b.eq(i).text())
        return bb


class Collector(HtmlParser):
    '''
    从html中提取相信息
    '''
    def get_nodes(self,node):
        '''
        提取标签文本
        适用于  title b h1 h2 h3 等标签
        '''
        nodes=self.get_node(node)
        text=''
        for n in nodes:
            text+=n
        return text
    
    def get_content(self):
        '''
        提取html中主内容
        '''
        #去除无用标签
        self.__clear_other_node()
        return self.d('html').text()
    
    def __clear_other_node(self):
        '''
        删除无用标签
        '''
        self.d('head').remove()
        self.d('h1').remove()
        self.d('h2').remove()
        self.d('h3').remove()
        self.d('b').remove()
        self.d('a').remove() 


