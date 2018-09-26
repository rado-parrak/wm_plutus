'''
Created on Jul 26, 2018

@author: Rado
'''
import initializer
import sourceData as sd
from calculator import Calculator

# --- INITIALIZE ---
party      = initializer.initializeParty(sd.source_data)
context    = initializer.initializeContext(sd.source_data)
behaviour  = initializer.initializeBehaviour(sd.source_data)

# --- DO CALCULATIONS ---
calc = Calculator(party, context, behaviour)
#pw = calc.projectPortfolioWeights('standard')


'''
outstandings = calc.calculateOutstandings()
'''



    

