class Agreement:
    '''
    classdocs
    '''

    def __init__(self, id, name):
        self.id = id
        self.name = name

class RentalAgreement(Agreement):

    def __init__(self, id, name, average_yearly_validity, linked_asset, my_position, rent, yearly_costs):
        # Constructor
        super().__init__(id, name)
        self.average_yearly_validity = average_yearly_validity # how much time, on average, over year this agreement is in place
        self.linked_asset = linked_asset # id of a linked asset

    def projectCashFlow(self, step):
        if self.my_position=='renter':
            self.cash_flow[step] = self.average_yearly_validity * (self.rent - self.yearly_costs/12)

        if self.y_position=='rentee':
            self.cash_flow[step] = self.average_yearly_validity * (-self.rent - self.yearly_costs/12)

class UtilitiesAgreement(Agreement):
    def __init__(self, id, name, linked_asset, water, gas, electricity, internet, heat, average_yearly_validity):
        # Constructor
        super().__init__(id, name)
        self.linked_asset = linked_asset
        self.water = water
        self.gas = gas
        self.electricity = electricity
        self.internet = internet
        self.heat = heat
        self.average_yearly_validity = average_yearly_validity

    def projectCashFlow(self, step):
        self.cash_flow[step] = - 1 * self.average_yearly_validity * (self.water + self.gas + self.electricity + self.internet + self.heat)

class EmployeeContract(Agreement):
    def __init__(self, id, name, average_yearly_validity, salary, bonus_steps: set, yearly_salary_trend, income_tax_rate, bonus_rate):
        # Constructor
        super().__init__(id, name)
        self.average_yearly_validity = average_yearly_validity
        self.bonus_steps = bonus_steps
        self.salary = salary
        self.income_tax_rate = income_tax_rate
        self.yearly_salary_trend = yearly_salary_trend
        self.salary_income = dict()
        self.bonus_rate = bonus_rate

    def project_salary_income(self, step):
        if step in self.bonus_steps:
            bonus = self.bonus_rate * (12*self.salary)
        else:
            bonus = 0.0
        self.salary_income[step] = (1 + (step // 12) * self.yearly_salary_trend) * (self.salary + bonus) * (1-self.income_tax_rate)

    def pay_salary(self, step) -> float:
        self.project_salary_income(step)
        return self.salary_income[step]