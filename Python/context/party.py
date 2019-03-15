'''
Created on Jul 26, 2018

@author: radov
'''
from resultObjects import PartyLevelResultObject
from context.instruments import InstrumentClass
from context.behaviour import BehaviourLibrary
from context.behaviour  import BehaviourScheme
from operator import itemgetter

class Party:
    '''
    This is the party in the entire setup
    '''

    def __init__(self, party_source_data):
        '''
        Constructor
        '''
        self.ID = party_source_data['ID']
        self.name = party_source_data['name']
        self.grossWage = party_source_data['monthly_gross_wage']    
        
        
    def calculateGrossWage(self, step, previous_results: PartyLevelResultObject):
        return(self.grossWage)
    
    def calculateIncomeTax(self, grossWage):
        #TODO: There should come a more elaborate calculation of this in line with the Czech legislation       
        return(self.grossWage * 0.21) 
    
    def staticSharesBestReturn(self, amount, instruments, shares):
        allocatedQuantities = dict()
        #i.) Savings:
        ret = -999
        for instrument in instruments:
            if instrument.instrument_class == InstrumentClass.SAVING:
                if instrument.CNIT > ret:
                    selectedInstrument = instrument
                    
        allocatedQuantities[selectedInstrument.ID] = shares['saving'] * amount
        
        
        return(allocatedQuantities)
    
    def prepareAllocationInputs(self, selectedBehaviourScheme, root, partyResult: PartyLevelResultObject, partyID, step):
        # this method prepares the allocation input parameters (= kwargs) for the respective allocation
        # mechanism
        allocationInputs = dict() 
        # i) static shares, best return:
        if selectedBehaviourScheme == BehaviourScheme.STATIC_SHARES_BEST_RETURN:
            allocationInputs['amount'] = partyResult.netCashBalance[step]            
            instrumentIDs = root['facts']['relations'].party_instrument[partyID]
            allocationInputs['instruments'] = itemgetter(*instrumentIDs)(root['facts']['instruments'])
            allocationInputs['shares'] = root['facts']['behaviour'].party[partyID]
        
        return(allocationInputs)
    
    def allocate(self, selectedBehaviourScheme, **kwargs):
        behaviourFunction = BehaviourLibrary.schemes[selectedBehaviourScheme]
        return( behaviourFunction(self, **kwargs) )



    