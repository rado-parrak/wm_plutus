'''
Created on Jul 26, 2018

@author: Rado
'''
import redis
redis = redis.StrictRedis(host='localhost', port=6379, db=0)
redis.flushall()

import initializer
import sourceData as sd
from calculator import Calculator

# --- INITIALIZE ---
party      = initializer.initializeParty(sd.source_data)
context    = initializer.initializeContext(sd.source_data)
behaviour  = initializer.initializeBehaviour(sd.source_data)
initializer.initializeResultBase(redis)

# --- DO CALCULATIONS ---
calc = Calculator(party, context, behaviour, redis)

'''
outstandings = calc.calculateOutstandings()
'''



    

