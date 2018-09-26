'''
Created on Jul 27, 2018

@author: radov
'''

class Scheduler(object):
    '''
    classdocs
    '''
    schedule = dict()

    def __init__(self, product):
        '''
        Constructor
        '''
        schedule[0] = {'function' : Calculator.addInterest(product), 'description' : 'Add interest'}
        schedule[1] = {'function' : Calculator.deductCosts(product), 'description' : 'Add interest'}
        schedule[2] = {'function' : Calculator.distributeIncome(product, behaviour), 'description' : 'Add interest'}