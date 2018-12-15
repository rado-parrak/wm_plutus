'''
Created on Jul 27, 2018

@author: radov
'''
import pandas as pd
import _pickle as pickle
from context.eventDomain import EventDomain
from context.instruments import AccountType
from resultObjects import *
from core.helpers import *
from context.behaviour import BehaviourLibrary, BehaviourScheme

class Calculator:
    '''
    classdocs
    '''
    def __init__(self, rredis, root_name):
        '''
        Constructor
        '''
        self.rredis = rredis
        
        # load the ROOT data file
        self.root = pickle.loads(self.rredis.get(root_name))    
        
        # initialize event domain
        for run in self.root['runs_config'].runs:
            run.appendEventDomain(EventDomain(run.life_expectancy, run.run_date))
        
        # create resultBase
        self.root['resultBase'] = ResultBase()

    def run(self):
        # 1) Run over all run_configs, scenarios, parties, instruments, steps
        for run in self.root['runs_config'].runs:
            for scenario in self.root['scenarios'].scenarios:
                for step in run.eventDomain.steps:
                    # i) first update the positions
                    for instrumentID in self.root['facts']['instruments'].keys():
                        instrument = self.root['facts']['instruments'][instrumentID] 
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
                       
                
                
                    # ii.) next simulate party actions based on these                
                    for party in self.root['facts']['parties']:
                        if self.root['resultBase'].getFromResultBasePartyResult(run.ID, scenario.ID, party.ID) == None: #create result object if doesn't exist
                            self.root['resultBase'].addToResultBasePartyResult(run.ID, scenario.ID, party.ID,  PartyLevelResultObject())
                                
                        resultObject = self.root['resultBase'].getFromResultBasePartyResult(run.ID, scenario.ID,party.ID)
                        
                        ## I) --- INCOME ACCOUNT ---
                        # i) calculate realized income (wage + capital income + inheritance + pension)                        
                        # grossWage
                        grossWage = party.calculateGrossWage(step, resultObject)
                        resultObject.updateGrossWage(grossWage, step)                    
                        
                        # ii) calculate unrealized income (capital gain/loss)
                        
                        # iii) capital redemptions
                        
                        # z) update income account
                        resultObject.updateIncomeAccount(grossWage, step)
                        
                        ## II) --- EXPENDITURE ACCOUNT (+ PENSION ACCOUNT) --- 
                        # i) Taxes
                        incomeTax = party.calculateIncomeTax(grossWage)
                        resultObject.updateIncomeTax(incomeTax, step)
                        
                        # ii) Social + Welfare
                        
                        # iii) Pension contribution
                        
                        # iv) Fees
                        
                        # v) Housing / renting
                        
                        # vi) Other monthly consumption
                        
                        # z) expenditure account
                        resultObject.updateExpenditureAccount(incomeTax, step)
                        
                        ## III) --- NET CASH BALANCE ---
                        resultObject.updateNetCashBalance(resultObject.incomeAccount[step] - resultObject.expenditureAccount[step], step)
                        
                        ## IV) --- ACTION ---
                        # i) allocate the netCashBalance to savings / investments / cash
                        # TODO: currently the behaviour scheme is hardcoded, should become an input parameter...
                        allocationInputParameters = party.prepareAllocationInputs(BehaviourScheme.STATIC_SHARES_BEST_RETURN, self.root, resultObject, party.ID, step)
                        allocatedQuantities = party.allocate(BehaviourScheme.STATIC_SHARES_BEST_RETURN, **allocationInputParameters)                                
                        
                        ## add to result base                        
                        self.root['resultBase'].addToResultBasePartyResult(run.ID, scenario.ID, party.ID, resultObject)
                        
        
        # save the root
        self.rredis.set('root', pickle.dumps(self.root))         
        return(None)
   
            