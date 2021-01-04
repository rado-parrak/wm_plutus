import matplotlib.pyplot as plt
import numpy as np
from context.party import Party

class PartyPlotter():

    def __init__(self, party: Party):
        self.party = party


    def plot_position_evolution(self):

        fig, [[p1, p2], [p3, p4]] = plt.subplots(2, 2, figsize=(16, 8))
        fig.text(0.5, 1.0, 'Financial overview', horizontalalignment='center', verticalalignment='top', fontsize=18)

        # Cash balance
        p1.plot(self.party.free_cash.values(), label='free cash')
        p1.plot(self.party.cash.values(), label='cash')
        p1.plot(self.party.expenditures.values(), label='expenditures')
        p1.grid(axis='y', which='major')
        p1.ticklabel_format(style='plain')
        p1.set_xlabel('month')
        p1.set_ylabel('cash position')
        p1.set_title('Cash | ' + self.party.id)
        p1.legend()

        # Portofolio balance
        p2.plot(self.party.portfolio_values.values(), label='Portfolio value')
        p2.grid(axis='y', which='major')
        p2.ticklabel_format(style='plain')
        p2.set_xlabel('month')
        p2.set_ylabel('value')
        p2.set_title('Portfolio | ' + self.party.id)
        p2.legend()

        # PV of cash balance
        p3.plot(self.party.free_cash_pv.values(), label='PV of free cash')
        p3.grid(axis='y', which='major')
        p3.ticklabel_format(style='plain')
        p3.set_xlabel('month')
        p3.set_ylabel('cash position')
        p3.set_title('PV of cash | ' + self.party.id)
        p3.legend()

        # Effect of inflation on free cash
        p4.bar(x=range(len(list(self.party.free_cash.values())))
                ,height=np.subtract(list(self.party.free_cash.values()), list(self.party.free_cash_pv.values())), label='Inflation cost')
        p4.ticklabel_format(style='plain')
        p4.set_xlabel('month')
        p4.set_ylabel('cost of inflation')
        p4.set_title('Inflation effect on free cash | ' + self.party.id)
        p4.legend()

        fig.subplots_adjust(wspace=0.4, hspace=0.3)

        #return fig.show()

 