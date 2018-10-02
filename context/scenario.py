'''
Created on Sep 26, 2018

@author: radov
'''

class FinancialScenario(object):
    '''
    classdocs
    '''


    def __init__(self, ID, consumption_share, investment_share, portfolio_shares):
        '''
        Constructor
        '''
        self.ID = ID
        self.consumption_share = consumption_share
        self.investment_share = investment_share
        self.portfolio_shares = portfolio_shares