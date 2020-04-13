from scipy.interpolate import interp1d

class Market:
    def __init__(self, market_objects: dict, scenarios: list, steps: int):
        self.scenarios = scenarios
        self.market_objects = market_objects

        # project market values for each market object in each scenario
        for scenario in scenarios:
            for market_object_name, market_object in self.market_objects.items():
                if isinstance(market_object, Index):
                    market_object.project_index(steps=steps, scenario=scenario)

class MarketScenario:
    def __init__(self, name, market_ojects_scenario_definitions: dict):
        self.name = name
        self.market_objects_scenario_definitions = market_ojects_scenario_definitions

class Index:
    def __init__(self, name, initial_value):
        self.name = name
        self.initial_value = initial_value
        self.monthly_values = dict()

    def project_index(self, steps, scenario: MarketScenario, type='linear'):
        yearly_values = dict()
        yearly_values[0] = self.initial_value
        scenario_type = scenario.market_objects_scenario_definitions[self.name]['scenario_type']

        if scenario_type == 'constant':
            annual_change = scenario.market_objects_scenario_definitions[self.name]['annual_change']
            # calculate number of steps to make it whole year (such that we always interpolate)
            whole_year_steps = steps / 12
            if steps % 12 != 0:
                whole_year_steps = ((steps // 12) + 1) * 12

            # calculate yearly steps
            for yearly_step in range(1, int(whole_year_steps+1)):
                yearly_values[yearly_step*12] = yearly_values[(yearly_step-1)*12] * (1+annual_change)

            # interpolate
            self.monthly_values[scenario.name] = self.interpolate_to_monthly(yearly_values, steps, interpolation_type=type)

    def interpolate_to_monthly(self, yearly_values, steps, interpolation_type='linear') -> dict:
        monthly_values = dict()
        interpolator = interp1d(list(yearly_values.keys()), list(yearly_values.values()), kind=interpolation_type)
        for step in range(0, steps+1):
            monthly_values[step] = interpolator(step)

        return(monthly_values)

