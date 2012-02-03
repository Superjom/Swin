cdef struct HI:
    long left
    long right

cdef class StaticList:
    '''
    静态查询list
    可使用hashindex加速查询
    默认对字符串的查询
    '''
    cdef:
        #字符串的数据
        char **dlist
        long length
        #索引 需要动态分配空间
        HI *hashIndex
        #最大 最小 hash  
        long left
        long right 
        #hashIndex 分块数
        int step

    def __cinit__(self, int step) :
        '''
        init
        '''
        #分配list初始化空间
        self.__init_list() 
        self.step = step
        #分配hashindex空间
        self.__init_hash_space() 

    def __dealloc__(self) :
        '''
        释放C空间
        '''
        free(self.dlist) 

    cdef inline void __init_list(self):
        '''
        分配list初始化空间
        将数据list初始化完毕
        '''
        pass

    cdef inline void __init_hash_space(self) :
        '''
        分配hashindex空间
        '''
        self.hashIndex = <HI *>malloc(step * sizeof(HI) )  
    cdef inline __v(self,char *data) :
        '''
        data的判断值
        '''
        return hash(data) 
    cdef int __hash_find(self,double data) :
        '''
        查找不大于一hash值的最大word的下标位置
        '''
        cdef:
            int i

        for i,w in enumerate(self.dlist) :
            if self.__v(w) > data:
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
            long left = self.__v(self.wlist[0] ) 
            long right = self.__v(self.wlist[-1] ) 
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

        dv = self.__v(word)      #传入词的hash

        pos=self.__pos_hash( dv )

        #print '开始 pos',pos

        if pos!=-1 and pos<STEP:
            #print '开始>cur=self.hashIndex.hi[pos]',pos
            cur=self.hashIndex[pos]
            #print 'cur< OK ',cur.left,cur.right

        else:
            print "the word is not in wordbar or pos wrong"
            return False

        #取得 hash 的一级推荐范围
        fir=cur.left
        end=cur.right
        mid=fir
        #print 'length',self.length

        #print 'trying ...',

        #print self.v(self.word_list[fir])

        #print 'the fir end gv',self.v(self.word_list[fir]),self.v(self.word_list[end]),dv

        if dv > self.__v(self.word_list[end]):
            return 0

        #print '词库: fir,end,mid',fir,end,mid

        while fir<end:

            #print 'in wordbar while'
            #print 'dv',dv

            mid=(fir+ end)/2
            #print 'mid',mid

            if ( dv > self.__v(self.word_list[mid]) ):
                fir = mid + 1
                #print '1 if fir',fir

            elif  dv < self.__v(self.word_list[mid]) :
                end = mid - 1
                #print '1 elif end',end

            else:
                break

        if fir == end:
            
            #print 'fir==end'

            if self.__v(self.word_list[fir]) > dv:
                return 0 

            elif self.__v(self.word_list[fir]) < dv:
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







