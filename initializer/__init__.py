from context.party import Party
from context.context import Context
from context.eventDomain import EventDomain
from context.portfolio import Portfolio
from context.behaviour import Behaviour
from context.scenario import FinancialScenario
from products.currentAccount import CurrentAccount
import sourceData

def initializeParty(source_data):
    party = Party()
    party.name = source_data['party']['name']
    party.monthly_income = source_data['party']['monthly_income']
    
    party.portfolio = Portfolio()
    
    for prod in source_data['portfolio']:
        if(prod['type'] == 'current_account'):
            party.portfolio.products.append(CurrentAccount(prod['name'], prod['current_outstanding'], prod['cnit'], prod['monthly_cost']))
    return(party)

def initializeContext(source_data):
    context = Context()
    context.eventDomain = EventDomain(source_data['context']['event_domain']['months'])
    return(context)

def initializeBehaviour(source_data):
    b = Behaviour()
    for scenario in source_data['behaviour']['scenarios']:
        s = FinancialScenario()
        s.consumption_share = scenario['financial']['consumption_share']
        s.investment_share  = scenario['financial']['investment_share']
        s.portfolio_shares  = scenario['financial']['portfolio_shares']
        b.scenarios.append(s)
        
    return(b)    
    
    
    