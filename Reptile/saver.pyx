'''
Project:	saver.py	2012-01-12
Function:	IO库	将Reptile下载的内容进行存储
			关于数据库的所以操作都会在此定义
			需要将parse，对网页的解析的相关操作也在此定义
			需要对源码处理的一些操作
Author:		Chunwei
'''
import sys
sys.path.append('../')

import sqlite as sq

#导入配置文件
import config
#导入标准html解析库
from Parser.htmlparser import HtmlParser
'''
保证各个站点分开
数据库结构：
	sites:
		tables:
			site1name
				id		url		source		psource
			site2name
				id		url		source		psource
			...
	urls:
		tables:
'''

def get_split_node_text(node_list):
	'''
	取得node表用特殊标志隔开的字符
	'''
	#多表示了一个标签
	for node in node_list:
		strr += node+config.DB_SPLIT_SYMB
	print strr	
	return strr


class Saver:
	def __init__(self):
		'''
		init 
		'''
		self.cx = sq.connect(config.DATABASE_PATH)
		self.cu = self.cx.cursor()
        #html解析 self.htmlparser = HtmlParser() 
	def save_url(self,url):
		'''
		存储urls
		便于以后对url配套（pagerank）的操作
		'''
		pass
	
	
	def save(self,site_name,source):
		'''
        site_name:
            为每个站点建立了一个表 表的名称
        source:
            html源码

		对网页内容的存储
        !!!此处需要在最终排序时候，做一些改进
        开发时默认，按照原来的方式存储
        此处保存时候，仍旧按照原来的方式保存
        当然，如果磁盘有限，可以直接保存源码，待最终的时候再进行分词
		'''
		#解析 得到相关内容
		strr = "insert into %s (url,source,psource)values('%s','%s','%s')"%(site_name,url,source,psource)
		print strr
		return self.cu.execute(strr)
		
	
	
