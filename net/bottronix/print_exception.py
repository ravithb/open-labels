'''
Created on Feb 11, 2016

@author: ravith
'''

class PrintException(Exception):
    '''
    classdocs
    '''


    def __init__(self, value):
        '''
        Constructor
        '''
        self.value = value

    def __str__(self):
        return repr(self.value)