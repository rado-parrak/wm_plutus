'''
Created on Jul 26, 2018

@author: radov
'''
from resultObjects import PartyLevelResultObject

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