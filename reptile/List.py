class List:
    '''
    内存管理
    '''
    def __init__(self):
        pass

    def getSize(self):
        pass

    def insert(self, i, node):
        pass
    
    def find(self, url):
        pass

    def returnUrlsStr(self):
        pass
    

class UrlQueue:
    '''
    url队列
    '''
    def __init__(self):
        self.queue = []

    def append(self,url):
        self.queue.append(url)

    def getList(self,url):
        return self.queue

    def clear(self):
        '''
        清空
        '''
        self.queue = []

