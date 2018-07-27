# 1. PARTY
JOE_NAME = 'joe'
JOE_MONTHLY_INCOME = 100

# portfolio
JOE_PORTFOLIO = dict()
JOE_PORTFOLIO[1] = ['current_account','CSOB_bezny_ucet', 100.0, 0.05, 2.0]
JOE_PORTFOLIO[2] = ['current_account','CSOB_bezny_ucet_2', 400.0, 0.01, 1.0]

# 2. CONTEXT
event_domain_steps = 5

# 2.i Scenarios
scenarios = dict()
scenario_1 = dict()


# 3 Behaviour
# 3.1 Product-related

behaviourBase = dict()
behaviour = dict()
financial_behaviour = dict()
portfolio_weights = dict()

financial_behaviour['monthly_spending_share'] = 0.3
financial_behaviour['saving_share'] = 0.45
financial_behaviour['saving_frequency'] = 'monthly'
financial_behaviour['inv_share'] = 0.55
financial_behaviour['inv_frequency'] = 'monthly'

portfolio_weights['CSOB_bezny_ucet'] = 0.3
portfolio_weights['CSOB_bezny_ucet_2'] = 0.7

behaviour['financial'] = financial_behaviour
behaviour['portfolio'] = portfolio_weights
behaviourBase['standard'] = behaviour



