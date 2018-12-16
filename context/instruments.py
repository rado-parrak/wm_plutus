'''
Created on Oct 4, 2018

@author: radov
'''
from enum import Enum
from resultObjects import InstrumentLevelResultObject 

class InstrumentType(Enum):
    CURRENT_ACCOUNT = 1
    SAVING_ACCOUNT = 2
    
class InstrumentClass(Enum):
    CASH_BALANCE = 1
    SAVING = 2
    INVESTMENT = 3
    
class AccountType(Enum):
    ASSET = 1
    LIABILITY = 2

class Instrument:
    '''
    classdocs
    '''
    def __init__(self, ID, name, current_outstanding, monthly_cost, account_type, instrument_class):
        '''
        Constructor
        '''
        self.ID = ID
        self.name = name
        self.current_outstanding = current_outstanding
        self.monthly_cost = monthly_cost
        self.account_type = account_type
        self.instrument_class = instrument_class
        
    def calculateCurrentValue(self, step, previous_results: InstrumentLevelResultObject):
        return(None)
        

class CurrentAccount(Instrument):
    '''
    classdocs
    '''
    def __init__(self, ID, name, current_outstanding, monthly_cost, account_type, instrument_class, cnit):
        '''
        Constructor
        '''
        super().__init__(ID, name, current_outstanding, monthly_cost, account_type, instrument_class)
        self.cnit = cnit
        self.effective_rate = (1 + self.cnit)**(1/12) - 1
        
    def calculateCurrentValue(self, step, previous_results: InstrumentLevelResultObject):
        super().calculateCurrentValue(step, previous_results)
        
        if step == 0:
            currentValue = self.current_outstanding
        else:
            if previous_results.currentValue[step-1] == None:
                raise Exception('Element in the resultBase not found!')
            else:
                lastOutstanding = previous_results.currentValue[step-1]
                currentValue = lastOutstanding*(1+self.effective_rate) - self.monthly_cost
        return(currentValue)    

class SavingAccount(Instrument):
    '''
    classdocs
    '''
    def __init__(self, ID, name, current_outstanding, monthly_cost, account_type, instrument_class, cnit):
        '''
        Constructor
        '''
        super().__init__(ID, name, current_outstanding, monthly_cost, account_type, instrument_class)
        self.cnit = cnit
        self.effective_rate = (1 + self.cnit)**(1/12) - 1
        
    def calculateCurrentValue(self, step, previous_results: InstrumentLevelResultObject):
        super().calculateCurrentValue(step, previous_results)
        
        if step == 0:
            currentValue = self.current_outstanding
        else:
            if previous_results.currentValue[step-1] == None:
                raise Exception('Element in the resultBase not found!')
            else:
                lastOutstanding = previous_results.currentValue[step-1]
                currentValue = lastOutstanding*(1+self.effective_rate) - self.monthly_cost
        return(currentValue)        

    
    