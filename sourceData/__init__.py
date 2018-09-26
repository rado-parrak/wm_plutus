# Source data
source_data = dict()

# i) Party
source_data['party'] = dict()
source_data['party']['name'] = 'Rado'
source_data['party']['monthly_income'] = 100

# ii) Portfolio
source_data['portfolio'] = []

contract_1 = dict()
contract_1['name'] = 'bezny_ucet'
contract_1['type'] = 'current_account'
contract_1['cnit'] = 0.0
contract_1['current_outstanding'] = 120
contract_1['monthly_cost'] = 0.0

contract_2 = dict()
contract_2['name'] = 'dalsi_bezny_ucet'
contract_2['type'] = 'current_account'
contract_2['cnit'] = 0.0
contract_2['current_outstanding'] = 50
contract_2['monthly_cost'] = 0.0

source_data['portfolio'].append(contract_1) 
source_data['portfolio'].append(contract_2)

# iii) Context
source_data['context'] = dict()
source_data['context']['event_domain'] = dict()
source_data['context']['event_domain']['months'] = 10

# iv) Behaviour
source_data['behaviour'] = dict()
source_data['behaviour']['scenarios'] = []

scenario_1 = dict()
scenario_1['financial'] = dict()
scenario_1['financial']['consumption_share'] = 0.3
scenario_1['financial']['investment_share'] = 0.2
scenario_1['financial']['portfolio_shares'] = [0.4, 0.6]

source_data['behaviour']['scenarios'].append(scenario_1)