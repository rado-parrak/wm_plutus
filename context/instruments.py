from enum import Enum

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
    '''
    classdocs
    '''
    def __init__(self, id, logger):
        self.id = id
        self.logger = logger
        # log
        self.logger.info('Initializing: '+ str(self.id))

class CurrentAccount(Instrument):
    '''
    classdocs
    '''

    def __init__(self, id, logger, current_outstanding, monthly_cost, cnit):
        # Constructor
        super().__init__(id, logger)
        self.cnit = cnit
        self.effective_rate = (1 + self.cnit) ** (1 / 12) - 1
        self.value = dict()
        self.current_outstanding = current_outstanding
        self.monthly_cost = monthly_cost
        self.monthly_costs = dict()

    def project_value(self, step):
        if step == 0:
            self.value[step] = self.current_outstanding
        else:
            if self.value[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.value[step] = self.value[step - 1] * (1 + self.effective_rate)

    def project_monthly_costs(self, step):
        self.monthly_costs[step] = self.monthly_cost

    def deposit(self, step, amount):
        self.value[step] = self.value[step] + amount

    def withdraw_all(self, step):
        self.value[step] = 0.0


class Mortgage(Instrument):
    def __init__(self, id, logger, principal, cnit, maturity_in_years):
        # Constructor
        super().__init__(id, logger)
        self.cnit = cnit
        self.monthly_interest_rate = self.cnit*(31/365)
        self.value = dict()
        self.principal = principal
        self.maturity_in_years = maturity_in_years
        self.outstanding_amount = dict()
        self.interest_payment = dict()
        self.principal_payment = dict()
        self.monthly_payment = 0.0
        self.monthly_costs = dict()

    def calculateNumberOfPeriods(self):
        self.number_of_periods = self.maturity_in_years * 12

    def calculateMonthlyPayment(self):
        self.calculateNumberOfPeriods()
        self.monthly_payment = (self.monthly_interest_rate * self.principal) / (
                    1 - (1 + self.monthly_interest_rate) ** -self.number_of_periods)

    def calculateOutstandingAmount(self, step):
        if step == 0:
            self.outstanding_amount[step] = self.principal
        else:
            if self.outstanding_amount[step-1] is None:
                raise Exception('Outstanding amount at previous step to step ' + str(step) + ' not calculated!')
            elif self.principal_payment[step-1] is None:
                raise Exception('Principal payment at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.outstanding_amount[step] = self.outstanding_amount[step-1] - self.principal_payment[step]

    def calculateInterestPayment(self, step):
        if step == 0:
            self.interest_payment[step] = 0.0
        else:
            if self.outstanding_amount[step - 1] is None:
                raise Exception('Outstanding amount at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.interest_payment[step] = self.outstanding_amount[step-1] * self.monthly_interest_rate

    def calculatePrincipalPayment(self, step):
        if step == 0:
            self.principal_payment[step] = 0.0
        else:
            if self.interest_payment[step - 1] is None:
                raise Exception('Interest payment at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.principal_payment[step] = self.monthly_payment - self.interest_payment[step]

    def project_monthly_costs(self, step):
        self.calculateMonthlyPayment
        self.monthly_costs[step] = self.monthly_payment

# class SavingAccount(Instrument):
#     '''
#     classdocs
#     '''
#
#     def __init__(self, id, name, current_outstanding, monthly_cost, cnit):
#         # Constructor
#         super().__init__(id, name)
#         self.cnit = cnit
#         self.effective_rate = (1 + self.cnit) ** (1 / 12) - 1
#         self.value = dict()
#         self.current_outstanding = current_outstanding
#         self.monthly_cost = monthly_cost
#
#     def projectValue(self, step):
#         if step == 0:
#             self.value[step] = self.current_outstanding
#         else:
#             if self.value[step - 1] is None:
#                 raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
#             else:
#                 self.value[step] = self.value[step - 1] * (1 + self.effective_rate) - self.monthly_cost



