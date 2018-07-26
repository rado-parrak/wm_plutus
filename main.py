'''
Created on Jul 26, 2018

@author: radov
'''

from context.eventDomain import EventDomain
from context.portfolio import Portfolio
from products.currentAccount import CurrentAccount

# generate eventdomain
ed = EventDomain(10)

# generate products
ca = CurrentAccount('CSOB_bezny_ucet', 100.0, 0.05, 2.0, ed)
for i in ed.steps:
    ca.calculateOutstanding(i)
    ca.calculateCumulativeCosts(i)
    ca.calculateBasisReturn(i)
    print(ca.basisReturn[i])

ca.deposit(10000, 4)
print(ca.outstanding[4])

# setup portfolio    
portfolio = Portfolio
portfolio.products.append(object)

