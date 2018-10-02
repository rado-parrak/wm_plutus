'''
Created on Jul 26, 2018

@author: Rado
'''
import redis
rredis = redis.StrictRedis(host='localhost', port=6379, db=0)
rredis.flushall()

import initializer
import sourceData as sd
from calculator.calculator import Calculator

# --- INITIALIZE ---
party      = initializer.initializeParty(sd.source_data)
context    = initializer.initializeContext(sd.source_data)
behaviour  = initializer.initializeBehaviour(sd.source_data)
initializer.initializeResultBase(rredis)

# --- DO CALCULATIONS ---
calc = Calculator(party, context, behaviour, rredis)

# i) calculate outstandings on all instruments:
calc.calculateOutstandings()



    

