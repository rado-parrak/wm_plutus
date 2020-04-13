import matplotlib.pyplot as plt
import numpy as np
from context.party import Party

class PlutusPlotter():
    '''
    classdocs
    '''

    def __init__(self, party: Party):
        self.party = party


    def plot_overall_financial_status(self):
        plt.plot(self.party.free_resources.values(), label='free resources')
        plt.plot(self.party.resources.values(), label='resources')
        plt.plot(self.party.expenditures.values(), label='expenditures')

        plt.xlabel('month')
        plt.ylabel('value')
        plt.title('Overall financial evolution | ' + self.party.name)
        plt.legend()

        return plt.show()

    def plot_overall_financial_status_pv(self):
        plt.plot(self.party.free_resources_pv.values(), label='PV of free resources')

        plt.xlabel('month')
        plt.ylabel('PV of value')
        plt.title('PV of overall financial evolution | ' + self.party.name)
        plt.legend()

        return plt.show()

    def plot_inflation_gap(self):
        plt.plot(self.party.free_resources.values(), label='free resources')
        plt.plot(self.party.free_resources_pv.values(), label='PV of free resources')

        plt.xlabel('month')
        plt.ylabel('value')
        plt.title('Inflation gap | ' + self.party.name)
        plt.legend()

        return plt.show()

    def plot_portfolio_value(self):
        plt.plot(self.party.portfolio_values.values(), label='Portfolio value')

        plt.xlabel('month')
        plt.ylabel('value')
        plt.title('Portfolio value | ' + self.party.name)
        plt.legend()

        return plt.show()