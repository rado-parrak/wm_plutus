class Asset:
    '''
    classdocs
    '''

    def __init__(self, id, name):
        self.id = id
        self.name = name


class RealEstate(Asset):

    def __init__(self, id, name, current_market_value):
        # Constructor
        super().__init__(id, name)
        self.current_market_value = current_market_value
        self.price = dict()
        self.costs = dict()


    def projectPrice(self, step, inflation, market_trend):
        # inflation is the economy-wide inflation
        # market trend is a add-on on the top of economy-wide inflation

        monthly_inflation = (1 + inflation) ** (1 / 12) - 1
        monthly_market_trend = (1 + market_trend) ** (1 / 12) - 1

        if step == 0:
            self.price[step] = self.current_market_value
        else:
            if self.price[step - 1] is None:
                raise Exception('Value at previous step to step ' + str(step) + ' not calculated!')
            else:
                self.price[step] = self.price[step - 1] * (1 + monthly_inflation + monthly_market_trend)

    def projectCosts(self, step, property_tax, renovation_costs, renovation_steps: set, house_community_costs):
        # renovations happen at distinct steps - renovation_steps
        if step in renovation_steps:
            self.costs[step] = property_tax / 12 + renovation_costs + house_community_costs/12
        else:
            self.costs[step] = property_tax / 12 + house_community_costs/12

