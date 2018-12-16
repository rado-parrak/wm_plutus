'''
Created on Jul 26, 2018

@author: radov
'''
from enum import Enum
from context.instruments import InstrumentClass

class Behaviour:
    '''
    classdocs
    '''
        
    def __init__(self, behaviour_source_data):
        '''
        Constructor
        '''
        self.party = dict()
        for key in behaviour_source_data['party'].keys():
            self.party[key] = behaviour_source_data['party'][key]
            
class BehaviourScheme(Enum):
    STATIC_SHARES_BEST_RETURN = 1 # allocation schemes are static over time, entire share is allocated into instrument with largest return
          
                        
class BehaviourLibrary:
    
    def staticSharesBestReturn(self, amount, instruments, shares):
        allocatedQuantities = dict()
        #i.) Savings:
        # allocate all saving-dedicated share of the remaining funds into the 
        # saving instrument with the largest income
        ret = -999
        for instrument in instruments:
            if instrument.instrument_class == InstrumentClass.SAVING:
                if instrument.cnit > ret:
                    selectedInstrument = instrument
                    ret = instrument.cnit
                    
        allocatedQuantities[selectedInstrument.ID] = shares['saving_allocation_weight'] * amount
        
        #i.) Cash:
        # allocate all cash-dedicated share of the remaining funds into the 
        # saving instrument with the largest income
        ret = -999
        for instrument in instruments:
            if instrument.instrument_class == InstrumentClass.CASH_BALANCE:
                if instrument.cnit > ret:
                    selectedInstrument = instrument
                    ret = instrument.cnit
                    
        allocatedQuantities[selectedInstrument.ID] = shares['cash_allocation_weight'] * amount
        
        
        return(allocatedQuantities)
    
    # list of all behaviour schemes
    schemes = {BehaviourScheme.STATIC_SHARES_BEST_RETURN : staticSharesBestReturn}