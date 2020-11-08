'''
Created on Jul 26, 2018

@author: radov
'''

class EventDomain:
    '''
    classdocs
    '''


    def __init__(self, life_expectancy, run_date):
        '''
        Constructor
        '''
        self.number_of_periods  = life_expectancy * 12
        self.steps              = range(0, self.number_of_periods)
        self.snapshot_date      = run_date
        
        
        
        