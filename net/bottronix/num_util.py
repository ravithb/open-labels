'''
Created on Feb 10, 2016

@author: ravith
'''

class NumUtil():
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    @staticmethod
    def to_lh_int(integer):
        integer = int(integer)
        lx = integer % 256
        hx = ( integer >> 8 ) & 0xFF
        return (hx,lx)