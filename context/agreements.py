import logging
class Agreement:

    def __init__(self, id:str, logger:logging.Logger):
        self.id = id
        self.cash_flow = dict()
        self.logger = logger

class RentalAgreement(Agreement):

    def __init__(self, id:str, logger:logging.Logger, index:dict, my_position:str, rent:float, yearly_costs:float):
        super().__init__(id, logger)
        self.index = index
        self.my_position = my_position
        self.rent = rent
        self.yearly_costs = yearly_costs

        self.logger.info('Initializing: Rental Agreement: {} with: '.format(self.id))
        self.logger.info('- position: {}'.format(my_position))
        self.logger.info('- rent: {}'.format(rent))
        self.logger.info('- yearly costs: {}'.format(yearly_costs))

    def calculate_cashflow(self, step):
        if self.my_position=='renter':
            self.cash_flow[step] = self.rent - self.yearly_costs/12
            self.logger.debug('[STEP {}] Cash-flow from rental agreement (renter): {:.2f}'.format(step, self.cash_flow[step] ))

        if self.my_position=='rentee':
            self.cash_flow[step] = -1.0 * self.rent
            self.logger.debug('[STEP {}] Cash-flow from rental agreement (rentee): {:.2f}'.format(step, self.cash_flow[step] ))

class UtilitiesAgreement(Agreement):
    def __init__(self, id, logger:logging.Logger, water:float, gas:float, electricity:float, internet:float, heat:float):
        super().__init__(id, logger)
        self.water = water
        self.gas = gas
        self.electricity = electricity
        self.internet = internet
        self.heat = heat
        
        self.logger.info('Initializing: Utilities Agreement: {} with: '.format(self.id))
        self.logger.info('- water: {}'.format(water))
        self.logger.info('- gas: {}'.format(gas))
        self.logger.info('- electricity: {}'.format(electricity))
        self.logger.info('- internet: {}'.format(internet))
        self.logger.info('- heat: {}'.format(heat))

    def calculate_cashflow(self, step):
        self.cash_flow[step] = - 1 * (self.water + self.gas + self.electricity + self.internet + self.heat)
        self.logger.debug('[STEP {}] Cash-flow from utilities agreement: {:.2f}'.format(step, self.cash_flow[step] ))

class EmployeeContract(Agreement):
    def __init__(self, id, logger:logging.Logger, salary:float, income_tax_rate:float, events:dict, duration:int):
        super().__init__(id, logger)
        self.salary = salary
        self.income_tax_rate = income_tax_rate
        self.events = events
        self.duration = duration 

        self.logger.info('Initializing: Employee Agreement: {} with: '.format(self.id))
        self.logger.info('- salary: {}'.format(salary))
        self.logger.info('- income tax rate: {}'.format(income_tax_rate))
        self.logger.info('- duration: {}'.format(duration))
        

    def calculate_cashflow(self, step):
        if self.events is not None:
            # modify
            if 'modify' in self.events.keys():
                for event in self.events['modify']:
                    if event['step'] == step:
                        self.salary = self.salary + event['value']

        salary = self.salary
        if self.events is not None:
            # bonuses
            if 'bonus' in self.events.keys():
                for event in self.events['bonus']:
                    if event['step'] == step:
                        salary += event['value']
                        self.logger.debug('[STEP {}] Bonus cash-flow from employee agreement: {:.2f}'.format(step, event['value'] ))
   
        self.cash_flow[step] = salary * (1-self.income_tax_rate)

        # after contract termination it is 0
        if step > self.duration*12:
            self.cash_flow[step] = 0.0
        self.logger.debug('[STEP {}] Cash-flow from employee agreement: {:.2f}'.format(step, self.cash_flow[step] ))