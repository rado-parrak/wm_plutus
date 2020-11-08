'''
Created on Oct 5, 2018

@author: radov
'''
class InstrumentLevelResultObject:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        self.currentValue   = dict()
        self.netIncome      = dict()
    
    def updateCurrentValue(self,delta, step):
        if not bool(self.currentValue): # when the dict is empty
            self.currentValue[step] = delta
        elif step in self.currentValue.keys():
            self.currentValue[step] = self.currentValue[step] + delta
        else:
            self.currentValue[step] = delta
            
    def updateNetIncome(self,netIncome, step):
        self.currentValue[step] = netIncome

class PartyLevelResultObject:
    '''
    classdocs
    '''

    def __init__(self):
        '''
        Constructor
        '''
        
        # accounts
        self.incomeAccount = dict()
        self.expenditureAccount = dict()
        self.netCashBalance = dict()
        
        # increments
        self.grossWage      = dict()
        self.capitalIncome  = dict()
        self.inheritance    = dict()
        self.pension        = dict()
        self.incomeTax      = dict()
        
    def updateGrossWage(self, delta, step):
        if not bool(self.grossWage): # when the dict is empty
            self.grossWage[step] = delta
        elif step in self.grossWage.keys():
            self.grossWage[step] = self.grossWage[step] + delta
        else:
            self.grossWage[step] = delta
            
    def updateIncomeAccount(self, delta, step):
        if not bool(self.incomeAccount): # when the dict is empty
            self.incomeAccount[step] = delta
        elif step in self.incomeAccount.keys():
            self.incomeAccount[step] = self.incomeAccount[step] + delta
        else:
            self.incomeAccount[step] = delta
            
    def updateIncomeTax(self, delta, step):
        if not bool(self.incomeTax): # when the dict is empty
            self.incomeTax[step] = delta
        elif step in self.incomeTax.keys():
            self.incomeTax[step] = self.incomeTax[step] + delta
        else:
            self.incomeTax[step] = delta
            
    def updateExpenditureAccount(self, delta, step):
        if not bool(self.expenditureAccount): # when the dict is empty
            self.expenditureAccount[step] = delta
        elif step in self.expenditureAccount.keys():
            self.expenditureAccount[step] = self.expenditureAccount[step] + delta
        else:
            self.expenditureAccount[step] = delta
            
    def updateNetCashBalance(self, delta, step):
        if not bool(self.netCashBalance): # when the dict is empty
            self.netCashBalance[step] = delta
        elif step in self.netCashBalance.keys():
            self.netCashBalance[step] = self.netCashBalance[step] + delta
        else:
            self.netCashBalance[step] = delta    

class ResultBase(dict):
    def __init__(self):
        
        self['runs'] = dict()
        
    def addToResultBaseInstrumentResult(self, runID, scenarioID, instrumentID, instrumentResult: InstrumentLevelResultObject): 
        if self['runs'].get(runID,None) == None:
            self['runs'][runID] = dict()
            self['runs'][runID]['scenarios'] = dict()
        if self['runs'][runID]['scenarios'].get(scenarioID, None) == None:
            self['runs'][runID]['scenarios'][scenarioID] = dict()
            self['runs'][runID]['scenarios'][scenarioID]['instruments'] = dict()
        if self['runs'][runID]['scenarios'][scenarioID]['instruments'].get(instrumentID,None) == None:
            self['runs'][runID]['scenarios'][scenarioID]['instruments'][instrumentID] = instrumentResult
        
        return(self)
    
    def getFromResultBaseInstrumentResult(self, runID, scenarioID, instrumentID):
        ret = None
        if self['runs'].get(runID,None) != None:
            if self['runs'].get(runID,None)['scenarios'].get(scenarioID, None) != None:
                if self['runs'].get(runID,None)['scenarios'].get(scenarioID, None)['instruments'].get(instrumentID,None) != None:
                    ret = self['runs'].get(runID,None)['scenarios'].get(scenarioID, None)['instruments'].get(instrumentID,None)
        return(ret)

    def addToResultBasePartyResult(self, runID, scenarioID, partyID, partyResult: PartyLevelResultObject): 
        if self['runs'].get(runID,None) == None:
            self['runs'][runID] = dict()
            self['runs'][runID]['scenarios'] = dict()
        if self['runs'][runID]['scenarios'].get(scenarioID, None) == None:
            self['runs'][runID]['scenarios'][scenarioID] = dict()
        if self['runs'][runID]['scenarios'][scenarioID].get('parties', None) == None:
            self['runs'][runID]['scenarios'][scenarioID]['parties'] = dict()
        if self['runs'][runID]['scenarios'][scenarioID]['parties'].get(partyID,None) == None:
            self['runs'][runID]['scenarios'][scenarioID]['parties'][partyID] = partyResult
        
        return(self)
    
    def getFromResultBasePartyResult(self, runID, scenarioID, partyID):
        ret = None
        if self['runs'].get(runID,None) != None:
            if self['runs'][runID]['scenarios'].get(scenarioID, None) != None:
                if self['runs'][runID]['scenarios'][scenarioID].get('parties', None) != None:
                    if self['runs'][runID]['scenarios'][scenarioID]['parties'].get(partyID,None) != None:
                        ret = self['runs'][runID]['scenarios'][scenarioID]['parties'][partyID]
        return(ret)

