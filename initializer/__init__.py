from context.joe import Joe
from context.context import Context
from context.eventDomain import EventDomain
from context.portfolio import Portfolio
from context.behaviour import Behaviour
from products.currentAccount import CurrentAccount
import sourceData

def initializeJoe():
    joe = Joe()
    joe.name = sourceData.JOE_NAME
    joe.monthly_income = sourceData.JOE_MONTHLY_INCOME
    joe.portfolio = Portfolio()
    
    for k in sourceData.JOE_PORTFOLIO.keys():
        prod = sourceData.JOE_PORTFOLIO.get(k)
        if(prod[0] == 'current_account'):
            joe.portfolio.products.append(CurrentAccount(prod[1], prod[2], prod[3], prod[4]))
    return(joe)

def initializeContext():
    context = Context()
    context.eventDomain = EventDomain(sourceData.event_domain_steps)
    return(context)

def initializeBehaviour():
    behaviourBase = dict()
    
    for k in sourceData.behaviourBase.keys():
        el = sourceData.behaviourBase.get(k)
        b = Behaviour()
        b.financial['monthly_spending_share'] = el['financial']['monthly_spending_share']
        b.financial['saving_share'] = el['financial']['saving_share']
        b.financial['saving_frequency'] = el['financial']['saving_frequency']
        b.financial['inv_share'] = el['financial']['inv_share']
        b.financial['inv_frequency'] = el['financial']['inv_frequency']
        
        b.product['portfolio_weights'] = el['portfolio']
        
        behaviourBase[k] = b
        
    return(behaviourBase)    
    
    
    