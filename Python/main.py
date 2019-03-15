'''
Created on Jul 26, 2018

@author: Rado
'''
#===============================================================================
# from calculator import Calculator
# from initialize import Initialize
# # --- INITIALIZE ---
# rredis = Initialize();
# 
# # --- DO CALCULATIONS ---
# calc = Calculator(rredis, 'root')
# calc.run()
# 
# # i) calculate outstandings on all instruments:
# #calc.projectOutstandings()
# 
# print('Calculation done!')
#===============================================================================
    
from historyKeeper.Parser import ParserCsob

parser = ParserCsob()
parser.parseRaw("../../03_data/transactions/CSOB/pohyby-na uctu 217207635_0300-20190315-1749.csv")
parser.updateHistory()
parser.saveHistory()

data.to_pickle("../../03_data/transactions/_aggregated/csob_current_account")
