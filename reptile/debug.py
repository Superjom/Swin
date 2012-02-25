# -*- coding: utf-8 -*-

def conheader(name):
    '''
    分割单个类到开头
    '''
    print '#'*40
    print '('*4,
    print name,
    print ')'*4

def console(func, strr=""):
        '''
        输出： 
            ---------------------------------
            <<<func>>> strr
            ---------------------------------
        '''
        print '--------------------------------'
        print '<<<%s>>> %s' % (func, strr)

WIDTH = 60
def hr():
    print '-' * WIDTH
