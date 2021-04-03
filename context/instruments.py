from enum import Enum
import logging

class InstrumentType(Enum):
    CURRENT_ACCOUNT = 1
    SAVING_ACCOUNT = 2


class InstrumentClass(Enum):
    CASH_BALANCE = 1
    SAVING = 2
    INVESTMENT = 3


class AccountType(Enum):
    ASSET = 1
    LIABILITY = 2


class Instrument:

    def __init__(self, id, logger):
        self.id = id
        self.logger = logger

class CurrentAccount(Instrument):

    def __init__(self, id:str, logger:logging.Logger, current_outstanding:float, monthly_cost:float, cnit:float, primary:bool=False, current_step:int=0):
        super().__init__(id, logger)
        self.cnit = cnit
        self.effective_rate = ((1 + self.cnit) ** (1 / 12)) - 1
        self.value = dict()
        self.value[current_step] = current_outstanding
        self.monthly_cost = monthly_cost
        self.monthly_costs = dict()
        self.current_step = current_step
        self.primary = primary

        self.logger.info('Initializing Current Account: {} with: '.format(self.id))
        self.logger.info(' - CNIT: {:.4f}'.format(cnit))
        self.logger.info(' - effective rate: {:.4f}'.format(self.effective_rate))
        self.logger.info(' - current outstanding: {:.2f}'.format(current_outstanding))
        self.logger.info(' - monthly cost: {}'.format(monthly_cost))

    def calculate_value(self, step):
        if step > self.current_step:
            if self.value[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.value[step] = self.value[step - 1] * (1 + self.effective_rate)
                self.logger.debug('[STEP {}] Account "{}" value: {}'.format(step, self.id, self.value[step]))

    def calculate_monthly_costs(self, step):
        self.monthly_costs[step] = self.monthly_cost
        self.logger.debug('[STEP {}] Account "{}" monthly cost: {}'.format(step, self.id, self.monthly_cost))

    def deposit(self, step, amount):
        self.value[step] = self.value[step] + amount
        self.logger.debug('[STEP {}] Amount deposited: {} to account "{}"'.format(step, amount, self.id))

    def withdraw_all(self, step):
        self.value[step] = 0.0
        self.logger.debug('[STEP {}] All funds withdrawn! from account {}'.format(step, self.id))

class Mortgage(Instrument):
    def __init__(self, id:str, logger:logging.Logger, principal:float, cnit:float, maturity_in_years:int, current_step:int=0):
        super().__init__(id, logger)
        self.cnit = cnit
        self.monthly_interest_rate = self.cnit*(31/365)
        self.value = dict()
        self.principal = principal
        self.maturity_in_years = maturity_in_years

        self.outstanding_amount = dict()
        self.outstanding_amount[current_step] = principal
        
        self.interest_payment = dict()
        self.interest_payment[current_step] = 0.0

        self.principal_payment = dict()
        self.principal_payment[current_step]= 0.0
        
        self.monthly_payment = 0.0
        self.monthly_costs = dict()
        self.current_step = current_step

        self.logger.info('Initializing Mortgage: {} with: '.format(self.id))
        self.logger.info(' - CNIT: {:.4f}'.format(cnit))
        self.logger.info(' - monthly interest rate: {:.4f}'.format(self.monthly_interest_rate))
        self.logger.info(' - principal: {:.2f}'.format(self.principal))
        self.logger.info(' - maturity (in years): {:.2f}'.format(self.maturity_in_years))

    def calculateNumberOfPeriods(self):
        self.number_of_periods = self.maturity_in_years * 12
        self.logger.debug(' Derived number of monthly periods: {:.2f}'.format(self.number_of_periods))

    def calculateMonthlyPayment(self):
        self.calculateNumberOfPeriods()
        self.monthly_payment = (self.monthly_interest_rate * self.principal) / (
                    1 - (1 + self.monthly_interest_rate) ** -self.number_of_periods)

        self.logger.debug(' Derived monthly mortgage payment: {:.2f}'.format(self.monthly_payment))

    def calculateOutstandingAmount(self, step):
        if step > self.current_step:
            if self.outstanding_amount[step-1] is None:
                raise Exception('Outstanding amount at previous step to step ' + str(step) + ' not calculated!')
            elif self.principal_payment[step-1] is None:
                raise Exception('Principal payment at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.outstanding_amount[step] = self.outstanding_amount[step-1] - self.principal_payment[step]
                self.logger.debug('[STEP {}] Outstanding amount: {}'.format(step, self.outstanding_amount[step]))

    def calculateInterestPayment(self, step):
        if step > self.current_step:
            if self.outstanding_amount[step - 1] is None:
                raise Exception('Outstanding amount at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.interest_payment[step] = self.outstanding_amount[step-1] * self.monthly_interest_rate
                self.logger.debug('[STEP {}] Interest payment: {}'.format(step, self.interest_payment[step]))

    def calculatePrincipalPayment(self, step):
        if step > self.current_step:
            if self.interest_payment[step - 1] is None:
                raise Exception('Interest payment at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.principal_payment[step] = self.monthly_payment - self.interest_payment[step]
                self.logger.debug('[STEP {}] Principal payment: {}'.format(step, self.principal_payment[step]))

    def calculate_monthly_costs(self, step):
        self.calculateMonthlyPayment
        self.monthly_costs[step] = self.monthly_payment

class Share(Instrument):

    def __init__(self, id:str, logger:logging.Logger, price:float, units:int, index: dict, dividend_yield:float, dividend_step:int,current_step:int=0):
        super().__init__(id, logger)
        self.price = price
        self.units = units
        self.index = index
        self.dividend_yield = dividend_yield
        self.dividend_step = dividend_step
        self.current_step = current_step

        self.logger.info('Initializing Share: {} with: '.format(self.id))
        self.logger.info(' - price: {:.2f}'.format(price))
        self.logger.info(' - units: {:.2f}'.format(self.units))
        self.logger.info(' - dividend_yield: {:.2f}'.format(dividend_yield))

        self.value = dict()
        self.value[0] = price*units

    def calculate_value(self, step):
        if step > self.current_step:
            if self.value[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.value[step] = self.value[step-1] * (self.index[step]/self.index[step-1])
                self.logger.debug('[STEP {}] Share "{}" value: {}'.format(step, self.id, self.value[step]))

    def pay_dividend(self, step):
        dividend=0.0
        if step==(step//12)*12+self.dividend_step:
            dividend = self.dividend_yield*self.value[step]
            self.logger.info('[STEP {}] Dividend of {} paid out by share "{}"'.format(step, dividend,self.id))
        else:
            self.logger.info('[STEP {}] Not a dividend month for share "{}"'.format(step, self.id))
        return(dividend)