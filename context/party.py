'''
Created on Jul 26, 2018

@author: radov
'''

class Party:
    '''
    This is the party in the entire setup
    '''

    def __init__(self, party_source_data):
        '''
        Constructor
        '''
        self.name = party_source_data['name']
        self.monthly_income = party_source_data['monthly_income']    