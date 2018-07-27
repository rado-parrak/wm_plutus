'''
Created on Jul 26, 2018

@author: radov
'''

class Behaviour(object):
    '''
    classdocs
    '''
    financial   = dict()
    product     = dict()
        
    def __init__(self):
        '''
        Constructor
        '''
        self.financial['monthly_spending_share'] = None
        self.financial['saving_share'] = None
        self.financial['saving_frequency'] = None
        self.financial['inv_share'] = None
        self.financial['inv_frequency'] = None
        
        self.product['portfolio_weights'] = None