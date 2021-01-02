import logging

class Asset:
    '''
    classdocs
    '''

    def __init__(self, id:str, logger:logging.Logger):
        self.id = id
        self.logger = logger
        # log
        self.logger.info('Initializing: '+ str(self.id))

class RealEstate(Asset):

    def __init__(self, id, logger, current_market_value:float, property_tax:float, renovation_costs:float, renovation_steps: set, house_community_costs:float, real_estate_index: dict):
        # Constructor
        super().__init__(id, logger)
        self.current_market_value = current_market_value
        self.price = dict()
        self.monthly_costs = dict()
        self.property_tax = property_tax
        self.renovation_costs = renovation_costs
        self.renovation_steps = renovation_steps
        self.house_community_costs = house_community_costs
        self.real_estate_index = real_estate_index


    def calculate_price(self, step):
        if step == 0:
            self.price[step] = self.current_market_value
        else:
            if self.price[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.price[step] = self.price[0] * self.real_estate_index[step]
        self.logger.debug('step '+str(step)+' | '+self.id+' price: '+str(self.price[step]))

    def calculate_monthly_costs(self, step):
        # renovations happen at distinct steps - renovation_steps
        if step in self.renovation_steps:
            self.monthly_costs[step] = self.property_tax / 12 + self.renovation_costs + self.house_community_costs/12
        else:
            self.monthly_costs[step] = self.property_tax / 12 + self.house_community_costs/12
        self.logger.debug('step '+str(step)+' | '+self.id+' monthly costs: '+str(self.monthly_costs[step]))