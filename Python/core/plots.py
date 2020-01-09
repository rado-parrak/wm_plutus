import matplotlib.pyplot as plt
import numpy as np
from context.party import Party

class PlutusPlotter():
    '''
    classdocs
    '''

    def __init__(self, party: Party):
        self.party = party


    def plot_resources_evolution(self):
        plt.plot(self.party.free_resources.values(), label='free_resources')
        plt.plot(self.party.expenditures.values(), label='expenditures')

        plt.xlabel('month')
        plt.ylabel('portfolio value')
        plt.title('Free resources & expenditures | ' + self.party.name)
        plt.legend()

        return plt.show()