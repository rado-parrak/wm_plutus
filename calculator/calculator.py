'''
Created on Jul 27, 2018

@author: radov
'''
import pandas as pd

class Calculator(object):
    '''
    classdocs
    '''


    def __init__(self, joe, context, behaviour):
        '''
        Constructor
        '''
        self.joe = joe
        self.context = context
        self.behaviour = behaviour
        
    def projectPortfolioWeights(self, behaviour_id):
        self.portfolio_weights = dict()
        for t in self.context.eventDomain.steps:
            self.portfolio_weights[t] = self.behaviour[behaviour_id].product['portfolio_weights']
            
        return(pd.Dataframe(self.portfolio_weights))
        
        
    def calculateOutstandings(self):
        return(None)
        