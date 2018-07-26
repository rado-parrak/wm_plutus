from context.joe import Joe
from context.context import Context
from context.eventDomain import EventDomain
from context.portfolio import Portfolio
from products.currentAccount import CurrentAccount
import sourceData

def initializeJoe():
    joe = Joe()
    joe.name = sourceData.JOE_NAME
    joe.monthly_income = sourceData.JOE_MONTHLY_INCOME
    joe.monthly_spendings = sourceData.JOE_MONTHLY_SPENDINGS
    joe.saving_share = sourceData.JOE_SHARE_SAVINGS
    joe.inv_share = sourceData.JOE_SHARE_INV
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