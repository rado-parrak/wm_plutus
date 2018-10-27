from context.instruments import InstrumentType, AccountType

# Source data
source_data = dict()

# Run Config:
source_data['runs_config'] = list()
run_config = dict()
run_config['ID'] = 'uniqueRunID'
run_config['name'] = 'dummy_run'
run_config['run_date'] = '2018-09-30'
run_config['life_expectancy'] = 10

source_data['runs_config'].append(run_config)

# i) Parties
source_data['parties'] = list()

party = dict()
party['ID'] = '00X'
party['name'] = 'Rado'
party['monthly_gross_wage'] = 100
party['current_age'] = 30

source_data['parties'].append(party)

# ii) Instruments
source_data['instruments'] = []

contract_1 = dict()
contract_1['type'] = InstrumentType.CURRENT_ACCOUNT
contract_1['name'] = 'bezny_ucet'
contract_1['ID']   = '001'
contract_1['cnit'] = 0.0
contract_1['current_outstanding'] = 120
contract_1['monthly_cost'] = 5
contract_1['accountType'] = AccountType.ASSET

contract_2 = dict()
contract_2['name'] = 'dalsi_bezny_ucet'
contract_2['ID'] = '002'
contract_2['type'] = InstrumentType.CURRENT_ACCOUNT
contract_2['cnit'] = 0.05
contract_2['current_outstanding'] = 50
contract_2['monthly_cost'] = 0.0
contract_2['accountType'] = AccountType.ASSET

source_data['instruments'].append(contract_1) 
source_data['instruments'].append(contract_2)

# iii) Relations
source_data['relations'] = dict()
source_data['relations']['party_instrument'] = dict()
source_data['relations']['party_instrument']['Rado'] = ['001', '002']

# iv) Config
source_data['config'] = dict()

# iv) Behaviour
source_data['behaviours'] = list()

behaviour= dict()
behaviour['ID'] = 1
behaviour['name'] = 'baseline_behaviour'
behaviour['saving_allocation_weight'] = 0.3
behaviour['investment_allocation_weight'] = 0.2
behaviour['cash_allocation_weight'] = 0.5
behaviour['instrument_shares']= dict()
behaviour['instrument_shares']['001'] = 0.3
behaviour['instrument_shares']['002'] = 0.7

source_data['behaviours'].append(behaviour)

# vi) Scenarios
source_data['scenarios'] = list()

scenario= dict()
scenario['ID'] = 1
scenario['name'] = 'baseline_scenario'

source_data['scenarios'].append(scenario)