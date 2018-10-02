'''
Created on Jul 27, 2018

@author: radov
'''
import pandas as pd
import json
import core.resultBaseServices as rbs

class Calculator(object):
    '''
    classdocs
    '''


    def __init__(self, party, context, behaviour, rredis):
        '''
        Constructor
        '''
        self.party = party
        self.context = context
        self.behaviour = behaviour
        self.rredis = rredis
    
    
    def calculateOutstandings(self):
        # fetch resultBase
        resultBase = json.loads(self.rredis.get('resultBase'))
        
        # do the actual calculation               
        for scenario in self.behaviour.scenarios:
            for instrument in self.party.portfolio.instruments:
                for step in self.context.eventDomain.steps:
                    # calculate the outstanding
                    outstanding = instrument.calculateOutstanding(scenario, step, resultBase)
                    # update resultBase
                    resultBase = rbs.addOutstandingToResultBase(resultBase, scenario, instrument, step, outstanding)
        # store the serialized resultBase to Redis
        self.rredis.set('resultBase', json.dumps(resultBase))
        