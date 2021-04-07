import matplotlib.pyplot as plt
import numpy as np
from context.party import Party
from context.instruments import CurrentAccount, Share, Mortgage
from context.agreements import RentalAgreement, EmployeeContract
from context.assets import RealEstate
from dateutil.relativedelta import relativedelta
import matplotlib.dates as mdates

class PartyPlotter():

    def __init__(self, party: Party):
        self.party = party
        self.step_domain = self.party.event_domain
        self.date_domain = [self.party.today+relativedelta(months=x) for x in self.step_domain]
        self.age_domain = [((x - self.party.birthdate).days)/365.25 for x in self.date_domain]

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

    def plot_bar(self, plot, dictionary, width, bottom, label, sign):
        x_ticks = np.array(list(dictionary.keys()))
        y_ticks = np.array(list(dictionary.values()))

        plot.bar(x_ticks, sign*y_ticks, width, bottom=bottom, label=label)
        bottom = bottom + sign*y_ticks 
        return(bottom)

    def fill_empty_with_zeros(self, dictionary):
        mini = np.amin(np.array(list(dictionary.keys())))
        if mini>0:
            for i in range(0,mini):
                dictionary[i]=0.0

        dictionary = dict(sorted(dictionary.items()))

        return(dictionary)

    def plot_wealth_evolution(self):
        # TODO: This could probably done in a more elegant way...

        WIDTH = 0.5 # the width of the bars: can also be len(x) sequence

        fig, [p1, p2] = plt.subplots(2, 1, figsize=(16, 16))
        
        # (1) Wealth
        # (A) Plot POSITIVE wealth first:
        BOTTOM = np.array([0 for x in self.step_domain])
        for el in self.party.portfolio.elements.values():
            if isinstance(el, CurrentAccount) or isinstance(el, Share):
                d = self.fill_empty_with_zeros(el.value)
                y_ticks = np.array(list(d.values()))
                p1.bar(np.array(self.age_domain), y_ticks, WIDTH, bottom=BOTTOM, label=el.id)
                BOTTOM = BOTTOM + y_ticks 

            if isinstance(el, RealEstate): 
                d = self.fill_empty_with_zeros(el.price)
                y_ticks = np.array(list(d.values()))
                p1.bar(np.array(self.age_domain), y_ticks, WIDTH, bottom=BOTTOM, label=el.id)
                BOTTOM = BOTTOM + y_ticks 
                
        # (B) Plot NEGATIVE wealth second:
        BOTTOM = np.array([0 for x in self.step_domain])
        for el in self.party.portfolio.elements.values():
            if isinstance(el, Mortgage):
                d = self.fill_empty_with_zeros(el.outstanding_amount)
                y_ticks = np.array(list(d.values()))           
                p1.bar(np.array(self.age_domain), -y_ticks, WIDTH, bottom=BOTTOM, label=el.id)
                BOTTOM = BOTTOM - y_ticks

        # Minor ticks every month.
        fmt_month = mdates.MonthLocator()
        p1.xaxis.set_minor_locator(fmt_month)
        p1.set_ylabel('Value')
        p1.set_xlabel('Age')
        p1.set_title('Wealth evolution')
        #p1.ticklabel_format(axis="y", style='plain')
        p1.axvline(x=self.party.retirement_age, color='r')
        p1.grid(axis='y', which='major')
        p1.legend()

        # (2) Cashflows
        width = WIDTH
        portfolio_element_types = [type(x) for x in self.party.portfolio.elements.values()]
        BOTTOM = np.array([0 for x in self.step_domain])

        # (2.i) expendidures from consumption
        dict_of_values = self.party.expenditures_consumption
        dict_of_values = self.fill_empty_with_zeros(dict_of_values)
        BOTTOM = self.plot_bar(p2, dict_of_values, WIDTH, BOTTOM,'expenditures from consumption',-1)
        
        # (2.ii) expenditures from mortgage
        if Mortgage in portfolio_element_types:
            dict_of_values = self.party.expenditures_mortgage
            dict_of_values = self.fill_empty_with_zeros(dict_of_values)
            BOTTOM = self.plot_bar(p2, dict_of_values, WIDTH, BOTTOM,'expenditures from mortgage',-1)

        # 2(.ii) expenditures from real-estate
        if RealEstate in portfolio_element_types:
            dict_of_values = self.party.expenditures_consumption_re
            dict_of_values = self.fill_empty_with_zeros(dict_of_values)
            BOTTOM = self.plot_bar(p2, dict_of_values, WIDTH, BOTTOM,'expenditures from real estate',-1)
        
        # (2.iii) income from work
        BOTTOM = np.array([0 for x in self.step_domain])

        dict_of_values = self.party.monthly_income
        dict_of_values = self.fill_empty_with_zeros(dict_of_values)
        BOTTOM = self.plot_bar(p2, dict_of_values, WIDTH, BOTTOM,'income from job',1)

        # (2.iv) income from real estate assets
        # TODO: extend for multiple RE assets
        if RentalAgreement in portfolio_element_types:  
            dict_of_values = self.party.monthly_income_re
            dict_of_values = self.fill_empty_with_zeros(dict_of_values)
            BOTTOM = self.plot_bar(p2, dict_of_values, WIDTH, BOTTOM,'income from real estate',1)

        # (2.v) income from dividends
        if Share in portfolio_element_types:
            dict_of_values = self.party.monhtly_income_dividends
            dict_of_values = self.fill_empty_with_zeros(dict_of_values)
            BOTTOM = self.plot_bar(p2, dict_of_values, WIDTH, BOTTOM,'income from dividends',1)

        p2.set_ylabel('Cashflow')
        p2.set_xlabel('Month')
        p2.set_title('Cashflows')
        p2.ticklabel_format(style='plain')
        p2.grid(axis='y', which='major')
        p2.legend()

        plt.show()


