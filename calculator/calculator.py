'''
Created on Jul 27, 2018

@author: radov
'''
import pandas as pd

class Calculator(object):
    '''
    classdocs
    '''


    def __init__(self, party, context, behaviour):
        '''
        Constructor
        '''
        self.party = party
        self.context = context
        self.behaviour = behaviour
        
    def projectPortfolioWeights(self):
        self.portfolio_weights = dict()
        self.portfolio_weights['scenario']      = []
        self.portfolio_weights['month']         = []
        self.portfolio_weights['product_name']  = [] 
        self.portfolio_weights['weight']        = []
        
        
        for scenario in self.behaviour.scenarios:
            for t in self.context.eventDomain.steps:
                for prod in self.
                self.portfolio_weights['scenario']  
                
                
                = self.behaviour[behaviour_id].product['portfolio_weights']
            
        return(pd.DataFrame())
        
    '''    
    def calculateOutstandings(self, behaviour_id):
        for t in self.context.eventDomain.steps:
            for product in self.party.portfolio.products:
               Scheduler.runSchedule(t, product, behaviour_id)
        
        return(None)
    '''    