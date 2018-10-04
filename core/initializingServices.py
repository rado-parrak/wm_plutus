'''
Created on Oct 4, 2018

@author: radov
'''
from context.instruments import *

def initializeInstrument(instrument_source_data):
    instrument = None
    if instrument_source_data['type'] == InstrumentType.CURRENT_ACCOUNT:
        instrument = CurrentAccount( instrument_source_data['ID']
                                     , instrument_source_data['name']
                                     , instrument_source_data['current_outstanding']
                                     , instrument_source_data['monthly_cost']
                                     , instrument_source_data['cnit'])
        
        
    return(instrument)