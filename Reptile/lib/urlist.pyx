'''
Created on 2012-1-11
Project:	Swin	a Better Seo for LAN
@author:	Chunwei
project:	urlist
function:	对爬虫的urlist的链接进行管理
'''
from libc.stdlib cimport realloc,malloc,free
import sys
sys.path.append('../')
#导入配置文件
import config

#定义urlist的数据结构
#初始化和增加长度
DEF TRUE=	1
DEF	FALSE=	0

DEF INIT_LENGTH=500
DEF PER_ADD_LENGTH=100

cdef struct UrlNode:
    char	*url
    long	hashvalue		#hash value of each url
							#it work faster in C mode
cdef struct UrlList:
    #为能够随机访问 实现一个顺序表 
    UrlNode	*list		
    int		length		#length of url_list
    int		maxlength	#容量
#-----------------------------------------
#-----------------------------------------

cdef class Urlist:
    '''
    对urlist数据结构的基础操作
    包括添加 删减
    '''

    def __cinit__(self,Flock):
        '''
        分配初始化空间
        '''
        #分配锁
        self.Flock = Flock

        self.urlist.list=<UrlNode *>malloc( sizeof(UrlNode)  * INIT_LENGTH )
        if self.urlist.list == NULL:
            print '!>init false'
        print '!>init OK'
        self.urlist.length=0				#长度
        self.urlist.maxlength=INIT_LENGTH	#最大空间
        print '!>status:'
        print '''!>length:%d 
maxsize %d'''%(self.urlist.length,self.urlist.maxlength)
	
    def __dealloc__(self):
        '''
        释放C空间
        包括urlist的指针空间及其指向的string空间
        '''
        print '!>delete all C space'
        free(self.urlist.list)
	
    cdef void dealloc(self):
        '''
        释放C空间
        包括urlist的指针空间及其指向的string空间
        '''
        cdef:
            int i=0
        print '!>delete all C space'
        '''
        print '!>删除所有string url'
        while(i<self.urlist.length):
            print '!>free %s'%self.urlist.list[i].url
            free(self.urlist.list[i].url)
            i+=1
        #删除指向string的空间
        '''
        print '!>删除urlist list'
        free(self.urlist.list)

    cdef int get_list_length(self):
        '''
        取得list长度
        '''
        return self.urlist.length
		
	
    cdef int Insert(self,int i,char *u):
        '''
        在元素插入到序号为i的位置
        '''
        cdef:
            UrlNode burl
        if i >self.urlist.length+1 or i<0:	
            #若在length插入 表示在末尾添加
            print 'i 大于length 越界错误'
            return FALSE
        #初始化新节点
        burl.url=u
        burl.hashvalue=hash(u)

        print '!>insert...',
        print hash(u),u
        #空间判断
        if (self.urlist.length+1)>self.urlist.maxlength:
            if self.AddSpace()==FALSE:
                print '空间过小，开始扩增'
                return FALSE
        #开始插入   
        cdef:
            int j=self.urlist.length
        
        while(j>i):
            self.urlist.list[j]=self.urlist.list[j-1]
            j-=1

        self.urlist.list[i]=burl
        #相关标志修改
        self.urlist.length+=1
        return TRUE
		
	
    cdef int AddSpace(self):
        '''
        添加空间
        '''
        cdef UrlNode *base=<UrlNode *>realloc( self.urlist.list, \
        sizeof(UrlNode) * (PER_ADD_LENGTH+self.urlist.maxlength))
        if base==NULL:
            return FALSE

        print '!>relloc succeed!'
        #相关标志修改
        self.urlist.list=base
        self.urlist.maxlength += PER_ADD_LENGTH
        return TRUE
	

    cdef int MinusSpace(self):
        '''
        减少空间
        当url开始减少时 减少空间分配
        '''
        cdef:
            UrlNode *base
        if(self.urlist.length<(self.maxlength-PER_ADD_LENGTH)):
            base= <UrlNode *>realloc( self.urlist.list, sizeof(UrlNode) * (PER_ADD_LENGTH-self.urlist.maxlength))
            if base==NULL:
                return FALSE
            #相关标志修改
            print '!>minux succeed!'
            self.urlist.list=base
            self.urlist.maxlength -= PER_ADD_LENGTH
        return TRUE

    cdef char* return_urls_str(self,Flock):
        '''
        返回urls组成的字符串
        然后直接清空
        此处需要设置一个锁
        '''
        #打开锁
        self.Flock.require()
        strr = ''
        for i in range(config.PER_URLS_NUM):
            '''
            将其中连接为一个字符串
            '''
            strr += self.urlist.list[i] + config.URLS_SPLIT_SG  
        #清空空间
        self.urlist.length = 0
        #释放锁
        self.Flock.release()
        return strr
	
    def show(self):
        '''
        展示内容
        '''
        print '!>begin to show content of list'
        print '!>status:    length:%d     maxlength:%d  '%(self.urlist.length,self.urlist.maxlength)
        cdef:
            int i
        i=0;
        for i in range(self.urlist.length):
            print i,self.urlist.list[i]

    cdef int Find(self,url):
        '''
        查找和插入
        外在接口
        '''
        cdef:
            int l=self.urlist.length
            int first=0
            int end=l-1
            int mid=0
            long uh=hash(url)

        print '!>find:%s'%url
    
        #开启锁 防止其他线程进行更改
        self.Flock.require()

        if l==0:
            self.Insert(0,url)
            self.Flock.release()
            return FALSE

        while first < end:  
            mid = (first + end)/2  

            if url> self.urlist.list[mid].hashvalue:  
                first = mid + 1  

            elif url < self.urlist.list[mid].hashvalue:  
                end = mid - 1  
            else:  
                break  
            
        if first == end:  
            if self.urlist.list[first].hashvalue > uh:  
                self.Insert(first, url) 
                self.Flock.release()
                return FALSE 
            
            elif self.urlist.list[first].hashvalue < uh:  
                self.Insert(first + 1, url)  

                self.Flock.release()
                return FALSE
            
            else:  
                self.Flock.release()
                return TRUE
                
        elif first > end:  
            self.Insert(first, url) 
            self.Flock.release()
            return FALSE
        else:  
            self.Flock.release()
            return TRUE 




		
	
	
		

	

