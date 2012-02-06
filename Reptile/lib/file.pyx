#############################################
#    Date:       2012-02-5 
#    Project:    File 
#    @Author:    Chunwei
#############################################
import Image

cdef class File:
    '''
    对下载的各种文件进行处理
    picture:
    doc:
    docx:
    pdf:
    html:
    处理完的数据都会存储到数据库中
    可以作为对外界数据的处理
    '''
    def __cinit__(self):
        pass

    def __html(self):
        '''
        对html的处理
        '''
        pass

    def __pic(self):
        '''
        对pic的处理
        主要为转化格式 建立名称 压缩存储到数据库
        处理完毕返回在数据库中的id号码
        '''


    def __pdf(self):
        '''
        对pdf的处理
        '''
        pass

    def __word(self):
        '''
        对word的处理
        '''
        pass






