# TODO:
# - present value
# - macro-economics as functionals
# - behaviour as functionals
# - group party view via party relations

import sys
from context.instruments import CurrentAccount, Mortgage
from context.assets import RealEstate
from context.agreements import RentalAgreement, UtilitiesAgreement, EmployeeContract
from context.party import Party
from context.market import Market, MarketScenario, Index
from core.plots import PlutusPlotter

# Define
# a) define global pars
steps = 36

# b) instruments, agreements and assets
current_account = CurrentAccount(id='001', name='Raduv bezny ucet', current_outstanding=1e5, monthly_cost=100, cnit=0.0)
mortgage = Mortgage(id='002', name='Radova hypoteka', principal=4.5e6, cnit=0.015, maturity_in_years=30)
flat = RealEstate(id='003', name='Byt', current_market_value=6e6, property_tax=2000, renovation_costs=2e5,renovation_steps={12, 24, 36}, house_community_costs=6000, linked_market_object='REI')
employeeContract = EmployeeContract(id='003', name='Credo zamestnanecka smlouva', average_yearly_validity=1.0, salary=65000,
                                    bonus_steps=set(range(6, 361, 6)), bonus_rate=0.3, yearly_salary_trend=0.05
                                    , income_tax_rate=0.42)

# c) run simulation given market
market_objects = {'REI': Index(name='REI', initial_value=1.0)}
market_scenario = MarketScenario(name='stable', market_ojects_scenario_definitions={'REI': {'annual_change': 0.07, 'scenario_type': 'constant'}})
market = Market(market_objects, scenarios=[market_scenario], steps=steps)

# d) party
party = Party(name='Rado'
              , initial_free_resources=2.5e6
              , initial_portfolio={current_account, mortgage, flat, employeeContract}
              , monthly_expenditures=20000
              , discount_rate=0.02
              , market=market)

party.live(steps)

# Plotting
# plotter = PlutusPlotter(party)
# plotter.plot_overall_financial_status()
# plotter.plot_overall_financial_status_pv()
# plotter.plot_inflation_gap()
# plotter.plot_portfolio_value()