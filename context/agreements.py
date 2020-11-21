import logging
class Agreement:
    '''
    classdocs
    '''

    def __init__(self, id:str, logger:logging.Logger):
        self.id = id
        self.cash_flow = dict()
        self.logger = logger
        # log
        self.logger.info('Initializing: '+ str(self.id))

class RentalAgreement(Agreement):

    def __init__(self, id, logger, average_yearly_validity:float, inflation_index:dict, my_position:str, rent:float, yearly_costs:float):
        # Constructor
        super().__init__(id, logger)
        self.average_yearly_validity = average_yearly_validity # how much time, on average, over year this agreement is in place
        self.inflation_index = inflation_index
        self.my_position = my_position
        self.rent = rent
        self.yearly_costs = yearly_costs

    def projectCashFlow(self, step):
        if self.my_position=='renter':
            self.cash_flow[step] = self.average_yearly_validity * (self.rent - self.yearly_costs/12)

        if self.my_position=='rentee':
            self.cash_flow[step] = self.average_yearly_validity * (-self.rent - self.yearly_costs/12)

class UtilitiesAgreement(Agreement):
    def __init__(self, id, logger, linked_asset, water, gas, electricity, internet, heat, average_yearly_validity):
        # Constructor
        super().__init__(id, logger)
        self.linked_asset = linked_asset
        self.water = water
        self.gas = gas
        self.electricity = electricity
        self.internet = internet
        self.heat = heat
        self.average_yearly_validity = average_yearly_validity

    def project_cash_flow(self, step):
        self.cash_flow[step] = - 1 * self.average_yearly_validity * (self.water + self.gas + self.electricity + self.internet + self.heat)

class EmployeeContract(Agreement):
    def __init__(self, id, logger, average_yearly_validity, salary, bonus_steps: set, yearly_salary_trend, income_tax_rate, bonus_rate):
        # Constructor
        super().__init__(id, logger)
        self.average_yearly_validity = average_yearly_validity
        self.bonus_steps = bonus_steps
        self.salary = salary
        self.income_tax_rate = income_tax_rate
        self.yearly_salary_trend = yearly_salary_trend
        self.bonus_rate = bonus_rate

    def project_cash_flow(self, step):
        if step in self.bonus_steps:
            bonus = self.bonus_rate * (12*self.salary)
        else:
            bonus = 0.0
        self.cash_flow[step] = (1 + (step // 12) * self.yearly_salary_trend) * (self.salary + bonus) * (1-self.income_tax_rate)