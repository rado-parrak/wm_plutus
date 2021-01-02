import logging

class Asset:

    def __init__(self, id:str, logger:logging.Logger):
        self.id = id
        self.logger = logger

class RealEstate(Asset):

    def __init__(self, id, logger, current_market_value:float, property_tax:float, house_community_costs:float, real_estate_index: dict, events: dict, current_step=0):
        # Constructor
        super().__init__(id, logger)
        self.price = dict()
        self.price[current_step] = current_market_value
        self.monthly_costs = dict()
        self.property_tax = property_tax
        self.house_community_costs = house_community_costs
        self.real_estate_index = real_estate_index
        self.events = events
        self.current_step = current_step

        self.logger.info('Initializing Real Estate Asset: {} with: '.format(self.id))
        self.logger.info(' - current market value: {}'.format(current_market_value))
        self.logger.info(' - property tax: {}'.format(self.property_tax))
        self.logger.info(' - house community costs: {}'.format(self.house_community_costs))
        self.logger.info(' - real estate index: {}'.format(self.real_estate_index))
        self.logger.info(' - events: {}'.format(self.events))

    def calculate_price(self, step):
        if step > self.current_step:
            if self.price[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.price[step] = self.price[step - 1] * self.real_estate_index[step]

        self.logger.debug('[STEP {}] Real-estate price: {}'.format(step, self.price[step]))

    def calculate_monthly_costs(self, step):
        # regular
        self.monthly_costs[step] = self.property_tax/12 + self.house_community_costs/12

        # event-based
        if self.events is not None:
            # costs:
            if self.events['cost'] is not None:
                for event in self.events['cost']:
                    if event['step'] == step:
                        self.monthly_costs[step] = self.monthly_costs[step] + event['value']

        self.logger.debug('[STEP {}] Real-estate monthly costs: {}'.format(step, self.monthly_costs[step]))