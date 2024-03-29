from context.instruments import CurrentAccount, Mortgage, Share
from context.assets import RealEstate
from context.agreements import EmployeeContract, RentalAgreement
from context.market import Market
import logging, datetime
class Portfolio:

    def __init__(self, logger: logging.Logger, elements:dict):

        self.elements = dict()
        self.logger = logger
        self.elements =  elements

        #self.logger.info('Initializing portfolio with elements: {}'.format(self.list_elements()))

    def list_elements(self):
        return(list(self.elements.keys())) 

    def add_element(self, element_to_add):
        self.elements[element_to_add.id]=element_to_add

    def remove_element(self, element_to_remove):
        del self.elements[element_to_remove.id]

class Party:

    def __init__(self, id: str, logger:logging.Logger, initial_free_cash: float, initial_portfolio: Portfolio, monthly_expenditures: float, discount_rate: float, events: dict, market:dict, birthdate:datetime.date, today:datetime.date, retirement_age:int):

        self.id = id
        self.initial_free_cash = initial_free_cash
        self.cash = dict()
        self.free_cash = dict()
        self.portfolio = initial_portfolio
        self.portfolio_types = dict()
        self.monthly_expenditures = monthly_expenditures
        self.expenditures = dict()
        self.expenditures_consumption = dict()
        self.expenditures_consumption_re = dict()
        self.expenditures_mortgage = dict()
        self.monthly_income = dict()
        self.monthly_income_re = dict() # income from real-estate
        self.monhtly_income_dividends = dict() # dividend income
        self.free_cash_pv = dict()
        self.discount_rate = discount_rate
        self.portfolio_values = dict()
        self.logger = logger
        self.events = events
        self.market = market
        self.birthdate = birthdate
        self.retirement_age = retirement_age
        self.event_domain = []
        self.current_age = ((today - birthdate).days)//365.25
        self.today = today

        self.logger.info('Initializing party: {}'.format(self.id))
        self.logger.info('with initial portfolio: {}'.format(initial_portfolio.list_elements()))
        self.logger.info('with initial free cash: {}'.format(self.initial_free_cash))

    def calculate_expenditures(self, step):        
        # expenditures from consumption
        expenditures = self.monthly_expenditures
        self.expenditures_consumption[step] = expenditures
        self.logger.debug('[STEP {}] Expenditures from consumption: {:.2f}'.format(step, self.monthly_expenditures))

        # expenditures from porfolio holding
        for key, el in self.portfolio.elements.items():
            if isinstance(el, Mortgage):
                el.calculate_monthly_costs(step)
                el.calculateInterestPayment(step)
                el.calculatePrincipalPayment(step)
                el.calculateOutstandingAmount(step)
                expenditures = expenditures + el.monthly_costs[step]
                self.expenditures_mortgage[step] = el.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from mortgage: {:.2f}'.format(step, el.monthly_costs[step]))

            if isinstance(el, CurrentAccount):
                el.calculate_monthly_costs(step)
                expenditures = expenditures + el.monthly_costs[step]
                self.logger.debug('[STEP {}] Expenditures from the current account: {:.2f}'.format(step, el.monthly_costs[step]))

            if isinstance(el, RealEstate):
                el.calculate_monthly_costs(step)
                expenditures = expenditures + el.monthly_costs[step]
                self.expenditures_consumption_re[step] = el.monthly_costs[step]
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
                self.monthly_income[step] = el.cash_flow[step]
                self.logger.debug('[STEP {}] cash from the employee contract "{}": {:.2f}'.format(step, el.id, el.cash_flow[step]))

            if isinstance(el, RentalAgreement):
                if el.my_position == 'renter':
                    el.calculate_cashflow(step)
                    cash = cash + el.cash_flow[step]
                    self.monthly_income_re[step] = el.cash_flow[step]
                    self.logger.debug('[STEP {}] cash from the rental agreement "{}": {:.2f}'.format(step, el.id, el.cash_flow[step]))

            if isinstance(el, Share):
                el.calculate_value(step)
                self.monhtly_income_dividends[step] = el.pay_dividend(step)
                cash = cash + self.monhtly_income_dividends[step]
                self.logger.debug('[STEP {}] cash from the dividends of share "{}": {:.2f}'.format(step, el.id, self.monhtly_income_dividends[step]))

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
        if 'sell' in self.events.keys():
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
        if 'buy' in self.events.keys():
            for event in self.events['buy']:
                if event['step'] == step:
                    # decrease saldo_of_events by bought asset
                    saldo_of_events -= event['current_market_value']
                    self.logger.debug('[STEP {}] New saldo of events after bought portfolio element: {:.2f} '.format(step, saldo_of_events))

                    # create new portfolio element and add to portfolio
                    el = self.create_new_portfolio_element(event)
                    self.portfolio.add_element(el)
                    self.logger.info('[STEP {}] New portfolio element {} added'.format(step, el.id))

        # create events:
        if 'create' in self.events.keys():
            for event in self.events['create']:
                if event['step'] == step:
                    # create new portfolio element and add to portfolio
                    el = self.create_new_portfolio_element(event)
                    self.portfolio.add_element(el)
                    self.logger.info('[STEP {}] New portfolio element {} added'.format(step, el.id))


        return(saldo_of_events)

    def act_on_post_events(self, step):
        # transfer events:
        if 'transfer' in self.events.keys():
            for event in self.events['transfer']:
                if event['step'] == step:
                    # decrease by amount 'from'
                    for key, el in self.portfolio.elements.copy().items():
                        if el.id == event['from']:
                            el.value[step] = el.value[step] - event['amount']
                            self.logger.debug('[STEP {}] Outstanding of account {} decreased by: {:.2f} '.format(step, el.id, event['amount']))
                            self.logger.debug('[STEP {}] New outstanding value of account {} is: {:.2f} '.format(step, el.id, el.value[step]))

                    # increase by amount 'to'   
                    for key, el in self.portfolio.elements.copy().items():
                        if el.id == event['to']:
                            el.value[step] = el.value[step] + event['amount']
                            self.logger.debug('[STEP {}] Outstanding of account {} increased by: {:.2f} '.format(step, el.id, event['amount']))
                            self.logger.debug('[STEP {}] New outstanding value of account {} is: {:.2f} '.format(step, el.id, el.value[step]))

    def create_new_portfolio_element(self, event_description: dict):
        if event_description['type'] == 'RealEstate':
            return(RealEstate(id=event_description['id']
                            , current_market_value=event_description['current_market_value']
                            , property_tax = event_description['property_tax']
                            , house_community_costs = event_description['house_community_costs']
                            , real_estate_index = self.market[event_description['real_estate_index']]
                            , logger=self.logger
                            , events=None # TODO: make also new production to be linked to events
                            , current_step=event_description['current_step']))

        if event_description['type'] == 'Mortgage':
            return(Mortgage(id=event_description['id'], 
                            logger=self.logger, 
                            principal=event_description['principal'], 
                            cnit=event_description['cnit'], 
                            maturity_in_years=event_description['maturity_in_years'],
                            current_step=event_description['current_step']))

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

                # enrich event domain
                self.event_domain.append(step)

def setup_portfolio(portfolio_config:dict, indices:dict, logger) -> dict:

    portfolio = dict()

    # (1) employee contracts
    if 'employee_contracts' in portfolio_config.keys():
        for ec in portfolio_config['employee_contracts']:
            logger.info('Adding Employee Contract: {} to the portfolio'.format(ec['id']))
            portfolio[ec['id']] = EmployeeContract(id=ec['id'], 
                                                salary = ec['salary'], 
                                                income_tax_rate = ec['income_tax_rate'], 
                                                duration=ec['duration'],
                                                events=ec['events'], 
                                                logger=logger)

    # (2) accounts
    if 'accounts' in portfolio_config.keys():
        for acc in portfolio_config['accounts']:
            logger.info('Adding Account: {} to the portfolio'.format(acc['id']))
            if acc['type'] == 'current':
                portfolio[acc['id']] = CurrentAccount(id=acc['id'],
                                                        current_outstanding=acc['current_outstanding'],
                                                        monthly_cost= acc['monthly_cost'],
                                                        cnit=acc['cnit'], 
                                                        logger=logger, 
                                                        primary=bool(acc['primary']))

    # (2) real estate assets
    if 'real_estate' in portfolio_config.keys():
        for re in portfolio_config['real_estate']:
            logger.info('Adding Real Estate Asset: {} to the portfolio'.format(re['id']))
            portfolio[re['id']] = RealEstate(id=re['id'], 
                                                current_market_value=re['current_market_value'], 
                                                property_tax = re['property_tax'], 
                                                house_community_costs = re['house_community_costs'], 
                                                real_estate_index = indices[re['index']], 
                                                logger=logger, 
                                                events=re['events'])

    # (3) rental agreement
    if 'rental_agreements' in portfolio_config.keys():
        for ra in portfolio_config['rental_agreements']:
            logger.info('Adding Rental Agreement: {} to the portfolio'.format(ra['id']))
            portfolio[ra['id']] = RentalAgreement(id=ra['id'],
                                                    index = indices[ra['index']],
                                                    my_position=ra['my_position'],
                                                    rent=ra['rent'],
                                                    yearly_costs=ra['yearly_costs'],
                                                    logger=logger)

    # (4) shares
    if 'shares' in portfolio_config.keys():
        for s in portfolio_config['shares']:
            logger.info('Adding Share: {} to the portfolio'.format(s['id']))
            portfolio[s['id']] = Share(id=s['id'],
                                        price=s['price'],
                                        units=s['units'],
                                        index=indices[s['index']],
                                        dividend_yield=s['dividend_yield'],
                                        dividend_step=s['dividend_step'],
                                        current_step=0,
                                        logger=logger)

    # (5) mortgage agreements
    if 'mortgage_agreements' in portfolio_config.keys():
        for m in portfolio_config['mortgage_agreements']:
            logger.info('Adding Mortgage agreement: {} to the portfolio'.format(m['id']))
            portfolio[m['id']] = Mortgage(id=m['id'], 
                                            principal=m['principal'], 
                                            cnit=m['cnit'], 
                                            maturity_in_years=m['maturity_in_years'], 
                                            logger=logger)

    return(portfolio)


    