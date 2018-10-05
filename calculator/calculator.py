'''
Created on Jul 27, 2018

@author: radov
'''
import pandas as pd
import _pickle as pickle
from context.eventDomain import EventDomain
from context.instruments import AccountType
from resultObjects import *

class Calculator:
    '''
    classdocs
    '''
    def __init__(self, rredis, root_name):
        '''
        Constructor
        '''
        # load the ROOT data file
        self.root = pickle.loads(rredis.get(root_name))    
        
        # initialize event domain
        for run in self.root['runs_config'].runs:
            run.appendEventDomain(EventDomain(run.life_expectancy, run.run_date))
        
        # create resultBase
        self.root['resultBase'] = ResultBase()

    def run(self):
        # 1) Run over all run_configs, scenarios, instruments, steps
        for run in self.root['runs_config'].runs:
            for scenario in self.root['scenarios'].scenarios:
                for instrument in self.root['facts']['instruments']:
                    for step in run.eventDomain.steps:
                        # i) Value Assets:
                        if instrument.account_type == AccountType.ASSET:
                            if self.root['resultBase'].getFromResultBaseInstrumentResult(run.ID, scenario.ID, instrument.ID) == None: #create result object if doesn't exist
                                self.root['resultBase'].addToResultBaseInstrumentResult(run.ID, scenario.ID, instrument.ID,  InstrumentLevelResultObject())
                            
                            resultObject = self.root['resultBase'].getFromResultBaseInstrumentResult(run.ID, scenario.ID,instrument.ID)
                            
                            # calculate the asset value and update
                            currentValue = instrument.calculateCurrentValue(step, resultObject)
                            resultObject = resultObject.updateCurrentValue(currentValue, step)                               
                            
                            # store back to resultBase    
                            self.root['resultBase'].addToResultBaseInstrumentResult(run.ID, scenario.ID, instrument.ID, resultObject)
                        
                        # ii) Value Liabilities:
                        
                        
                        # iii) Net Position
                        
                        
                        # iv) Net Income
        
        
                        
        
        # 2) Run over all scenarios, parties, steps
        
        
        
        return(None)
    

'''
    def projectOutstandings(self):
        # do the actual calculation               
        for scenario in self.behaviour.scenarios:
            for instrument in self.party.portfolio.instruments:
                for step in self.context.eventDomain.steps:
                    # calculate the outstanding
                    outstanding = instrument.calculateOutstanding(scenario, step, resultBase)
                    # update resultBase
                    resultBase = rbs.addOutstandingToResultBase(resultBase, scenario, instrument, step, outstanding)
 
        
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
 '''           
            