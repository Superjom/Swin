from libc.stdio cimport fopen,fclose,fwrite,FILE,fread
from libc.stdlib cimport malloc,free

import sys
sys.path.append('../') 
import config


DEF TRUE=	1
DEF	FALSE=	-1

DEF INIT_LENGTH=500
DEF PER_ADD_LENGTH=100

cdef class Create_Thesaurus:

    '''
    新建词库
    类似于urlist的相关方法
    if has_this_word:
        return True
    else
        enter_this_word
    '''
    cdef:
        #word 指针数组 每个*wlist为一个词
        char **wlist
        #词数目
        long length
        #分配的空间大小
        long space

    def __cinit__(self) :
        '''
        init
        分配初始化的空间
        '''
        self.wlist = <char**>malloc(sizeof(INIT_LENGTH) * sizeof(char *)  )  
        self.length = 0
        self.space = INIT_LENGTH

    def __dealloc__(self) :
        '''
        自动释放C空间
        '''
        print '!>delete all C space'
        free(self.wlist) 

    cdef inline int __AddSpace(): 
        '''
        分配空间过小
        需要另外添加空间
        '''
        cdef:
            char **base
        base = <char**>realloc(self.wlist,sizeof(self.space+PER_ADD_LENGTH) * sizeof(char *)  )  
        if not base:
            print 'Fail to AddSpace'
            return FALSE
        #相关更改
        self.wlist = base
        self.space += PER_ADD_LENGTH

        return TRUE

    cdef int  Insert(self,int i,char *u) :
        '''
        在元素插入到序号为i的位置
        '''
        if i>self.length or i<0:
            '''
            越界错误
            '''
            print 'i 越界'
            return FALSE

        if self.length+1 > self.space:
            '''
            超出空间
            '''
            if self.__AddSpace() == FALSE:
                print '空间增加失败'
                return FALSE
            #开始插入
            cdef:
                int j = self.length

            while(j>i):
                '''
                移动元素
                '''
                self.wlist[j] = self.wlist[j-1] 
                j -= 1

            self.wlist[i] = u
            self.length += 1
            return TRUE


    def show(self):
        '''
        展示内容
        '''
        print '!>begin to show content of list'
        print '!>status:    length:%d     maxlength:%d  '%(self.length,self.space)

        cdef:
            int i

        i=0
        for i in range(self.length):
            print i,self.wlist[i]


    cdef int find(self,char *word):
        '''
        查找和插入
        外在接口
        '''
        cdef:
            int l=self.length
            int first=0
            int end=l-1
            int mid=0
            long uh=hash(word)

        print '!>find:%s'%url
    
        if l==0:
            '''
            长度为0 首次插入
            '''
            self.Insert(0,url)
            return FALSE

        while first < end:  
            mid = (first + end)/2  

            if url> hash( self.wlist[mid]):
                first = mid + 1  

            elif url < hash( self.wlist[mid]):
                end = mid - 1  

            else:  
                break  
            
        if first == end:  
            if hash(self.wlist[first]) > uh:  
                '''
                小
                '''
                self.Insert(first, word ) 
                return FALSE 
            
            elif hash(self.wlist[first])< uh:  
                '''
                大
                '''
                self.Insert(first + 1, word)  
                return FALSE
            
            else:  
                '''
                等
                '''
                return TRUE
                
        elif first > end:  
            self.Insert(first, word) 
            return FALSE
        else:  
            return TRUE 

    cdef char *get_str(self):
        '''
        取得以空格分割的词库字符串
        '''
        cdef:
            char *strr = ''
        for i in range(self.length) :
            strr += self.wlist[i] + ' '
        return strr

    cdef void save(self):
        '''
        将词库以字符串方式保存
        '''
        print 'begin save thes'
        f=fopen(config.THES_PH,'w') 
        f.write( self.get_str()  ) 
        f.close() 


#创建索引表数据结构
cdef struct HI:
    long left
    long right


cdef class Init_thesaurus:
    '''
    初始化词库
    '''
    cdef:
        #词库数据
        char ** wlist
        long length
        #索引
        HI hashIndex[config.HI_STEP] 
        #最小和最大的词 hash值
        long left
        long right
        
    def __cinit__(self):
        '''
        init 
        从文件中读取相关词典文件 初始化为词典文件
        '''
        cdef:
            char **base

        f = open(config.THES_PH,'r') 
        strr = f.read() 
        f.close() 
        words = strr.split() 
        self.length = len(words) 

        print '!>读取词库文件\n得到 %d 个词'%self.length

        base = <char **> malloc(sizeof(char *) * self.length ) 
        if not base:
            print '分配内存失败'
            return FALSE

        self.wlist = base
        
        print '开始产生词库'
        for i in range(self.length):
            '''
            生成词库
            '''
            self.wlist[i] = words[i] 

    def __dealloc__(self) :
        '''
        释放C空间
        '''
        print '释放C空间'
        free(self.wlist) 

    cdef int __hash_find(self,double data) :
        '''
        查找不大于一hash值的最大word的下标位置
        '''
        cdef:
            int i

        for i,w in enumerate(self.wlist) :
            if hash(w) > data:
                return i-1
        #最后一个词汇
        return len(self.wlist)-1

    cdef void show_hash(self) :
        '''
        展示hash值
        '''
        cdef:
            int i
        print '!> the hash index %d is:'%config.HI_STEP

        for i in range(config.HI_STEP) :
            print '[%d %d]'%( self.hashIndex[i].left ,self.hashIndex[i].right)
        print '\n'+'-'*50

    cdef create_hash_index(self) :
        '''
        产生hash 索引
        '''
        cdef:
            #左右边界
            long left = hash(self.wlist[0] ) 
            long right = hash(self.wlist[-1] ) 
            #中间步长的平均跨度
            long step = <double> (right - left) / config.HI_STEP 
            long minidx = left
            int cur_step = 0
            int i

        #将模块本身hash范围作定义
        self.left = left
        self.right = right

        print '!>begin to create hashindex'

        for i in range(config.HI_STEP ) :
            '''
            为每一步建立索引
            '''
            minidx += step
            self.hashIndex[i].left = cur_step+1 
            self.hashIndex[i].right =  self.__hash_find(minidx) 
            cur_step = self.hashIndex[i].right 

            print 'minidx: %d  left: %d  right: %d'%(minidx,self.hashIndex[i].left,self.hashIndex[i].right) 

    cdef int __pos_hash(self,long hashvalue) :
        '''
        通过hashvalue 确定其对应的hashvalue区间下标
        '''
        cdef:
            long cur = -1


        cdef double step=<double>( (self.right-self.left)/STEP )
        return <long>int((hashvalue-self.left)/step)

    def find(self,word):

        '''
        具体查取值 
        若存在 返回位置 
        若不存在 返回   0
        '''
        #print 'want to find ',hash(data),data
        cdef:
            long l
            long fir
            long mid
            long end
            long pos
            HI cur  #范围

        #print '初始化数据ok'

        dv = hash(word)      #传入词的hash

        pos=self.__pos_hash( dv )

        #print '开始 pos',pos

        if pos!=-1 and pos<STEP:
            #print '开始>cur=self.hashIndex.hi[pos]',pos
            cur=self.hashIndex[pos]
            #print 'cur< OK ',cur.left,cur.right

        else:
            print "the word is not in wordbar or pos wrong"
            return FALSE

        #取得 hash 的一级推荐范围
        fir=cur.left
        end=cur.right
        mid=fir

        if dv > hash(self.word_list[end]):
            return 0

        #print '词库: fir,end,mid',fir,end,mid

        while fir<end:

            #print 'in wordbar while'
            #print 'dv',dv

            mid=(fir+ end)/2
            #print 'mid',mid

            if ( dv > hash(self.word_list[mid]) ):
                fir = mid + 1
                #print '1 if fir',fir

            elif  dv < hash(self.word_list[mid]) :
                end = mid - 1
                #print '1 elif end',end

            else:
                break

        if fir == end:
            
            #print 'fir==end'

            if hash(self.word_list[fir]) > dv:
                return 0 

            elif (self.word_list[fir]) < dv:
                return 0

            else:
                #print 'return fir,mid,end',fir,mid,end
                #print '查得 wordid',end
                return end#需要测试
                
        elif fir>end:
            return 0

        else:
            #print '1return fir,mid,end',fir,mid,end
            #print '查得 wordid',mid
            return mid#需要测试


