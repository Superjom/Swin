#定义 hashIndex 结构
cdef struct HI: #hashIndex 结构
    long left    #左侧范围
    long right   #右侧范围
