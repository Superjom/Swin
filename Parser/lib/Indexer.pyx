#############################################
#    Date:       2012-01-19 
#    Project:    Indexer 
#    @Author:    Chunwei
#############################################
'''
将会用二进制文件存储hash
运行中间过程将存储为n个tem文件
最终采用外排，将tem文件同一存储为1个整文件
初始化默认：
    每n个文件合并为一个tem文件
    最终，进行外排序 合并为一个大文件

工作简介：
    Hit_list运行时，对每一个词汇进行扫描，制成hitlist
        排序
        对一个文件处理完毕，交给Hit_lists
    Hit_lists:
        对内存中各个Hit_list合并排序为一个大的文件
        内存中，管理hit_list，若其中包含的内存达到EACH_TEM_CONTAIN ，则保存到一个tem文件中
'''
import os
from libc.stdlib cimport malloc,free,realloc
from libc.stdio cimport fopen, fwrite, fread,fclose,FILE 

import sys
sys.path.append('../') 

import config

from wordlist cimport HI

from Thesaurus cimport

DEF LIST_INIT_SIZE = 500
DEF PER_LIST_ADD = 30
DEF TRUE = 1
DEF FALSE = -1

#定义 Hit 结构
cdef struct Hit:
    long wordID
    long docID
    short score
    long pos


#单个list结构
cdef struct List:
    Hit *start
    long length #此记录中的总hit数目  初始化时需要使用
    long space #分配空间
    #long top  #没有作用

cdef class Sorter:
    '''
    快速排序主算法
    '''
    cdef: 
        Hit *dali
        long length

    cdef void init(self,Hit *data,long length):
        '''
        init 
        '''
        self.dali=data
        self.length=length

    cdef inline double __gvalue(self,Hit data):
        '''
		返回需要进行比较的值
        '''
        return data.wordID

    cdef void quicksort(self,long p,int q):
        '''
        主程序
        '''
        cdef: 
            long j

        a=self.dali
        st=[]

        while True:
            while p<q:
                j=self.partition(p,q)

                if (j-p)<(q-j):
                    st.append(j+1)
                    st.append(q)
                    q=j-1

                else:
                    st.append(p)
                    st.append(j-1)
                    p=j+1

            if(len(st)==0):
                return

            q=st.pop()
            p=st.pop()

    cdef long partition(self,int low,int high):
        cdef Hit v
        v=self.dali[low]

        while low<high:

            while low<high and self.__gvalue( self.dali[high] ) >= self.__gvalue( v ):
                high-=1
            self.dali[low]=self.dali[high]

            while low<high and self.__gvalue( self.dali[low] )<=self.__gvalue( v ):
                low+=1
            self.dali[high]=self.dali[low]

        self.dali[low]=v

        return low

cdef class WidSort(Sorter):
    '''
    根据 wid 进行排序
    '''
    cdef void init(self,Hit *data,long length):
        '''
        初始化 父亲 Sorter
        '''
        Sorter.init(self,data,length)

    cdef inline double __gvalue(self,Hit data):
        '''
        重载 Sorter 方法
		返回需要进行比较的值
        '''
        return data.wordID



cdef class DidSort(Sorter):
    '''
    根据 DocID 进行排序
    '''
    cdef void init(self,Hit *data,long length):
        '''
        初始化 父亲 Sorter
        '''
        Sorter.init(self,data,length)

    cdef inline double __gvalue(self,Hit data):
        '''
        重载 Sorter 方法
		返回需要进行比较的值
        '''
        return data.docID


cdef class ScoSort(Sorter):
    '''
    根据 score 进行排序
    '''
    cdef void init(self,Hit *data,long length):
        '''
        初始化 父亲 Sorter
        '''
        Sorter.init(self,data,length)

    cdef inline double __gvalue(self,Hit data):
        '''
        重载 Sorter 方法
		返回需要进行比较的值
        '''
        return data.score




cdef class Hit_list:
    '''
    hit存储队列
    对一个文件进行hit处理 然后进行快速排序
    解析完毕，交给Hit_lists管理
    '''

    cdef:
        long length
        List hitlist
        #分词系统
        #object ict

    #def __cinit__(self, Thes) :
    def __cinit__(self) :
        '''
        init
        初始化list
            Thes:   由Hit_lists传递统一的
        '''
        #直接显式调用init命令
        pass

        #分配空间 及初始化
        self.hitlist.start = <Hit *> malloc ( sizeof(Hit) *LIST_INIT_SIZE   )
        self.hitlist.space = LIST_INIT_SIZE  
        self.hitlist.length = 0
        #self.thes = Thes


    cdef Hit* Get_hitlist(self) :
        '''
        取得hitlist结构体
        整体赋值
        '''
        return self.hitlist


    cdef void init(self):
        '''
        手动初始化
        '''
        self.hitlist.start = <Hit *> malloc ( sizeof(Hit) *LIST_INIT_SIZE   )
        self.hitlist.space = LIST_INIT_SIZE  
        self.hitlist.length = 0
        #self.thes = Thes
    
    def __dealloc__(self)  :
        '''
        释放C空间
        '''
        print '释放C空间'
        free(self.hitlist.start) 

    cdef void Empty(self,int re) :
        '''
        将此队列清空
        re: 是否需要继续运行
        '''
        free(self.hitlist.start) 
        self.hitlist.space = 0
        self.hitlist.length = 0
        #重新分配空间
        if re == TRUE:
            '''
            需要继续运行
            '''
            self.__init__() 

    cdef Save_and_init(self) :
        '''
        将各项处理完成后，将内存中的hits块转移保存
        并且将原来的数据进行初始化
        '''

  cdef long GetLength(self) :
        '''
        取得length
        '''
        return self.hitlist.length

    cdef inline void  __AddSpace(self) :
        '''
        空间不足  添加空间
        '''
        cdef:
            HI *base

        base = <HI*>realloc( self.hitlist.start , LIST_INIT_SIZE +  PER_LIST_ADD   )  

        if self.hitlist.start != NULL:
            '''
            分配成功
            '''
            return FALSE

        self.hitlist.start = base
        self.space +=  PER_LIST_ADD   
        return TRUE

    cdef inline void __eq(self,HI hi,int wordID,int docID,short score,int pos):
        '''
        结构体赋值
        将hi进行赋值
        '''
        hi.wordID = wordID
        hi.docID = docID
        hi.score = score
        hi.pos = pos
        

    cdef int Append(self,int wordID, int docID, short score, int pos) :
        '''
        附加到后面
        结构体可以直接等号赋值
        '''
        self.__eq( self.hitlist.start[self.hitlist.length] , wordID , docID , score , pos ) 
        self.hitlist.length += 1

        if self.hitlist.length > self.hitlist.space-2:
            '''
            快要达到空间上限
            需要再分配内存
            '''
            return self.__AddSpace() 
        return TRUE
    
    cdef void WidSort(self) :
        '''
        将hitlist根据wordID进行快速排序
        在排完后再根据dID排序
        '''
        widsort = WidSort() 
        widsort.init(self.hitlist.start,self.hitlist.length) 
        didsort = DidSort() 
        didsort.init(self.hitlist.start,self.hitlist.length) 
        scosort = ScoSort() 
        scosort.init(self.hitlist.start,self.hitlist.length) 
        #根据wid排序
        widsort.quicksort(0,self.hitlist.length-1) 
        #在每个wid字段中，根据docID进行排序
        cdef:
            #现在正在扫描的wordID
            long cur_wid = self.hitlist.start[0].wordID 
            #扫描范围的起始地址
            long cur_step = 0
            #对于score排序时的字段起始地址
            long sco_step = 0
            int i=0,j=0

        while i<self.hitlist.length:
            '''
            在所有hit中进行扫描
            '''
            if self.hitlist.start[i].wordID == cur_wid:
                pass
            else:
                #更新cur_wid
                cur_wid = self.hitlist.start[i].wordID
                #在此字段内根据docID进行排序
                self.DidSort(cur_step,i-1) 

                #更新cur_step
                cur_step = i
                #在同一docID字段内根据score排序
                j = cur_step
                cur_sco_step = j

                while j<i:
                    if self.hitlist.docID == cur_did:
                        pass
                    else:
                       cur_did = self.hitlist.start[j].docID
                       scosort(cur_sco_step,j-1) 
                       cur_sco_step = j
                    j += 1
                cur_step = i
            i += 1
        print '!>sort ok'




from io import IO
from ICTCLAS50.Ictclas import Ictclas

cdef class UniSort:
    '''
    合并排序
    '''
    cdef:
        List l1,l2

    def __cinit__(self) :
        pass

    cdef void  init(self,List l1,List l2) :
        '''
        手动初始化
        '''
        self.l1 = l1
        self.l2 = l2

    cdef inline long __gvalue(Hit h) :
        '''
        取得值
        '''
        return h.wid

    def sort(self):
        '''
        排序
        '''
        cdef:
            int i = 0,j = 0

        #?????????????????
        while i<self.l1.length and j<self.l2.length:
            if self.l1.start[i] < self.l2.start[j]:  
                    
cdef class Hit_lists:
    '''
    对EACH_TEM_CONTAIN 个Hit_list内的hits进行管理
    达到一定量，保存为tem文件
    具体进行运行及其他操作
    '''
    cdef:
        #管理的Hit_list的数量
        int num
        #分词库
        object ict
        object io
        object file_docIDs
        Hit_list hitlist
        List **hit_bu_list
        
    

    def __cinit__(self) :
        '''
        init 
        '''
        self.io = IO() 
        self.hitlist = Hit_list() 
        self.thes = Thesaurus() 
        self.hitlist = Hitlist() 
        #为内存中保存 Hit_list中处理的hits分配指针空间
        self.ht_num = config.EACH_TEM_CONTAIN
        self.hit_bu_list = <List*>malloc(self.ht_num * sizeof(List*) )  


    cdef init(self,object file_docIDs) :
        '''
        手动初始化
        files:  传入list 
                一定数量的file
                文件名为具体的docID
        '''
        self.num = len(files) 
        self.file_docIDs = file_docIDs

    
        

    cdef run(self) :
        '''
        主程序运行
        '''
        self.init() 
        for hi,docID in enumerate( file_docIDs ):
            '''
            具体对每个文件操作
            '''
            #对于每一个文件
            #显式初始化 分配空间
            self.hitlist.init() 

            #传输过来一个标签的tag list
            tags = self.__get_file(docID) 

            for scoid,tag in enumerate(tags):
                '''
                根据scoid进行处理
                '''
                for text in enumerate( self.ict.split(tag).split()  ) :
                    '''
                    在标签内扫描
                    '''
                    for pos,c in self.ict.split(tag).split()  :
                        '''
                        每个tag内进行分词
                        '''
                        wid = self.thes.find(c) 
                    
                        if wid != 0:
                            '''
                            词在词库中可以查到
                            '''
                            if self.hitlist.Append( wid , docID , score , pos ) :
                                '''
                                添加成功
                                '''
                                pass

            #单个文件hitlist建立成功
            #加入Hitlists中综合处理
            self.hit_bu_list[hi] = self.hitlist.Get_hitlist() 
        #文件均处理完毕 需要保存为一个tem文件
        #先进行合并排序 合并成一个大文件
        #外排方法.....??????????????????????
        #???????????????????????????????????
        

        







    cdef __get_file(int docID) :
        '''
        根据docID取得文件内容
        需要对外接口的实现
        直接传送过来一个list  包含各个标签
        如：    [ ] 
        '''
        return self.io.get_file_by_docID(docID) 


    cdef char *__save_doc_name(self,char *inter) :
        '''
        返回合适的doc_name给 Save 将内存中的hitlist进行存储
        '''
        if inter == 'wid':
            '''
            根据wid排序的hitlist
            '''
            #????????????????????????????????????
            pass

        elif inter == 'did':
            '''
            根据did排序的hitlist
            '''
            #????????????????????????????????????
            pass




    cdef void Save(List hitlist , char *inter):
        '''
        将list进行存储
        存储结构：
            文件头：
                long        length
        '''
        cdef:
            char *fname
            FILE *fp

        if *inter == 'wid':
            '''
            根据wid进行排序
            '''
            fname = self.__save_doc_name('wid') 
            fp=<FILE *>fopen(fname,"ab")
            #存入length
            fwrite(self.hitlist.GetLength(),sizeof(long),1,fp) 
            #开始保存主要list内容
            fwrite(self.hitlist.Get_hitlist(),sizeof(Hit),self.hitlist.GetLength(),fp) 
            fclose(fp) 

#index.pyx
cdef class Sorter:
    '''
    快速排序主算法
    '''
    cdef void init(self,Hit *data,long length):
        '''
        init 手动初始化
        '''
        pass

    cdef inline double __gvalue(self,Hit data):
        '''
		返回需要进行比较的值
        '''
        pass

    cdef void quicksort(self,long p,int q):
        '''
        主程序
        '''
        pass


cdef class WidSort(Sorter):
    '''
    根据 wid 进行排序
    继承自 Sorter
    '''
    cdef void quicksort(self,long p,int q):
        '''
        主程序
        '''
        pass

cdef class DidSort(Sorter):
    '''
    根据 DocID 进行排序
    继承自 Sorter
    '''
    cdef void quicksort(self,long p,int q):
        '''
        主程序
        '''
        pass

cdef class ScoSort(Sorter):
    '''
    根据 score 进行排序
    继承自 Sorter
    '''
    cdef void quicksort(self,long p,int q):
        '''
        主程序
        '''
        pass

cdef struct List:
    Hit *start
    long length #此记录中的总hit数目  初始化时需要使用
    long space #分配空间

cdef class Hit_list:
    '''
    内存中单个hit队列的管理
    '''
    

