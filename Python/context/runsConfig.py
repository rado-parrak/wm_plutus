'''
Created on Oct 4, 2018

@author: radov
'''
from context.eventDomain import EventDomain

class RunsConfig:
    '''
    classdocs
    '''
    def __init__(self, runsConfig_source_data):
        '''
        Constructor
        '''
        self.runs = list()        
        for rc in runsConfig_source_data:
            self.runs.append(RunConfig(rc['ID']
                                 , rc['name']
                                 , rc['run_date']
                                 , rc['life_expectancy']))    
    
class RunConfig:
    
    def __init__(self, ID, name, run_date, life_expectancy):
        '''
        Constructor
        '''
        self.ID         = ID
        self.name       = name
        self.run_date   = run_date
        self.life_expectancy = life_expectancy
        
    def appendEventDomain(self, eventDomain: EventDomain):
        self.eventDomain = eventDomain
        