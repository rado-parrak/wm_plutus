'''
Created on Oct 4, 2018

@author: radov
'''
from enum import Enum

class InstrumentType(Enum):
    CURRENT_ACCOUNT = 1

class Instrument:
    '''
    classdocs
    '''
    def __init__(self, ID, name, current_outstanding, monthly_cost):
        '''
        Constructor
        '''
        self.ID = ID
        self.name = name
        self.current_outstanding = current_outstanding
        self.monthly_cost = monthly_cost
        

class CurrentAccount(Instrument):
    '''
    classdocs
    '''
    def __init__(self, ID, name, current_outstanding, monthly_cost, cnit):
        '''
        Constructor
        '''
        self.cnit = cnit
        self.effective_rate = (1 + self.cnit)**(1/12) - 1
        
    def deposit(self, amount, t):
        self.outstanding[t] = self.outstanding.get(t, 0) + amount
    
    def calculateOutstanding(self, scenario, t, resultBase):
        if t == 0:
            outstanding = self.current_outstanding
        else:
            if resultBase[scenario.ID][self.ID][t-1] == None:
                raise Exception('Element in the resultBase not found!')
            else:
                lastOutstanding = resultBase[scenario.ID][self.ID][t-1]
                outstanding = lastOutstanding*(1+self.effective_rate) - self.monthly_cost
        return(outstanding)

        

    
    