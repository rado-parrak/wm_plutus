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
# =================  INITIALIZATION  =================  
initialization_object = dict()
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
instruments = list()
for i in range(len(sd.source_data['instruments'])):
    instruments.append( initializeInstrument(sd.source_data['instruments'][i]) )
    
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
# TO BE DONE

# z) --- add to the the initialization_object and store to redis
initialization_object['runs_configs'] = runs_config
initialization_object['facts'] = facts
initialization_object['scenarios'] = None
    
# Store serialized to REDIS
rredis.set('initialization_object', pickle.dumps(initialization_object) )