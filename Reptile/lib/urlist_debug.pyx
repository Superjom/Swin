from urlist cimport Urlist

cdef Urlist url=Urlist()
url.show()
cdef char* u1="http://www.cau.edu.cn"
uu='http://google.com'
for u in ['http://www.cau.edu.cn','http://www.google.com',\
'http://www.baidu.com']:

    if url.Find(u):
        print 'secceed finding %s'%u
    else:
        print '!>fail to find %s'%u
	
url.show()
url.dealloc()


