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
    
    def updateCurrentValue(self,currentValue, step):
        self.currentValue[step] = currentValue
        
    def updateNetIncome(self,netIncome, step):
        self.currentValue[step] = netIncome


class ResultBase(dict):
    def __init__(self):
        
        self['runs'] = dict()
        self['runs']['scenarios'] = dict()
        self['runs']['scenarios']['parties'] = dict()
        self['runs']['scenarios']['instruments'] = dict()
        
    def addToResultBaseInstrumentResult(self, runID, scenarioID, instrumentID, instrumentResult: InstrumentLevelResultObject):
        self['runs'][runID]['scenarios'][scenarioID]['instruments'][instrumentID] = instrumentResult
        return(self)
    
    def getFromResultBaseInstrumentResult(self, runID, scenarioID, instrumentID):
        ret = None
        if self['runs'].get(runID,None) != None:
            if self['runs'].get(runID,None)['scenarios'].get(scenarioID, None) != None:
                if self['runs'].get(runID,None)['scenarios'].get(scenarioID, None)['instruments'].get(instrumentID,None) != None:
                    ret = self['runs'].get(runID,None)['scenarios'].get(scenarioID, None)['instruments'].get(instrumentID,None)
        return(ret)
