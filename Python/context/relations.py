'''
Created on Oct 4, 2018

@author: radov
'''

class Relations:
    '''
    classdocs
    '''

    def __init__(self, relations_source_data):
        '''
        Constructor
        '''
        self.party_instrument = dict()
        for p in relations_source_data['party_instrument']:
            self.party_instrument[p] = relations_source_data['party_instrument'][p]