'''
Created on Jul 26, 2018

@author: radov
'''

class EventDomain(object):
    '''
    classdocs
    '''


    def __init__(self, number_of_periods):
        '''
        Constructor
        '''
        self.number_of_periods = number_of_periods
        self.steps = range(0, self.number_of_periods)
        
        
        
        