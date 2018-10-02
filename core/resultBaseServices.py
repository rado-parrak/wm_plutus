'''
Created on Sep 26, 2018

@author: radov
'''

def addOutstandingToResultBase(resultBase, scenario, instrument, step, outstanding):
    if resultBase.get(scenario.ID) == None:
        resultBase[scenario.ID] = dict()
            
    if resultBase[scenario.ID].get(instrument.ID) == None:
        resultBase[scenario.ID][instrument.ID] = dict()
       
    resultBase[scenario.ID][instrument.ID][step] = outstanding        
    return(resultBase)