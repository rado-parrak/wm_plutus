from context.instruments import CurrentAccount
from context.agreements import EmployeeContract

class Party:

    def __init__(self, name: str, initial_free_resources: float, initial_portfolio: set, monthly_expenditures: float):
        '''
        Constructor
        '''
        self.name = name
        self.initial_free_resources = initial_free_resources
        self.initial_portfolio = initial_portfolio
        self.free_resources = dict()
        self.portfolio = initial_portfolio
        self.portfolio_types = dict()
        self.monthly_expenditures = monthly_expenditures
        self.expenditures = dict()

    def refresh_portfolio(self, step):
        if step == 0:
            self.portfolio = self.initial_portfolio
        # TODO: add portfolio changes according to a behaviour

    def calculate_expenditures(self, step):
        

    def calculate_free_resources(self, step, verbose=True):
        self.refresh_portfolio(step)
        free_resources = 0.0

        if verbose:
            print('=========================================================================================')

        # Calculate monthly expenditures
        self.expenditures[step] = self.monthly_expenditures
        if verbose:
            print('[step ' + str(step) + '] Monthly expenditures = ' + str(self.expenditures[step]))
        # Calculate free resources coming from the portfolio
        for item in self.portfolio:
            # Current accounts:
            if isinstance(item, CurrentAccount):
                # resources:
                resources_from_this_item = item.freeup_resources(step)
                if verbose:
                    print('[step ' + str(step) + '] Resources from current account :: ' + item.name + ' = ' + str(resources_from_this_item))
                # costs:
                costs_from_this_item = item.pay_costs(step)
                if verbose:
                    print('[step ' + str(step) + '] Costs from current account :: ' + item.name + ' = ' + str(costs_from_this_item))

                # free resources:
                free_resources_from_this_item = resources_from_this_item - costs_from_this_item
                if verbose:
                    print('[step ' + str(step) + '] Free resources from current account :: ' + item.name + ' = ' + str(free_resources_from_this_item))

                # add to total
                free_resources = free_resources + free_resources_from_this_item

            # Employee contracts:
            if isinstance(item, EmployeeContract):
                # resources:
                free_resources_from_this_item = item.pay_salary(step)
                free_resources = free_resources + free_resources_from_this_item
                if verbose:
                    print('[step ' + str(step) + '] Free resources from employee contract :: ' + item.name + ' = ' + str(free_resources_from_this_item))

        if step == 0:
            free_resources = free_resources + self.initial_free_resources
            if verbose:
                print('[step ' + str(step) + '] Initial free resources = ' + str(self.initial_free_resources))

        self.free_resources[step] = free_resources - self.expenditures[step]
        if verbose:
            print('----------------------------------------------------------------------------')
            print('[step ' + str(step) + '] Total free resources to allocate = ' + str(self.free_resources[step]))

    def allocate_free_resources(self, step, verbose=True):
        # assumption: only single current account
        for item in self.portfolio:
            if isinstance(item, CurrentAccount):
                item.deposit(step, self.free_resources[step])
                if verbose:
                    print('[step ' + str(step) + '] Resources allocated to current account :: ' + item.name + ' = ' + str(self.free_resources[step]))
                    print('=========================================================================================')

    def live(self, step, verbose=False):
        self.calculate_free_resources(step, verbose)
        self.allocate_free_resources(step, verbose)