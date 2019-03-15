'''
Created on Sep 26, 2018

@author: radov
'''

class Scenarios:
    '''
    classdocs
    '''
    
    def __init__(self, scenarios_source_data):
        '''
        Constructor
        '''
        self.scenarios = list()
        for s in scenarios_source_data:            
            self.scenarios.append(Scenario(s['ID'], s['name']))

class Scenario:
    def __init__(self
                 , ID
                 , name):
        
        self.ID = ID
        self.name = name