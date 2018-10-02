'''
Created on Jul 26, 2018

@author: radov
'''
from context.scenario import FinancialScenario

class Behaviour(object):
    '''
    classdocs
    '''
    scenarios   = []
        
    def __init__(self):
        '''
        Constructor
        '''
        
    def appendScenario(self, financialScenario: FinancialScenario):
        self.scenarios.append(financialScenario)