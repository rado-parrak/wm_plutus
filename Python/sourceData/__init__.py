from context.instruments import InstrumentType, AccountType, InstrumentClass

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
party['monthly_gross_wage'] = 35000
party['current_age'] = 30

source_data['parties'].append(party)

# ii) Instruments
source_data['instruments'] = []

contract_1 = dict()
contract_1['type'] = InstrumentType.CURRENT_ACCOUNT
contract_1['name'] = 'bezny_ucet'
contract_1['ID']   = '001'
contract_1['cnit'] = 0.0001
contract_1['current_outstanding'] = 25000
contract_1['monthly_cost'] = 25
contract_1['accountType'] = AccountType.ASSET
contract_1['instrumentClass'] = InstrumentClass.CASH_BALANCE

contract_2 = dict()
contract_2['name'] = 'dalsi_bezny_ucet'
contract_2['ID'] = '002'
contract_2['type'] = InstrumentType.CURRENT_ACCOUNT
contract_2['cnit'] = 0.00001
contract_2['current_outstanding'] = 7500
contract_2['monthly_cost'] = 0.0
contract_2['accountType'] = AccountType.ASSET
contract_2['instrumentClass'] = InstrumentClass.CASH_BALANCE

contract_3 = dict()
contract_3['name'] = 'sporak'
contract_3['ID'] = '003'
contract_3['type'] = InstrumentType.SAVING_ACCOUNT
contract_3['cnit'] = 0.01
contract_3['current_outstanding'] = 250000
contract_3['monthly_cost'] = 12
contract_3['accountType'] = AccountType.ASSET
contract_3['instrumentClass'] = InstrumentClass.SAVING

source_data['instruments'].append(contract_1) 
source_data['instruments'].append(contract_2)
source_data['instruments'].append(contract_3)

# iii) Relations
source_data['relations'] = dict()
source_data['relations']['party_instrument'] = dict()
source_data['relations']['party_instrument']['00X'] = ['001', '002','003']

# iv) Config
source_data['config'] = dict()

# iv) Behaviour
# TODO: Currently only 1 behaviour allowed per tool configuration
source_data['behaviour'] = dict()
source_data['behaviour']['party'] = dict()
source_data['behaviour']['party']['00X'] = dict()
source_data['behaviour']['party']['00X']['saving_allocation_weight'] = 0.3
source_data['behaviour']['party']['00X']['investment_allocation_weight'] = 0.2
source_data['behaviour']['party']['00X']['cash_allocation_weight'] = 0.5
 
# vi) Scenarios
source_data['scenarios'] = list()

scenario= dict()
scenario['ID'] = 1
scenario['name'] = 'baseline_scenario'

source_data['scenarios'].append(scenario)