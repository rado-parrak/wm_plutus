'''
Created on Oct 4, 2018

@author: radov
'''
import redis
import _pickle as pickle
import sourceData as sd
from context.party import Party
from context.relations import Relations
from context.runsConfig import RunsConfig
from context.behaviour import Behaviours
from initializingServices import initializeInstrument
from context.scenarios import Scenarios

def Initialize():  
    root = dict()
    # 0) --- redis:
    rredis = redis.StrictRedis(host='localhost', port=6379, db=0)
    rredis.flushall()
    
    # a) --- run config:
    runs_config = RunsConfig(sd.source_data['runs_config'])
    
    # b) --- facts:
    facts = dict()
    # b.i) parties:
    parties = list()
    for i in range(len(sd.source_data['parties'])):
        parties.append( Party(sd.source_data['parties'][i]) )
    
    # b.ii) instruments:
    instruments = dict()
    for i in range(len(sd.source_data['instruments'])):
        instrument = initializeInstrument(sd.source_data['instruments'][i])
        instruments[instrument.ID] = instrument
        
    # b.iii) relations:
    relations = Relations(sd.source_data['relations'])
    
    # b.v) behaviour:
    behaviours  = Behaviours(sd.source_data['behaviours'])
    
    # !!! STORE !!!
    facts['parties']        = parties
    facts['instruments']    = instruments
    facts['relations']      = relations
    facts['behaviours']     = behaviours 
    
    # c) --- scenarios:
    scenarios = Scenarios(sd.source_data['scenarios'])
    
    # z) --- add to the the initialization_object and store to redis
    root['runs_config'] = runs_config
    root['facts'] = facts
    root['scenarios'] = scenarios
        
    # Store serialized to REDIS
    rredis.set('root', pickle.dumps(root) )
    
    return(rredis)