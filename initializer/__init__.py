from context.party import Party
from context.context import Context
from context.eventDomain import EventDomain
from context.portfolio import Portfolio
from context.behaviour import Behaviour
from context.scenario import FinancialScenario
from instruments.currentAccount import CurrentAccount
import sourceData
import json
import redis

def initializeParty(source_data):
    party = Party()
    party.name = source_data['party']['name']
    party.monthly_income = source_data['party']['monthly_income']
    
    party.portfolio = Portfolio()
    
    for instrument in source_data['portfolio']:
        if(instrument['type'] == 'current_account'):
            party.portfolio.instruments.append(CurrentAccount(instrument['id']
                                                              , instrument['name']
                                                              , instrument['current_outstanding']
                                                              , instrument['cnit']
                                                              , instrument['monthly_cost']))
    return(party)

def initializeContext(source_data):
    context = Context()
    context.eventDomain = EventDomain(source_data['context']['event_domain']['months'])
    return(context)

def initializeBehaviour(source_data):
    b = Behaviour()
    for scenario in source_data['behaviour']['scenarios']:
        s = FinancialScenario(scenario['financial']['ID']
                              , scenario['financial']['consumption_share']
                              , scenario['financial']['investment_share']
                              , scenario['financial']['portfolio_shares'])
        b.appendScenario(s)
    return(b)

def initializeResultBase(rredis):
    resultBase      = dict()
    resultBase_ser  = json.dumps(resultBase) 
    
    # Store serialized to REDIS
    rredis.set('resultBase', resultBase_ser)
        
    
    
    