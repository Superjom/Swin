# -*- coding: utf-8 -*-

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

class Queue:
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
        self.home_url = ''
        self.queue = []

    def init(self, siteID, home_url):
        self.siteID = siteID
        self.home_url = home_url

    def append(self, title, url):
        #对存入的url进行处理
        if url[:7] == 'http://':
            '''
            转为绝对地址
            '''
            le = len(self.home_url)
            url = url[le:]
        self.queue.append([title, url])

    def getList(self):
        return self.queue

    def clear(self):
        '''
        清空
        '''
        self.queue = []

    def pop(self):
        return self.queue.pop()

    def size(self):
        return len(self.queue)

    def show(self):
        for i in range(len(self.queue)):
            print self.queue[i]

class UrlQueue:
    def __init__(self, home_urls):
        self.siteNum = len(home_urls)
        self.queue = []
        for i in range(self.siteNum):
            q = Queue()
            q.init(i, home_urls[i])
            self.queue.append(q)
    
    def size(self, siteID):
        return self.queue[siteID].size()

    def append(self, siteID, title, url):
        self.queue[siteID].append([title, url])

    def pop(self, siteID):
        return self.queue[siteID].pop()

    def getList(self):
        return self.queue

    def clear(self, siteID):
        self.queue[siteID].clear()

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
