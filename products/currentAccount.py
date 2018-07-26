'''
Created on Jul 26, 2018

@author: radov
'''
from context.eventDomain import EventDomain
from context.configuration import Configuration

class CurrentAccount(object):
    '''
    - product_name
    - current_outstanding
    - cnit: current nominal interest rate
    - monthly_cost
    '''


    def __init__(self, ID, current_outstanding, cnit, monthly_cost, EventDomain):
        '''
        Constructor
        '''
        self.ID = ID
        self.current_outstanding = current_outstanding
        self.cnit = cnit
        self.monthly_cost = monthly_cost
        self.horizon = EventDomain.steps
        self.outstanding = dict()
        self.cumulativeCosts = dict()
        self.basisReturn = dict()
        self.effective_rate = (1 + self.cnit)**(1/12) - 1
        
    def deposit(self, amount, t):
        self.outstanding[t] = self.outstanding.get(t, 0) + amount
    
    def calculateOutstanding(self, t):
        if t == 0:
            self.outstanding[t] = self.outstanding.get(t,0) + self.current_outstanding
        else:
            self.outstanding[t] = self.outstanding.get(t,0) + self.outstanding[t-1]*(1+self.effective_rate) - self.monthly_cost
            
    def calculateCumulativeCosts(self, t):
        if t == 0:
            self.cumulativeCosts[t] = 0 + self.monthly_cost
        else:
            self.cumulativeCosts[t] = self.cumulativeCosts[t-1] + self.monthly_cost
            
    def calculateBasisReturn(self, t):
        if t == 0:
            self.basisReturn[t] = 0
        else:
            self.basisReturn[t] = (self.outstanding[t] - self.outstanding[0])/(self.outstanding[0] + Configuration.exp)        
        