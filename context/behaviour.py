'''
Created on Jul 26, 2018

@author: radov
'''
class Behaviours:
    '''
    classdocs
    '''
        
    def __init__(self, behaviours_source_data):
        '''
        Constructor
        '''
        self.behaviours = list()
        for b in behaviours_source_data:            
            self.behaviours.append(Behaviour(b['ID']
                                             , b['name']
                                             , b['saving_allocation_weight']
                                             , b['investment_allocation_weight']
                                             , b['cash_allocation_weight']
                                             , b['instrument_shares']))
            
class Behaviour:
    def __init__(self
                 , ID
                 , name
                 , saving_allocation_weight
                 , investment_allocation_weight
                 , cash_allocation_weight
                 , instrument_shares):
        
        self.ID = ID
        self.name = name
        self.saving_allocation_weight = saving_allocation_weight
        self.investment_allocation_weight = investment_allocation_weight
        self.cash_allocation_weight = cash_allocation_weight
        self.instrument_shares = instrument_shares