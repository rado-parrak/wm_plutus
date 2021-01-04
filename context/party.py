from context.instruments import CurrentAccount, Mortgage
from context.assets import RealEstate
from context.agreements import EmployeeContract
from context.market import Market
import logging
class Portfolio:

    def __init__(self, logger: logging.Logger, *args):

        self.elements = dict()
        self.logger = logger
        for el in args:
            self.elements[el.id] = el

        #self.logger.info('Initializing portfolio with elements: {}'.format(self.list_elements()))

    def list_elements(self):
        return(list(self.elements.keys())) 

    def add_element(self, element_to_add):
        self.elements[element_to_add.id]=element_to_add

    def remove_element(self, element_to_remove):
        del self.elements[element_to_remove.id]

class Party:

    def __init__(self, id: str, logger:logging.Logger, initial_free_cash: float, initial_portfolio: Portfolio, monthly_expenditures: float, discount_rate: float, events: dict):

        self.id = id
        self.initial_free_cash = initial_free_cash
        self.cash = dict()
        self.free_cash = dict()
        self.portfolio = initial_portfolio
        self.portfolio_types = dict()
        self.monthly_expenditures = monthly_expenditures
        self.expenditures = dict()
        self.free_cash_pv = dict()
        self.discount_rate = discount_rate
        self.portfolio_values = dict()
        self.logger = logger
        self.events = events

        self.logger.info('Initializing party: {}'.format(self.id))
        self.logger.info('with initial portfolio: {}'.format(initial_portfolio.list_elements()))
        self.logger.info('with initial free cash: {}'.format(self.initial_free_cash))

    def calculate_expenditures(self, step):        
        # expenditures from consumption
        expenditures = self.monthly_expenditures
        self.logger.debug('[STEP {}] Expenditures from consumption: {:.2f}'.format(step, self.monthly_expenditures))

        # expenditures from porfolio holding
        for key, el in self.portfolio.elements.items():
            if isinstance(el, Mortgage):
                el.calculate_monthly_costs(step)
                expenditures = expenditures + el.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from mortgage: {:.2f}'.format(step, el.monthly_costs[step]))

            if isinstance(el, CurrentAccount):
                el.calculate_monthly_costs(step)
                expenditures = expenditures + el.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from the current account: {:.2f}'.format(step, el.monthly_costs[step]))

            if isinstance(el, RealEstate):
                el.calculate_monthly_costs(step)
                expenditures = expenditures + el.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from the real estate {:.2f}'.format(step, el.monthly_costs[step]))

        # total expenditures
        self.expenditures[step] = expenditures
        self.logger.info('[STEP {}] Total expenditures: {:.2f}'.format(step, expenditures))

    def calculate_cash(self, step, saldo_of_events):
        cash = 0.0
        if step == 0:
            cash = self.initial_free_cash

        for key,el in self.portfolio.elements.items():
            if isinstance(el, CurrentAccount):
                el.calculate_value(step)
                if el.primary:
                    cash = cash + el.value[step]
                    self.logger.debug('[STEP {}] cash from PRIMARY current account "{}": {:.2f}'.format(step, el.id ,el.value[step]))

            if isinstance(el, EmployeeContract):
                el.calculate_cashflow(step)
                cash = cash + el.cash_flow[step]
                self.logger.debug('[STEP {}] cash from the employee contract "{}": {:.2f}'.format(step, el.id, el.cash_flow[step]))

        self.cash[step] = cash + saldo_of_events
        self.logger.info('[STEP {}] Total cash: {:.2f}'.format(step, cash))

    def calculate_free_cash(self, step, saldo_of_events):
        self.calculate_cash(step, saldo_of_events)
        self.calculate_expenditures(step)
        self.free_cash[step] = self.cash[step] - self.expenditures[step]

        self.logger.info('[STEP {}] Free cash: {:.2f}'.format(step, self.free_cash[step]))

    def allocate_free_cash(self, step):
        # TODO: assumption: only single PRIMARY current account
        for key, el in self.portfolio.elements.items():
            if isinstance(el, CurrentAccount):
                if el.primary:
                    el.withdraw_all(step)
                    el.deposit(step, self.free_cash[step])

    def discount_free_cash(self, step: int, discount_rate: float):
        # TODO: discout rate / factor should be also a curve, not a point
        
        # discount factor calculation
        df = 1 / ((1+discount_rate)**(step/12.0))
        self.logger.debug('[STEP {}] Discount factor: {:.4f}'.format(step, df))

        self.free_cash_pv[step] = self.free_cash[step] * df
        self.logger.info('[STEP {}] Discounted free cash: {:.2f}'.format(step, self.free_cash_pv[step]))

    def calculate_portfolio_value(self, step):
        portfolio_value = 0.0

        for key, el in self.portfolio.elements.items():
            if isinstance(el, RealEstate):
                el.calculate_price(step)
                portfolio_value = portfolio_value + el.price[step]

        self.portfolio_values[step] = portfolio_value
        self.logger.info('[STEP {}] Portfolio value: {:.2f}'.format(step, portfolio_value))

    def act_on_pre_events(self, step):
        saldo_of_events = 0.0

        # sell events:
        if self.events['sell'] is not None:
            for event in self.events['sell']:
                if event['step'] == step:
                    for key, el in self.portfolio.elements.copy().items():
                        if el.id == event['id']:
                            # increase saldo_of_events by sold asset
                            saldo_of_events += el.price[step-1]
                            self.logger.debug('[STEP {}] New saldo of events after sold portfolio element: {:.2f} '.format(step, saldo_of_events))

                            # delete asset from the portfolio:
                            self.portfolio.remove_element(el)
                            self.logger.info('[STEP {}] Asset {} sold for: {:.2f}'.format(step, el.id, el.price[step-1]))

        # buy events:
        if self.events['buy'] is not None:
            for event in self.events['buy']:
                if event['step'] == step:
                    # decrease saldo_of_events by bought asset
                    saldo_of_events -= event['current_market_value']
                    self.logger.debug('[STEP {}] New saldo of events after bought portfolio element: {:.2f} '.format(step, saldo_of_events))

                    # create new portfolio element and add to portfolio
                    el = self.create_new_portfolio_element(event)
                    self.portfolio.add_element(el)
                    self.logger.info('[STEP {}] New portfolio element {} added'.format(step, el.id))

        return(saldo_of_events)

    def act_on_post_events(self, step):
        # transfer events:
        if self.events['transfer'] is not None:
            for event in self.events['transfer']:
                if event['step'] == step:
                    # decrease by amount 'from'
                    for key, el in self.portfolio.elements.copy().items():
                        if el.id == event['from']:
                            el.value[step] = el.value[step] - event['amount']
                            self.logger.debug('[STEP {}] Outstanding of account {} decreased by: {:.2f} '.format(step, el.id, event['amount']))

                    # increase by amount 'to'
                    for key, el in self.portfolio.elements.copy().items():
                        if el.id == event['to']:
                            el.value[step] = el.value[step] + event['amount']
                            self.logger.debug('[STEP {}] Outstanding of account {} increased by: {:.2f} '.format(step, el.id, event['amount']))

    def create_new_portfolio_element(self, event_description: dict):
        if event_description['type'] == 'RealEstate':
            return(RealEstate(id=event_description['id']
                            , current_market_value=event_description['current_market_value']
                            , property_tax = event_description['property_tax']
                            , house_community_costs = event_description['house_community_costs']
                            , real_estate_index = event_description['real_estate_index']
                            , logger=self.logger
                            , events=None # TODO: make also new production to be linked to events
                            , current_step= event_description['step'])) 

    def live(self, steps: int):
            for step in range(0, steps):
                self.logger.info('')
                self.logger.info('>>>>>> Party {} is living the step: {} <<<<<<<'.format(self.id, step))
                
                # pre-events
                saldo_of_events = self.act_on_pre_events(step)
                
                # cash
                self.calculate_free_cash(step, saldo_of_events)
                self.allocate_free_cash(step)
                self.discount_free_cash(step, self.discount_rate)

                # post-events
                self.act_on_post_events(step)

                # balance
                self.calculate_portfolio_value(step)
