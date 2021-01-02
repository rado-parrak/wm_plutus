from context.instruments import CurrentAccount, Mortgage
from context.assets import RealEstate
from context.agreements import EmployeeContract
from context.market import Market
import logging
class Party:

    def __init__(self, id: str, logger:logging.Logger, initial_free_resources: float, initial_portfolio: set, monthly_expenditures: float, discount_rate: float):
        '''
        Constructor
        '''
        self.id = id
        self.initial_free_resources = initial_free_resources
        self.initial_portfolio = initial_portfolio
        self.resources = dict()
        self.free_resources = dict()
        self.portfolio = initial_portfolio
        self.portfolio_types = dict()
        self.monthly_expenditures = monthly_expenditures
        self.expenditures = dict()
        self.free_resources_pv = dict()
        self.discount_rate = discount_rate
        self.portfolio_values = dict()
        self.logger = logger

        self.logger.info('Initializing party: {}'.format(self.id))
        self.logger.info('with initial portfolio: {}'.format(self.initial_portfolio))
        self.logger.info('with initial free resources: {}'.format(self.initial_free_resources))

    def refresh_portfolio(self, step):
        if step == 0:
            self.portfolio = self.initial_portfolio
            
        self.logger.debug('[STEP {}] Portfolio members: {}'.format(step, self.portfolio))

        # TODO: add portfolio changes according to a behaviour
        # else:

    def calculate_expenditures(self, step):        
        # expenditures from consumption
        expenditures = self.monthly_expenditures
        self.logger.debug('[STEP {}] Expenditures from consumption: {:.2f}'.format(step, self.monthly_expenditures))

        # expenditures from porfolio holding
        for item in self.portfolio:
            if isinstance(item, Mortgage):
                item.project_monthly_costs(step)
                expenditures = expenditures + item.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from mortgage: {:.2f}'.format(step, item.monthly_costs[step]))

            if isinstance(item, CurrentAccount):
                item.project_monthly_costs(step)
                expenditures = expenditures + item.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from the current account: {:.2f}'.format(step, item.monthly_costs[step]))

            if isinstance(item, RealEstate):
                item.calculate_monthly_costs(step)
                expenditures = expenditures + item.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from the real estate {:.2f}'.format(step, item.monthly_costs[step]))

        # total expenditures
        self.expenditures[step] = expenditures
        self.logger.info('[STEP {}] Total expenditures: {:.2f}'.format(step, expenditures))

    def calculate_resources(self, step):
        resources = 0.0
        if step == 0:
            resources = self.initial_free_resources

        for item in self.portfolio:
            if isinstance(item, CurrentAccount):
                item.project_value(step)
                resources = resources + item.value[step]
                self.logger.debug('[STEP {}] Resources from current account: {:.2f}'.format(step, item.value[step]))

            if isinstance(item, EmployeeContract):
                item.project_cash_flow(step)
                resources = resources + item.cash_flow[step]
                self.logger.debug('[STEP {}] Resources from the employee contract: {:.2f}'.format(step, item.cash_flow[step]))

        self.resources[step] = resources
        self.logger.info('[STEP {}] Total resources: {:.2f}'.format(step, resources))

    def calculate_free_resources(self, step):
        self.refresh_portfolio(step)
        self.calculate_resources(step)
        self.calculate_expenditures(step)
        self.free_resources[step] = self.resources[step] - self.expenditures[step]

        self.logger.info('[STEP {}] Free resources: {:.2f}'.format(step, self.free_resources[step]))

    def allocate_free_resources(self, step):
        # TODO: assumption: only single current account

        for item in self.portfolio:
            if isinstance(item, CurrentAccount):
                item.withdraw_all(step)
                item.deposit(step, self.free_resources[step])

    def discount_free_resources(self, step: int, discount_rate: float):
        # TODO: discout rate / factor should be also a curve, not a point
        
        # discount factor calculation
        df = 1 / ((1+discount_rate)**(step/12.0))
        self.logger.debug('[STEP {}] Discount factor: {:.4f}'.format(step, df))

        self.free_resources_pv[step] = self.free_resources[step] * df
        self.logger.info('[STEP {}] Discounted free resources: {:.2f}'.format(step, self.free_resources_pv[step]))

    def calculate_portfolio_value(self, step):
        portfolio_value = 0.0

        for item in self.portfolio:
            if isinstance(item, RealEstate):
                # project value
                item.calculate_price(step)
                portfolio_value = portfolio_value + item.price[step]

        self.portfolio_values[step] = portfolio_value
        self.logger.info('[STEP {}] Portfolio value: {:.2f}'.format(step, portfolio_value))        

    def live(self, steps: int):
            for step in range(0, steps):
                self.logger.info('')
                self.logger.info('>>>>>> Party {} is living the step: {} <<<<<<<'.format(self.id, step))
                # resources
                self.calculate_free_resources(step)
                self.allocate_free_resources(step)
                self.discount_free_resources(step, self.discount_rate)

                # balance
                self.calculate_portfolio_value(step)
