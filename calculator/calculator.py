'''
Created on Jul 27, 2018

@author: radov
'''
import pandas as pd
import json
from core import resultBasedServices as rbs

class Calculator(object):
    '''
    classdocs
    '''


    def __init__(self, party, context, behaviour, redis):
        '''
        Constructor
        '''
        self.party = party
        self.context = context
        self.behaviour = behaviour
    
    '''    
    def projectPortfolioWeights(self):
        self.portfolio_weights = dict()
        self.portfolio_weights['scenario']      = []
        self.portfolio_weights['month']         = []
        self.portfolio_weights['product_name']  = [] 
        self.portfolio_weights['weight']        = []
        
        
        for scenario in self.behaviour.scenarios:
            for share in scenario.portfolio_shares:
                    for t in self.context.eventDomain.steps:
                
                self.portfolio_weights['scenario']  
                
                
                = self.behaviour[behaviour_id].product['portfolio_weights']
            
        return(pd.DataFrame())
    '''    
    
    def calculateOutstandings(self):
        # fetch resultBase
        resultBase = json.loads(self.redis.get('resultBase'))
        
        # do the actual calculation               
        for scenario in self.behaviour.scenarios:
            for step in self.context.eventDomain.steps:
                for instrument in self.party.portfolio.instruments:                    
                    # calculate the outstanding
                    outstanding = instrument.calculateOutstanding(scenario, step, resultBase)
                    # update resultBase
                    resultBase = rbs.addOutstandingToResultBase(resultBase, scenario, step, instrument, outstanding)
        # store the serialized resultBase to Redis
        self.redis.set('resultBase', json.dumps(resultBase))
        