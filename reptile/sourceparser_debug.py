# -*- coding: utf-8 -*-
from sourceparser import *

class PicParser_debug:
    def __init__(self):
        self.pp = PicParser()

    def compresspic(self):
        f = open('./dog.jpg','rb')
        c = f.read()
        f.close()
        self.pp.init(c)
        print 'begin to compress pic'
        res = self.pp.compressedPic(c)
        f = open('cat.jpg','w')
        f.write(res['source'])
        f.close()

if __name__ == '__main__':
    pp = PicParser_debug()
    pp.compresspic()
