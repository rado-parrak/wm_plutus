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
    
    
    def projectOutstandings(self):
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
        
    def projectIncome(self):
        # fetch resultBase
        resultBase = json.loads(self.rredis.get('resultBase'))
        
        # do the actual calculation               
        for scenario in self.behaviour.scenarios:
            for step in self.context.eventDomain.steps:
                # wage
                wage        = self.calculateWage(scenario, step)
                resultBase = rbs.addIncomeToResultBase(resultBase, scenario, step, wage, 'wage')
                # capital income
                for instrument in self.party.portfolio.instruments:
                    capital_income = self.calculateCapitalIncome(scenario, instrument, step)
                    resultBase = rbs.addIncomeToResultBase(resultBase, scenario, step, capital_income, 'capital_income')
                # inheritance
                
                # pension savings
                
        # store the serialized resultBase to Redis
        self.rredis.set('resultBase', json.dumps(resultBase))
    
    def projectExpenses(self):
        return(None)
    
    def projectInvestments(self):
        return(None)
    
    def projectSavings(self):
        return(None)
    
    def calculateWage(self, scenario, step):
        return(self.party.monthly_income)
    
    def calculateCapitalIncome(self, scenario, instrument, step):
        return(self.party.monthly_income)
            
            