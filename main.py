'''
Created on Jul 26, 2018

@author: radov
'''
from context.eventDomain import EventDomain
from context.portfolio import Portfolio
from products.currentAccount import CurrentAccount
import initializer
from calculator import Calculator

# INITIALIZE:
joe        = initializer.initializeJoe()
context    = initializer.initializeContext()
behaviour  = initializer.initializeBehaviour()

# CALCULATE:
calc = Calculator(joe, context, behaviour)
pw = calc.projectPortfolioWeights('standard')
print(pw)

#outstandings = calc.calculateOutstandings()




    

