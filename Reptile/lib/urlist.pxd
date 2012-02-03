from libc.stdlib cimport realloc,malloc,free

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
    cdef UrlList urlist
	
    cdef void dealloc(self)
    cdef int Insert(self,int i,char *u)
	
    cdef int AddSpace(self)

    cdef int MinusSpace(self)

    cdef int Find(self,url)

    cdef char* return_urls_str(self,Flock)

    cdef int get_list_length(self)
