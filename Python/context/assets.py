class Asset:
    '''
    classdocs
    '''

    def __init__(self, id, name):
        self.id = id
        self.name = name


class RealEstate(Asset):

    def __init__(self, id, name, current_market_value, property_tax, renovation_costs, renovation_steps: set, house_community_costs, linked_market_object: str):
        # Constructor
        super().__init__(id, name)
        self.current_market_value = current_market_value
        self.price = dict()
        self.monthly_costs = dict()
        self.property_tax = property_tax
        self.renovation_costs = renovation_costs
        self.renovation_steps = renovation_steps
        self.house_community_costs = house_community_costs
        self.linked_market_object = linked_market_object


    def project_price(self, step, index_value: float):
        if step == 0:
            self.price[step] = self.current_market_value
        else:
            if self.price[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.price[step] = self.price[0] * index_value

    def project_monthly_costs(self, step):
        # renovations happen at distinct steps - renovation_steps
        if step in self.renovation_steps:
            self.monthly_costs[step] = self.property_tax / 12 + self.renovation_costs + self.house_community_costs/12
        else:
            self.monthly_costs[step] = self.property_tax / 12 + self.house_community_costs/12

