'''
Created on Jul 26, 2018

@author: radov
'''

class EventDomain:
    '''
    classdocs
    '''


    def __init__(self, config_source_data):
        '''
        Constructor
        '''
        self.number_of_periods  = config_source_data['eventDomain']['number_of_periods']
        self.steps              = range(0, self.number_of_periods)
        self.snapshot_date      = config_source_data['eventDomain']['snapshot_date']
        
        
        
        