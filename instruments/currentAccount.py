'''
Created on Jul 26, 2018

@author: radov
'''
from context.configuration import Configuration

class CurrentAccount(object):
    '''
    - product_name
    - current_outstanding
    - cnit: current nominal interest rate
    - monthly_cost
    '''


    def __init__(self, ID, name, current_outstanding, cnit, monthly_cost):
        '''
        Constructor
        '''
        self.ID = ID
        self.name = name
        self.current_outstanding = current_outstanding
        self.cnit = cnit
        self.monthly_cost = monthly_cost
        self.cumulativeCosts = dict()
        self.basisReturn = dict()
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
    
    
    def calculateIncome(self, scenario, t, resultBase):
        return(None)
    
    def calculateExpenses(self, scenario, t, resultBase):
        return(None)
    
    def calculateInvestments(self, scenario, t, resultBase):
        return(None)
    
    def calculateSavings(self, scenario, t, resultBase):
        return(None)
    
    
    
    