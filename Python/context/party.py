from context.instruments import CurrentAccount, Mortgage
from context.assets import RealEstate
from context.agreements import EmployeeContract
from context.market import Market

class Party:

    def __init__(self, name: str, initial_free_resources: float, initial_portfolio: set, monthly_expenditures: float, discount_rate: float, market: Market):
        '''
        Constructor
        '''
        self.name = name
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
        self.market = market

    def refresh_portfolio(self, step):
        if step == 0:
            self.portfolio = self.initial_portfolio
        # TODO: add portfolio changes according to a behaviour

    def calculate_expenditures(self, step):
        # expenditures from consumption
        expenditures = self.monthly_expenditures

        # expenditures from porfolio holding
        for item in self.portfolio:
            if isinstance(item, Mortgage):
                item.project_monthly_costs(step)
                expenditures = expenditures + item.monthly_costs[step]

            if isinstance(item, CurrentAccount):
                item.project_monthly_costs(step)
                expenditures = expenditures + item.monthly_costs[step]

            if isinstance(item, RealEstate):
                item.project_monthly_costs(step)
                expenditures = expenditures + item.monthly_costs[step]

        # total expenditures
        self.expenditures[step] = expenditures

    def calculate_resources(self, step):
        resources = 0.0
        if step == 0:
            resources = self.initial_free_resources

        for item in self.portfolio:
            if isinstance(item, CurrentAccount):
                item.project_value(step)
                resources = resources + item.value[step]

            if isinstance(item, EmployeeContract):
                item.project_cash_flow(step)
                resources = resources + item.cash_flow[step]

        self.resources[step] = resources

    def calculate_free_resources(self, step, verbose=True):
        self.refresh_portfolio(step)
        self.calculate_resources(step)
        self.calculate_expenditures(step)
        self.free_resources[step] = self.resources[step] - self.expenditures[step]

        if verbose:
            print('=========================================================================================')
            print('[step ' + str(step) + '] Expenditures = ' + str(self.expenditures[step]))
            print('[step ' + str(step) + '] Resources = ' + str(self.resource[step]))
            print('----------------------------------------------------------------------------')
            print('[step ' + str(step) + '] Total free resources to allocate = ' + str(self.free_resources[step]))

    def allocate_free_resources(self, step, verbose=True):
        # assumption: only single current account
        for item in self.portfolio:
            if isinstance(item, CurrentAccount):
                item.withdraw_all(step)
                item.deposit(step, self.free_resources[step])
                if verbose:
                    print('[step ' + str(step) + '] Resources allocated to current account :: ' + item.name + ' = ' + str(self.free_resources[step]))
                    print('=========================================================================================')

    def discount_free_resources(self, step: int, discount_rate: float, verbose=False):
        # discount factor calculation
        df = 1 / ((1+discount_rate)**(step/12.0))
        if verbose:
            print('discount rate in step ' + str(step) + ': ' + str(df))

        self.free_resources_pv[step] = self.free_resources[step] * df

    def project_portfolio_value(self, step, scenario_name):
        portfolio_value = 0.0
        for item in self.portfolio:
            if isinstance(item, RealEstate):
                # fetch market linked market object
                linked_market_object = item.linked_market_object

                # determine index value given step and scenario
                index_value = float(self.market.market_objects[linked_market_object].monthly_values[scenario_name][step])

                # project value
                item.project_price(step, index_value)
                portfolio_value = portfolio_value + item.price[step]

        if scenario_name not in self.portfolio_values.keys():
            self.portfolio_values[scenario_name] = dict()
        self.portfolio_values[scenario_name][step] = portfolio_value


    def live(self, steps: int, verbose=False):
        for scenario in self.market.scenarios:
            for step in range(0, steps):
                # resources
                self.calculate_free_resources(step, verbose)
                self.allocate_free_resources(step, verbose)
                self.discount_free_resources(step, self.discount_rate)

                # balance
                self.project_portfolio_value(step, scenario.name)
