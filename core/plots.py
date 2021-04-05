import matplotlib.pyplot as plt
import numpy as np
from context.party import Party
from context.instruments import CurrentAccount, Share, Mortgage
from context.assets import RealEstate

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

    def plot_wealth_evolution(self):

        width = 0.5 # the width of the bars: can also be len(x) sequence

        fig, [p1, p2] = plt.subplots(2, 1, figsize=(16, 16))
        
        # (1) Wealth
        b = np.array([0 for x in range(0, len(self.party.free_cash.values()))])
        
        for el in self.party.portfolio.elements.values():            
            if isinstance(el, CurrentAccount):
                instrument_values = el.value
                x_ticks = np.array(list(instrument_values.keys()))
                y_ticks = np.array(list(instrument_values.values()))

                p1.bar(x_ticks,
                        y_ticks, 
                        width,
                        bottom=b,
                        label=el.id)

                b = b+y_ticks

            if isinstance(el, RealEstate):
                asset_prices = el.price
                x_ticks = np.array(list(asset_prices.keys()))
                y_ticks = np.array(list(asset_prices.values()))

                p1.bar(x_ticks,
                        y_ticks, 
                        width,
                        bottom=b,
                        label=el.id)

                b = b+y_ticks

            if isinstance(el, Share):
                share_values = el.value
                x_ticks = np.array(list(share_values.keys()))
                y_ticks = np.array(list(share_values.values()))

                p1.bar(x_ticks,
                        y_ticks, 
                        width,
                        bottom=b,
                        label=el.id)

                b = b+y_ticks

            if isinstance(el, Mortgage):
                b = np.array([0 for x in range(0, len(self.party.free_cash.values()))])
                outstanding_amount = el.outstanding_amount
                x_ticks = np.array(list(outstanding_amount.keys()))
                y_ticks = np.array(list(outstanding_amount.values()))

                p1.bar(x_ticks,
                        -y_ticks, 
                        width,
                        bottom=b,
                        label=el.id)

                b = b-y_ticks

        p1.set_ylabel('Value')
        p1.set_xlabel('Month')
        p1.set_title('Wealth evolution')
        p1.ticklabel_format(style='plain')
        p1.grid(axis='y', which='major')
        p1.legend()

        # (2) Cashflows
        b = np.array([0 for x in range(0, len(self.party.free_cash.values()))])

        # (2.i) expendidures from consumption
        x_ticks = np.array(list(self.party.expenditures_consumption.keys()))
        y_ticks = np.array(list(self.party.expenditures_consumption.values()))
        p2.bar(x_ticks, -y_ticks, width, label='expenditures from consumption')
        
        # (2.ii) expenditures from mortgage
        b = b-y_ticks
        x_ticks = np.array(list(self.party.expenditures_mortgage.keys()))
        y_ticks = np.array(list(self.party.expenditures_mortgage.values()))
        p2.bar(x_ticks, -y_ticks, width, label='expenditures from mortgage', bottom=b)

        # 2(.ii) expenditures from real-estate
        b = b-y_ticks
        x_ticks = np.array(list(self.party.expenditures_consumption_re.keys()))
        y_ticks = np.array(list(self.party.expenditures_consumption_re.values()))
        p2.bar(x_ticks, -y_ticks, width, label='expenditures from real estate', bottom=b)
        
        # (2.iii) income from work
        b = np.array([0 for x in range(0, len(self.party.free_cash.values()))])

        x_ticks = np.array(list(self.party.monthly_income.keys()))
        y_ticks = np.array(list(self.party.monthly_income.values()))
        p2.bar(x_ticks, y_ticks, width, label='income from job')

        # (2.iv) income from real estate assets
        # TODO: extend for multiple RE assets
        b = b+y_ticks
        x_ticks = np.array(list(self.party.monthly_income_re.keys()))
        y_ticks = np.array(list(self.party.monthly_income_re.values()))
        p2.bar(x_ticks, y_ticks, width, label='income from real estate', bottom=b)

        # (2.v) income from dividends
        b = b+y_ticks
        x_ticks = np.array(list(self.party.monhtly_income_dividends.keys()))
        y_ticks = np.array(list(self.party.monhtly_income_dividends.values()))
        p2.bar(x_ticks, y_ticks, width, label='income from dividends', bottom=b)

        p2.set_ylabel('Cashflow')
        p2.set_xlabel('Month')
        p2.set_title('Cashflows')
        p2.ticklabel_format(style='plain')
        p2.grid(axis='y', which='major')
        p2.legend()

        plt.show()


