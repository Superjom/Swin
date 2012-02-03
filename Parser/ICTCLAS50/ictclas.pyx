import ictclas
cdef class Ictclas:
    def __cinit__(self,basepath='./'):
        ictclas.ict_init(basepath)

    def __del__ (self):
        ictclas.ict_exit()

    cdef split(self,char *s):
        cdef:
            int length
            object li
            object str

        length=len(s)

        li=ictclas.process_str_ret_list(s,length,ictclas.eCodeType.UTF8)

        str=''
        for i in li:
            #print i.iStartPos
            str=str+s[i.iStartPos:(i.iStartPos+i.iLength)]+' '
        return str


