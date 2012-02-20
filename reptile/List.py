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

import Queue

class List(list):
    'the runtime list for all the url list'
    def find(self, url):  
        
        l = len(self)  
        first = 0  
        end = l - 1  
        mid = 0  
        
        if l == 0:  
            self.insert(0,url)  
            return False  
        
        while first < end:  
            mid = (first + end)/2  
            if hash(url) > hash(self[mid]):
                first = mid + 1  
            elif hash(url) < hash(self[mid]):
                end = mid - 1  
            else:  
                break  
            
        if first == end:  
            if hash(self[first]) > hash(url):  
                self.insert(first, url) 
                return False  
            
            elif hash(self[first]) < hash(url):  
                self.insert(first + 1, url)  
                return False  
            
            else:  
                return True  
                
        elif first > end:  
            self.insert(first, url) 
            return False  
        else:  
            return True  

    def show(self):
        print '-'*50
        print 'list-'*10
        for i in range(len(self)):
            url = self[i]
            print hash(url),'__',url

class Urlist:
    def __init__(self, siteNum):
        self.siteNum = siteNum
        self.list = []
        for i in range(siteNum):
            self.list.append(List())

    def find(self, siteID, url):
        '''
        find url in list 
        '''
        return self.list[siteID].find(url)

    def show(self):
        print 'show list'
        for i in range(self.siteNum):
            print '-'*50
            print self.list[i].show()
#get() 超时时间
TIMEOUT = 3

class Queue(Queue.Queue):
    '''
    url队列
    '''
    def __init__(self):
        '''
        存储格式:
            siteID
            home_url
            相对地址唯一标志一个url
        '''
        self.siteID = -1
        
    def init(self, siteID):
        self.__siteID = siteID

MAX = 100
class UrlQueue:
    def __init__(self, home_urls):
        self.siteNum = len(home_urls)
        self.queue = []
        #统一记录每个Queue的长度
        self.qsize = []
        #扫描指针 从此Queue检测是否符合要求
        self.__index = 0
        
        for i in range(self.siteNum):
            q = Queue()
            q.init(i)
            self.queue.append(q)
            self.qsize.append(0)
    
    def size(self, siteID):
        return self.queue[siteID].qsize()
    
    def __get_right_siteID(self):
        '''
        取得有一定量url储备的站点id
        '''
        maxn = 0
        max_index = 0
        size = 0
        while (self.size(self.__index) < MAX):
            '''
            遍历
            '''
            self.__index += 1
            size = self.size(self.__index)
            if self.size(self.__index) > maxn:
                maxn = self.size(self.__index)
                max_index = self.__index
        return (max_index, maxn)

    def put(self, siteID, title, url):
        self.queue[siteID].put([title, url])

    def get(self, siteID):
        '''
        如果数据池为空超过 3 s 
        则引发 Queue.empty 错误
        '''
        return self.queue[siteID].get(timeout = 3)
    
    def getUrlList(self, maxsize):
        '''
        从候选队列中选出一个最合适的队列 取出一定量的list
        '''
        idx = self.__find_right_index()
        size = self.size(idx)
        if size == 0:
            return False
        if size > maxsize:
            size = maxsize
        ulist = []
        for i in range(size):
            ulist.append(self.get(idx))
        res = {}
        res['siteID'] = idx
        res['urls'] = ulist
        return res
    
    def show(self):
        print 'show queue'
        for i in range(self.siteNum):
            print '-'*50
            self.queue[i].show()


if __name__ == '__main__':
    home_url_list = [
                'http://www.cau.edu.cn',
                'http://www.google.com',
    ]
    siteNum = len(home_url_list)
    l = Urlist(siteNum)
    q = UrlQueue(siteNum)

    l1 = List()
    l1.find("tem/index")
    l1.find("hel/index")
    l1.find("a.index")
    l1.find("a.index")
    l1.find("dsfsdfsd")
    l1.find("dfsfs")
    l1.show()
